from typing import List
from util.db_conn_util import DBConnUtil
from entity.jobs import Jobs
from entity.company import Company
from entity.applicant import Applicant
from entity.application import Application
from datetime import datetime
from exception.deadline_over_exception import DeadlinePassedException
from exception.negative_salary_exception import NegativeSalaryException
from exception.invalid_email_exception import InvalidEmailException


class DatabaseManager:

    def __init__(self):
        self.conn = DBConnUtil.get_connection(r'C:/Users/anush/PycharmProjects/Career Hub/util/db.properties')
        self.cursor = self.conn.cursor()

    def initialize_database(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Companies (
            company_id INT AUTO_INCREMENT PRIMARY KEY,
            company_name VARCHAR(255),
            location VARCHAR(255)
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Jobs (
            job_id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            job_title VARCHAR(255),
            job_description TEXT,
            job_location VARCHAR(255),
            salary DECIMAL(10,2),
            job_type VARCHAR(50),
            posted_date DATETIME,
            deadline DATETIME,
            FOREIGN KEY (company_id) REFERENCES Companies(company_id)
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Applicants (
            applicant_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(20),
            resume TEXT
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Applications (
            application_id INT AUTO_INCREMENT PRIMARY KEY,
            job_id INT,
            applicant_id INT,
            application_date DATETIME,
            cover_letter TEXT,
            FOREIGN KEY (job_id) REFERENCES JobListings(job_id),
            FOREIGN KEY (applicant_id) REFERENCES Applicants(applicant_id)
        )""")

        self.conn.commit()

    def insert_company(self, company: Company):
        self.cursor.execute("""
        INSERT INTO Companies (company_name, location) VALUES (%s, %s)
        """, (company.company_name, company.location))
        self.conn.commit()
        company.company_id = self.cursor.lastrowid

    def insert_job(self, company_id, job_title, description, location, salary, job_type, deadline):
        query = """
                INSERT INTO Jobs (company_id, jobtitle, job_description, job_location, salary, job_type, posted_date, application_deadline)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(),%s)
            """
        self.cursor.execute(query, (company_id, job_title, description, location, salary, job_type, deadline))
        self.conn.commit()
        print("Job posted successfully.")

    def insert_applicant(self, applicant:Applicant):
        try:
            Applicant.validate_email(applicant.email)  # Email format validation
            self.cursor.execute("""
                    INSERT INTO Applicants (first_name, last_name, email, phone, resume)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (
            applicant.first_name, applicant.last_name, applicant.email, applicant.phone, applicant.resume))
            self.conn.commit()
            applicant.applicant_id = self.cursor.lastrowid
            print("Applicant profile created successfully.")
        except InvalidEmailException as e:
            raise e

    def insert_application(self, application: Application):
        self.cursor.execute("""
        INSERT INTO Applications (job_id, applicant_id, application_date, cover_letter)
        VALUES (%s, %s, %s, %s)
        """, (application.job_id, application.applicant_id, application.application_date, application.cover_letter))
        self.conn.commit()
        application.application_id = self.cursor.lastrowid

    def insert_job_application(self, applicant_id, job_id, cover_letter):
        self.cursor.execute("SELECT application_deadline FROM Jobs WHERE job_id = %s", (job_id,))
        deadline_result = self.cursor.fetchone()

        if deadline_result and deadline_result[0] and datetime.now() > deadline_result[0]:
            raise DeadlinePassedException("Application deadline has passed.")

        self.cursor.execute("""
                INSERT INTO Applications (applicant_id, job_id, application_date, cover_letter)
                VALUES (%s, %s, %s, %s)
            """, (applicant_id, job_id, datetime.now(), cover_letter))
        self.conn.commit()
        print("Application submitted successfully.")

    def get_jobs(self) -> List[Jobs]:
        self.cursor.execute("SELECT * FROM Jobs")
        rows = self.cursor.fetchall()
        return [Jobs(*row[1:], job_id=row[0]) for row in rows]

    def get_companies(self) -> List[Company]:
        self.cursor.execute("SELECT * FROM Companies")
        rows = self.cursor.fetchall()
        return [Company(*row) for row in rows]

    def get_applicants(self) -> List[Applicant]:
        self.cursor.execute("SELECT * FROM Applicants")
        rows = self.cursor.fetchall()
        return [Applicant(
            applicant_id=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            phone=row[4],
            resume=row[5],
            experience=row[6]
        ) for row in rows]

    def get_applications_for_job(self, job_id: int) -> List[Application]:
        self.cursor.execute("SELECT * FROM applications WHERE job_id = %s", (job_id,))
        rows = self.cursor.fetchall()
        return [ Application(
            application_id=row[0],
            job_id=row[1],
            applicant_id=row[2],
            application_date=row[3],
            cover_letter=row[4]
            ) for row in rows]

    def get_jobs_by_salary_range(self, min_salary, max_salary):
        query = """
                SELECT j.jobtitle, c.company_name, j.salary
                FROM Jobs j
                JOIN Companies c ON j.company_id = c.company_id
                WHERE j.salary BETWEEN %s AND %s
            """
        self.cursor.execute(query, (min_salary, max_salary))
        return self.cursor.fetchall()

    def calculate_average_salary(self):
        self.cursor.execute("SELECT job_id, salary FROM Jobs")
        rows = self.cursor.fetchall()

        if not rows:
            print("No jobs found.")
            return 0

        total_salary = 0
        count = 0

        for job_id, salary in rows:
            if salary is None or salary < 0:
                print(f"Invalid salary for job ID {job_id}.")
                print("Skipping to the next job.")
                raise NegativeSalaryException(job_id=job_id)
            total_salary += salary
            count += 1

        average_salary = total_salary / count if count > 0 else 0
        return average_salary

    def close(self):
        self.cursor.close()
        self.conn.close()

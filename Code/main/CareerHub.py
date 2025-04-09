from dao.database_manager import DatabaseManager
from entity.company import Company
from entity.applicant import Applicant
from exception.invalid_email_exception import InvalidEmailException
from exception.negative_salary_exception import NegativeSalaryException
from exception.deadline_over_exception import DeadlinePassedException
from entity.application import Application
from datetime import datetime


def main():
    db = DatabaseManager()
    db.initialize_database()

    while True:
        print("""
-------- Job Portal Menu --------
1. Register Company
2. Post a Job
3. Register Applicant
4. Apply for Job
5. View All Jobs
6. View All Companies
7. View All Applicants
8. View Applications for a Job
9. Search Jobs by Salary Range
10. Calculate Average Salary
11. Exit
        """)

        choice = input("Enter your choice (1-11): ")

        try:
            if choice == "1":
                name = input("Enter company name: ")
                location = input("Enter company location: ")
                company = Company(company_name=name, location=location)
                db.insert_company(company)
                print(f"Company {name} registered successfully.")

            elif choice == "2":
                company_id = int(input("Enter company ID: "))
                title = input("Enter job title: ")
                description = input("Enter job description: ")
                location = input("Enter job location: ")
                salary = float(input("Enter job salary: "))
                job_type = input("Enter job type (full time,part time,contract): ")
                deadline = input("Enter application deadline (YYYY-MM-DD HH:MM:SS): ")
                deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
                db.insert_job(company_id, title, description, location, salary, job_type, deadline)

            elif choice == "3":
                email = input("Enter email: ")
                first = input("Enter first name: ")
                last = input("Enter last name: ")
                phone = input("Enter phone number: ")
                resume = input("Enter resume content or file name: ")
                applicant = Applicant(first_name=first, last_name=last, email=email, phone=phone, resume=resume)
                db.insert_applicant(applicant)

            elif choice == "4":
                applicant_id = int(input("Enter applicant ID: "))
                job_id = int(input("Enter job ID to apply for: "))
                cover = input("Enter cover letter: ")
                db.insert_job_application(applicant_id, job_id, cover)

            elif choice == "5":
                jobs = db.get_jobs()
                for job in jobs:
                    print(job)

            elif choice == "6":
                companies = db.get_companies()
                for company in companies:
                    print(company)

            elif choice == "7":
                applicants = db.get_applicants()
                for app in applicants:
                    print(app)

            elif choice == "8":
                job_id = int(input("Enter job ID: "))
                applications = db.get_applications_for_job(job_id)
                for app in applications:
                    print(f"Application ID: {app.application_id}, Applicant ID: {app.applicant_id}, Date: {app.application_date}, Cover: {app.cover_letter[:30]}...")

            elif choice == "9":
                min_sal = float(input("Enter minimum salary: "))
                max_sal = float(input("Enter maximum salary: "))
                results = db.get_jobs_by_salary_range(min_sal, max_sal)
                for title, company, salary in results:
                    print(f"{title} at {company} - ₹{salary}")

            elif choice == "10":
                avg = db.calculate_average_salary()
                print(f"Average Salary: ₹{avg:.2f}")

            elif choice == "11":
                print("Exiting Job Portal. Goodbye!")
                db.close()
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 11.")

        except InvalidEmailException as e:
            print(f"Email Error: {e}")
        except NegativeSalaryException as e:
            print(f"Salary Error: Negative salary found for job ID {e.job_id}.")
        except DeadlinePassedException as e:
            print(f"Deadline Error: {e}")
        except ValueError as e:
            print("Input error. Please enter data in the correct format.")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()

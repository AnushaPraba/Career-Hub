import re
from exception.invalid_email_exception import InvalidEmailException
class Applicant:
    def __init__(self, first_name, last_name, email, phone, resume,experience, applicant_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.resume = resume
        self.experience = experience
        self.applicant_id = applicant_id

    def __str__(self):
        return (
            f"\n--- Applicant ---\n"
            f"Applicant ID : {self.applicant_id}\n"
            f"Name         : {self.first_name} {self.last_name}\n"
            f"Email        : {self.email}\n"
            f"Phone        : {self.phone}\n"
            f"Resume       : {self.resume}\n"
            f"Experience   : {self.experience}\n"
        )

    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise InvalidEmailException(email)



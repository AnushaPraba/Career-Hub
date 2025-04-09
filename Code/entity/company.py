class Company:
    def __init__(self,company_name,location,company_id=None):
        self.company_name=company_name
        self.location=location
        self.company_id=company_id

    def __str__(self):
        return (
            f"\n--- Company ---\n"
            f"Company ID   : {self.company_id}\n"
            f"Name         : {self.company_name}\n"
            f"Location     : {self.location}\n"
        )
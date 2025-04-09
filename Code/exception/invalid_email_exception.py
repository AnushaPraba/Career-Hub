class InvalidEmailException(Exception):
    def __init__(self, message="Invalid email format."):
        super().__init__(message)

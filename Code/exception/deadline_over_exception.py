class DeadlinePassedException(Exception):
    def __init__(self, message="Deadline has passed. Application cannot be submitted."):
        super().__init__(message)

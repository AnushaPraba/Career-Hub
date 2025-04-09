class FileUploadException(Exception):
    pass

class FileNotFound(FileUploadException):
    def __init__(self, message="File not found."):
        super().__init__(message)

class FileTooLarge(FileUploadException):
    def __init__(self, message="File size exceeds the limit."):
        super().__init__(message)

class UnsupportedFormat(FileUploadException):
    def __init__(self, message="Unsupported file format."):
        super().__init__(message)

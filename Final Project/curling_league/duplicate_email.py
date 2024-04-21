class DuplicateEmail(Exception):
    def __init__(self, message, email):
        super().__init__(message)
        self.email = email

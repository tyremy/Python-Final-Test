class DuplicateOID(Exception):
    def __init__(self, message, oid):
        super().__init__(message)
        self.email = oid

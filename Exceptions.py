class EmailNotSetError(Exception):
    def __init__(self):
        self.message = "Email not set"


class IDNotSetError(Exception):
    def __init__(self):
        self.message = "ID not set"


class KeyNotSetError(Exception):
    def __init__(self):
        self.message = "Key not set"

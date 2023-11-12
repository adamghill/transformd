class InvalidSpecError(Exception):
    def __init__(self, key: str, data: dict):
        self.key = key
        self.data = data

        message = f"'{self.key}' is invalid"

        super().__init__(message)

class FyleError(Exception):
    status_code = 400

    def __init__(self, status_code, message):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        res = dict()
        res['message'] = self.message
        return res

class ValidationError(FyleError):
    def __init__(self, message="Validation error"):
        super().__init__(status_code=400, message=message)

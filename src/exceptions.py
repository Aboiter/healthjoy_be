from werkzeug.exceptions import (
    HTTPException,
    NotFound,
    BadRequest
)


class DuplicateRepoName(BadRequest):
    code = 400
    description = "The repository name that you are trying to fork already exists in your account."

    def __init__(self, description=None):
        self.description = description or self.description


class DoesNotExistError(NotFound):
    code = 404
    description = "Not Found"

    def __init__(self, description=None):
        self.description = description or self.description


class ValidationError(HTTPException):
    code = 417
    description = "Validation error."

    def __init__(self, description=None):
        self.description = description or self.description

from mimetypes import init
from typing import Any, Sequence
from fastapi import Request, HTTPException, status
from .response import send_failed_response
from fastapi.exceptions import RequestValidationError


class NotAllowedException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "You are not project manager"
        super().__init__(self.status_code, self.detail)


class NotAuthenticatedExceptiion(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "You are not authenticated"
        super().__init__(self.status_code, self.detail)


class NotFoundException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "Not found!"
        super().__init__(self.status_code, self.detail)


class UsernameTakenException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = {"error": "Username already takend"}
        super().__init__(self.status_code, self.detail)


def init_exception_handler(app):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    app.add_exception_handler(RequestValidationError,
                              validation_exception_handler)


async def http_exception_handler(request: Request, exc: HTTPException):
    print(exc.detail)
    return send_failed_response(str(exc.detail), status_code=exc.status_code)


async def general_exception_handler(request: Request, exc: Exception):
    return send_failed_response({"exc": str(exc)})


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()[0]
    msg = errors["msg"]
    if len(errors["loc"]) == 1:
        field = errors["loc"][0]
    else:
        field = errors["loc"][1]
    return send_failed_response({field: msg}, status_code=400)

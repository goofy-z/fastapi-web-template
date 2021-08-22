import json
from starlette.responses import JSONResponse
from starlette.requests import Request


class APIException(Exception):
    """
    Http处理基类
    """

    def __init__(self, status_code=None, msg=None, error_id=None, message=None):
        """

        :param status_code:
        :param msg: deprecated ,use message
        :param error_id:
        :param message:
        """
        self.status_code = status_code
        self.message = message
        self.error_id = error_id

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, error_info={self.message!r})"


async def http_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """
    替换fastapi的except_handler
    """
    return JSONResponse(
        {"error_info": exc.message, "error_type": exc.error_id},
        status_code=exc.status_code,
        headers={"Content-Type": "application/json"},
    )


class BadRequestException(APIException):
    def __init__(self, message):
        APIException.__init__(self, 400, error_id="error_bad_param", message=message)


class ConflictException(APIException):
    def __init__(self, message=None):
        APIException.__init__(self, 409, error_id="error_already_exists", message=message)


class UnAuthenticatedException(APIException):
    def __init__(self, message=None):
        APIException.__init__(self, 401, error_id="error_unauthenticated", message=message)


class ForbiddenException(APIException):
    def __init__(self, message=None):
        APIException.__init__(self, 403, error_id="error_permission", message=message)


class NotFoundException(APIException):
    def __init__(self, message=None):
        APIException.__init__(self, 404, error_id="error_not_found", message=message)


class InternalServerError(APIException):
    def __init__(self, message=None):
        APIException.__init__(self, 500, error_id="Internal Server Error", message=message)

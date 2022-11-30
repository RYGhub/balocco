import fastapi

from balocco.server import models

__all__ = (
    "ApiException",
    "MissingAuthHeader",
    "InvalidAuthHeader",
    "InvalidCredentials",
    "WrongAuthHeader",
    "ResourceNotFound",
    "MultipleResultsFound",
    "CompulsiveJoin"
)


class ApiException(Exception):
    """
    Base class for :mod:`open_dictionary` exceptions.
    """

    STATUS_CODE: int = 500
    ERROR_CODE: str = "UNKNOWN"
    REASON: str = "Unknown error, please report this as a bug to the application developers."

    @classmethod
    def to_model(cls) -> models.error.ApiErrorModel:
        return models.error.ApiErrorModel(error_code=cls.ERROR_CODE, reason=cls.REASON)

    @classmethod
    def to_response(cls) -> fastapi.Response:
        return fastapi.Response(content=cls.to_model().json(), status_code=cls.STATUS_CODE)


class MissingAuthHeader(ApiException):
    STATUS_CODE = 401
    ERROR_CODE = "MISSING_AUTH_HEADER"
    REASON = "The Authorization header is missing."


class InvalidAuthHeader(ApiException):
    STATUS_CODE = 401
    ERROR_CODE = "INVALID_AUTH_HEADER"
    REASON = "The provided Authorization header is invalid."


class InvalidCredentials(ApiException):
    STATUS_CODE = 401
    ERROR_CODE = "INVALID_CREDENTIALS"
    REASON = "The provided credentials do not match up with any user in the database."


class WrongAuthHeader(ApiException):
    STATUS_CODE = 401
    ERROR_CODE = "WRONG_AUTH_HEADER"
    REASON = "The token provided in the Authorization header does not match any resource."


class ResourceNotFound(ApiException):
    STATUS_CODE = 404
    ERROR_CODE = "NOT_FOUND"
    REASON = "The requested resource was not found. Either it does not exist, or you are not authorized to view it."


class MultipleResultsFound(ApiException):
    STATUS_CODE = 500
    ERROR_CODE = "MULTIPLE_FOUND"
    REASON = "Multiple resources were found with the requested identifier. This is probably a problem in the application database. If you are the system admininistrator, ensure you have run all the available migrations through Alembic."


class CompulsiveJoin(ApiException):
    STATUS_CODE = 500
    ERROR_CODE = "MULTIPLE_JOIN"
    REASON = "You are trying to join a Giveaway you're already partecipating in."


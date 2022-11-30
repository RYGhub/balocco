from balocco.server.models import base

__all__ = (
    "ApiErrorModel",
)


class ApiErrorModel(base.ApiModel):
    """
    Model for errors returned by the API.
    """

    error_code: str
    reason: str

    class Config(base.ApiModel.Config):
        schema_extra = {
            "example": {
                "error_code": "NOT_FOUND",
                "reason": "The requested object was not found.",
            },
        }

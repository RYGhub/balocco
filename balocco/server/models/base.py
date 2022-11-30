from __future__ import annotations

import abc
import datetime
import uuid

import pydantic

__all__ = (
    "ApiModel",
    "ApiORMModel",
)


class ApiModel(pydantic.BaseModel, metaclass=abc.ABCMeta):
    """
    Base model for :mod:`impressive_strawberry`\\ 's :mod:`pydantic` models.
    """

    class Config(pydantic.BaseModel.Config):
        json_encoders = {
            uuid.UUID:
                lambda obj: str(obj),
            datetime.datetime:
                lambda obj: obj.timestamp(),
        }


class ApiORMModel(ApiModel, metaclass=abc.ABCMeta):
    """
    Extension to :class:`.StrawberryModel` which enables the :attr:`.StrawberryModel.Config.orm_mode`.
    """

    class Config(ApiModel.Config):
        orm_mode = True

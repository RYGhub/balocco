import typing as t
from uuid import UUID
from balocco.server.models import base
from datetime import datetime

__all__ = (
    "UserEdit",
    "ServerEdit",
    "GiveawayEdit",
    "ItemEdit"
)


class UserEdit(base.ApiORMModel):
    """
    **Edit** model for :class:`.database.tables.User`.
    """

    username: str

    class Config(base.ApiORMModel.Config):
        schema_extra = {
            "example": {
                "username": "Nemesis",
            },
        }


class ServerEdit(base.ApiORMModel):
    """
    **Edit** model for :class:`.database.tables.Server`.
    """

    name: str
    motd: str
    logo_uri: t.Optional[str]
    custom_colors: t.Optional[str]


class GiveawayEdit(base.ApiORMModel):
    """
    **Edit** model for :class:`.database.tables.Giveaway`.
    """

    name: str
    description: str
    closing_date: datetime
    assignment_date: datetime


class ItemEdit(base.ApiORMModel):
    """
    **Edit** model for :class:`.database.tables.Item`.
    """
    name: str
    giveaway_id: UUID
    obtain_action: str

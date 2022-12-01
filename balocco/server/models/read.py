import typing
from uuid import UUID
from balocco.server.models import edit
from balocco.server.models import base

__all__ = (
    "UserRead",
    "ServerRead",
    "GiveawayRead",
    "ItemRead"
)


class UserRead(base.ApiORMModel):
    """
    **Read** model for :class:`.database.tables.User`.
    """

    id: UUID
    username: str
    email: str

    class Config(edit.UserEdit.Config):
        schema_extra = {
            "example": {
                **edit.UserEdit.Config.schema_extra["example"],
                "id": "70fd1bf3-69dd-4cde-9d41-42368221849f",
            },
        }


class ServerRead(edit.ServerEdit):
    """
    **Read** model for :class:`.database.tables.Server`.
    """

    id: UUID


class GiveawayRead(edit.GiveawayEdit):
    """
    **Read** model for :class:`.database.tables.Giveaway`.
    """

    id: UUID
    issuer_id: UUID
    active: bool


class ItemRead(base.ApiORMModel):
    id: UUID
    data: typing.Optional[dict]
    obtainable: bool
    winner_id: typing.Optional[UUID]
    giveaway_id: UUID
    taken: bool
    name: str
    giveaway_id: UUID

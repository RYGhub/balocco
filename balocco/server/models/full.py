import typing
from balocco.server.models import read, base

__all__ = ("UserFull",
           "ServerFull",
           "Planetarium",
           "Signup",
           "GiveawayFull",
           "ItemFull")


class ServerFull(read.ServerRead):
    """
    **Full** model for :class:`.database.tables.Dictionary`.
    """

    admin: typing.Optional[read.UserRead]


class Planetarium(base.ApiModel):
    """
    **Planetarium-compliant** model for :class:`.database.tables.Server`.
    """

    version: str
    type: str
    oauth_public: str
    audience: str
    domain: str

    server: ServerFull


class Signup(base.ApiORMModel):
    """
    **Full** model for :class:`.database.tables.Signup`.
    """

    user: typing.Optional[read.UserRead]
    giveaway: typing.Optional[read.GiveawayRead]


class ItemFull(read.ItemRead):
    """
    **Full** model for :class:`.database.tables.ItemFull`.
    """

    winner: typing.Optional[read.UserRead]
    giveaway: typing.Optional[read.GiveawayRead]
    obtain_action: str


class GiveawayFull(read.GiveawayRead):
    """
    **Full** model for :class:`.database.tables.Giveaway`.
    """

    issuer: typing.Optional[read.UserRead]
    signups: typing.List[Signup]
    items: typing.List[read.ItemRead]


class UserFull(read.UserRead):
    """
    **Full** model for :class:`.database.tables.User`.
    """
    issued: typing.List[read.GiveawayRead]
    wins: typing.List[read.ItemRead]
    signups: typing.List[Signup]


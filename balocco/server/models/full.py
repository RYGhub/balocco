import typing
from balocco.server.models import read, base

__all__ = ()


class UserFull(read.UserRead):
    """
    **Full** model for :class:`.database.tables.User`.
    """
    pass


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
    server: ServerFull

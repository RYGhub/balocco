import uuid
import os

import sqlalchemy.orm
import requests
from sqlalchemy import Column, String, LargeBinary, ForeignKey, JSON, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

__all__ = (
    "Base",
    "User",
    "Server",
    "Item",
    "Giveaway",
    "Signup"
)

Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(LargeBinary, nullable=True)
    admin_of = relationship("Server", back_populates="admin")

    issued = relationship("Giveaway", back_populates="issuer")
    wins = relationship("Item", back_populates="winner")
    signups = relationship("Signup", back_populates="user")


class Giveaway(Base):
    __tablename__ = "giveaway"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    closing_date = Column(DateTime, nullable=False)
    assignment_date = Column(DateTime, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    issuer_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    issuer = relationship("User", back_populates="issued")
    items = relationship("Item", back_populates="giveaway")
    signups = relationship("Signup", back_populates="giveaway")


class Signup(Base):
    __tablename__ = "signup"

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True)
    user = relationship("User", back_populates="signups")
    giveaway_id = Column(UUID(as_uuid=True), ForeignKey("giveaway.id"), primary_key=True)
    giveaway = relationship("Giveaway", back_populates="signups")


class Item(Base):
    __tablename__ = "item"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    data = Column(JSON)
    obtainable = Column(Boolean, nullable=False, default=True)
    obtain_action = Column(String, nullable=False)
    taken = Column(Boolean, nullable=False, default=False)

    value = Column(Integer, nullable=False, default=0, server_default="0")
    """
    The weight of the item, considered during the distribution of items in the giveaway.

    To ignore values and distribute items evenly, ensure the values of the distributed items are all equal.
    """

    winner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    winner = relationship("User", back_populates="wins")
    giveaway_id = Column(UUID(as_uuid=True), ForeignKey("giveaway.id"), nullable=False)
    giveaway = relationship("Giveaway", back_populates="items")

    def set_value_to_itad_lowest(self) -> float:
        """
        Set the :attr:`.value` of the item to the lowest price it has ever been from the `IsThereAnyDeal API <https://itad.docs.apiary.io/>`_.

        Expects :attr:`.data` to contain the appid of the item at the ``appid`` key; if missing, sets the value to 0.

        Expects the item to exist on ITAD; if missing, sets the value to 0.

        :returns: The lowest price of the item, in Euro cents (``249`` for 2.49 €).
        """

        itad_api_key = os.environ["BALOCCO_ITAD_KEY"]

        appid = self.data["appid"]

        r = requests.get(f"https://api.isthereanydeal.com/v02/game/plain/", params=dict(
            key=itad_api_key,
            shop="steam",
            game_id=f"app/{appid}",
        ))
        r.raise_for_status()
        r = r.json()
        
        try:
            app_plain: str = r["data"]["plain"]
        except KeyError:
            return 0

        r = requests.get(f"https://api.isthereanydeal.com/v01/game/lowest/", params=dict(
            key=itad_api_key,
            plains=app_plain,
            region="eu1",
            country="IT",
        ))
        r.raise_for_status()
        r = r.json()

        try:
            lowest: float = r["data"][app_plain]["price"]
        except KeyError:
            return 0
        else:
            return int(lowest * 100)


class Server(Base):
    __tablename__ = "server"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    motd = Column(String)
    logo_uri = Column(String)
    custom_colors = Column(JSON)

    admin_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    admin = relationship("User", back_populates="admin_of")

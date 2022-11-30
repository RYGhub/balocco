import uuid

import sqlalchemy.orm
from sqlalchemy import Column, String, LargeBinary, ForeignKey, JSON, DateTime, Boolean
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

    issuer_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
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

    winner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    winner = relationship("User", back_populates="wins")
    giveaway_id = Column(UUID(as_uuid=True), ForeignKey("giveaway.id"))
    giveaway = relationship("Giveaway", back_populates="items")


class Server(Base):
    __tablename__ = "server"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    motd = Column(String)
    logo_uri = Column(String)
    custom_colors = Column(JSON)

    admin_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    admin = relationship("User", back_populates="admin_of")

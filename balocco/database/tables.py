import uuid

import sqlalchemy.orm
from sqlalchemy import Column, String, LargeBinary, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

__all__ = (
    "Base",
    "User",
    "Server"
)

Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(LargeBinary, nullable=True)
    admin_of = relationship("Server", back_populates="admin")


class Server(Base):
    __tablename__ = "server"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    motd = Column(String)
    logo_uri = Column(String)
    custom_colors = Column(JSON)

    admin_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    admin = relationship("User", back_populates="admin_of")

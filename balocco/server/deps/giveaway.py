import json
from uuid import UUID

from balocco.database import tables, engine
from balocco.server import crud
from balocco.server.deps.database import dep_session
from balocco.server.errors import ResourceNotFound
import fastapi

__all__ = (
    "dep_giveaways",
    "dep_giveaway",
)


def dep_giveaways(session: engine.Session = fastapi.Depends(dep_session)):
    return session.query(tables.Giveaway).all()


def dep_giveaway(giveaway_id: UUID, session: engine.Session = fastapi.Depends(dep_session)):
    return crud.quick_retrieve(session, tables.Giveaway, id=giveaway_id)

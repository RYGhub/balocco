import json
from uuid import UUID

from balocco.database import tables, engine
from balocco.server import crud
from balocco.server.deps.database import dep_session
from balocco.server.errors import ResourceNotFound
import fastapi

__all__ = (
    "dep_items",
    "dep_items_giveaway",
    "dep_item"
)


def dep_items(session: engine.Session = fastapi.Depends(dep_session)):
    return session.query(tables.Item).all()


def dep_items_giveaway(giveaway_id: UUID, session: engine.Session = fastapi.Depends(dep_session)):
    return session.query(tables.Item).filter_by(giveaway_id=giveaway_id).all()


def dep_item(item_id: UUID, session: engine.Session = fastapi.Depends(dep_session)):
    return crud.quick_retrieve(session, tables.Item, id=item_id)

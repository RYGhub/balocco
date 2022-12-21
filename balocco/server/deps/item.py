import json
from uuid import UUID

from balocco.database import tables, engine
from balocco.server import crud
from balocco.server.deps.database import dep_session
from balocco.server.deps.user import dep_user
from balocco.server.errors import ResourceNotFound
import fastapi

__all__ = (
    "dep_items",
    "dep_items_giveaway",
    "dep_item",
    "dep_item_weaker"
)


def dep_items(session: engine.Session = fastapi.Depends(dep_session)):
    return session.query(tables.Item).all()


def dep_items_giveaway(giveaway_id: UUID, session: engine.Session = fastapi.Depends(dep_session)):
    return session.query(tables.Item).filter_by(giveaway_id=giveaway_id).all()


def dep_item(item_id: UUID, session: engine.Session = fastapi.Depends(dep_session),
             current_user=fastapi.Depends(dep_user)):
    item = crud.quick_retrieve(session, tables.Item, id=item_id)
    if not current_user.admin_of and item not in current_user.wins:
        raise ResourceNotFound
    return item


def dep_item_weaker(item_id: UUID, session: engine.Session = fastapi.Depends(dep_session),
                    current_user=fastapi.Depends(dep_user)):
    item = crud.quick_retrieve(session, tables.Item, id=item_id)
    return item

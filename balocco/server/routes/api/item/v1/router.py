import datetime

import sqlalchemy.exc
from pydantic import typing

from balocco.server import models
import fastapi
from fastapi import Depends
from balocco.server import crud
from balocco.server import deps
from balocco.database.engine import Session
from balocco.database import tables
from balocco.server.authentication import auth
from balocco.server.errors import *

router = fastapi.routing.APIRouter(
    prefix="/api/item/v1",
    tags=["Item v1"]
)


@router.get("/{item_id}", dependencies=[Depends(auth.implicit_scheme)], response_model=models.full.ItemFull)
async def get_item(
        item: tables.Giveaway = fastapi.Depends(deps.dep_item),
        current_user: tables.User = fastapi.Depends(deps.dep_user)):
    return item


@router.post("/", dependencies=[Depends(auth.implicit_scheme)], response_model=models.full.ItemFull)
async def create_item(item: models.edit.ItemEdit,
                      current_user: tables.User = fastapi.Depends(deps.dep_admin),
                      session: Session = fastapi.Depends(deps.dep_session)
                      ):
    # Add data retrieval from steam to populate the data json column.
    return crud.quick_create(session, tables.Item(name=item.name, giveaway_id=item.giveaway_id,
                                                  obtain_action=item.obtain_action))


@router.patch("/{item_id}", dependencies=[Depends(auth.implicit_scheme)], response_model=models.full.ItemFull)
async def edit_item(item_new: models.edit.ItemEdit,
                    current_user: tables.User = fastapi.Depends(deps.dep_admin),
                    item: tables.Item = fastapi.Depends(deps.dep_item),
                    session: Session = fastapi.Depends(deps.dep_session)
                    ):
    try:
        return crud.quick_update(session, item, item_new)
    except sqlalchemy.exc.IntegrityError:
        raise ResourceNotFound

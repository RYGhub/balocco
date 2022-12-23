import datetime
import random

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
    prefix="/api/giveaway/v1",
    tags=["Giveaway v1"]
)


@router.get("/", dependencies=[Depends(auth.implicit_scheme)], response_model=typing.List[models.read.GiveawayRead])
async def list_giveaways(
        current_user: tables.User = fastapi.Depends(deps.dep_user),
        giveaways: tables.Giveaway = fastapi.Depends(deps.dep_giveaways)):
    return giveaways


@router.get("/{giveaway_id}", dependencies=[Depends(auth.implicit_scheme)], response_model=models.full.GiveawayFull)
async def get_giveaway(
        giveaway: tables.Giveaway = fastapi.Depends(deps.dep_giveaway),
        current_user: tables.User = fastapi.Depends(deps.dep_user)):
    return giveaway


@router.post("/", dependencies=[Depends(auth.implicit_scheme)], response_model=models.full.GiveawayFull)
async def create_giveaway(giveaway: models.edit.GiveawayEdit,
                          current_user: tables.User = fastapi.Depends(deps.dep_admin),
                          session: Session = fastapi.Depends(deps.dep_session)
                          ):
    return crud.quick_create(session, tables.Giveaway(name=giveaway.name, description=giveaway.description,
                                                      closing_date=giveaway.closing_date,
                                                      assignment_date=giveaway.assignment_date,
                                                      issuer_id=current_user.id))


@router.patch("/{giveaway_id}", dependencies=[Depends(auth.implicit_scheme)], response_model=models.full.GiveawayFull)
async def edit_giveaway(giveaway_new: models.edit.GiveawayEdit,
                        current_user: tables.User = fastapi.Depends(deps.dep_admin),
                        giveaway: tables.Giveaway = fastapi.Depends(deps.dep_giveaway),
                        session: Session = fastapi.Depends(deps.dep_session)
                        ):
    return crud.quick_update(session, giveaway, giveaway_new)


@router.patch("/close/{giveaway_id}", dependencies=[Depends(auth.implicit_scheme)],
              response_model=models.full.GiveawayFull)
async def close_giveaway(giveaway: tables.Giveaway = fastapi.Depends(deps.dep_giveaway),
                         current_user: tables.User = fastapi.Depends(deps.dep_admin),
                         session: Session = fastapi.Depends(deps.dep_session)):
    giveaway.active = False
    giveaway.closing_date = datetime.datetime.now()
    session.commit()
    return giveaway


@router.patch("/join/{giveaway_id}", dependencies=[Depends(auth.implicit_scheme)],
              response_model=models.full.GiveawayFull)
async def join_giveaway(giveaway: tables.Giveaway = fastapi.Depends(deps.dep_giveaway),
                        current_user: tables.User = fastapi.Depends(deps.dep_user),
                        session: Session = fastapi.Depends(deps.dep_session)):
    time = datetime.datetime.now()
    if time > giveaway.closing_date:
        raise ResourceNotFound
    try:
        crud.quick_create(session, tables.Signup(user_id=current_user.id, giveaway_id=giveaway.id))
    except sqlalchemy.exc.IntegrityError:
        raise CompulsiveJoin
    return giveaway


@router.put("/provide/{giveaway_id}", dependencies=[Depends(auth.implicit_scheme)],
            response_model=models.full.GiveawayFull)
async def provide_items(giveaway: tables.Giveaway = fastapi.Depends(deps.dep_giveaway),
                        current_user: tables.User = fastapi.Depends(deps.dep_admin),
                        session: Session = fastapi.Depends(deps.dep_session)):
    if not giveaway.active:
        raise ResourceNotFound
    subscribed_users: list[tables.User] = [entry.user for entry in giveaway.signups]
    random.shuffle(subscribed_users)
    items: list[tables.Item] = [item for item in giveaway.items if item.obtainable]
    random.shuffle(items)
    max_val = len(subscribed_users)
    mode = "users"
    if max_val > len(items):
        mode = "items"
        max_val = len(items)
    j = 0
    for i in range(0, max_val, 1):
        if mode == "items":
            items[i].winner_id = subscribed_users[j].id
            items[i].obtainable = False
            j += 1
        else:
            items[j].winner_id = subscribed_users[i].id
            items[j].obtainable = False
            j += 1
        session.commit()
    return giveaway

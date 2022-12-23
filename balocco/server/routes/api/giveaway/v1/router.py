import datetime
import random
import dataclasses

import sqlalchemy.exc
import sortedcontainers
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


@dataclasses.dataclass
class GiveawayPartecipant:
    """
    An user currently being tracked in a giveaway.
    """

    user: tables.User
    """The :class:`.tables.User` itself."""
    
    current_value: int
    """The total value of the items the user has received so far."""

    seed: float
    """A random value used to resolve ties."""


@router.put("/provide/{giveaway_id}", dependencies=[Depends(auth.implicit_scheme)],
            response_model=models.full.GiveawayFull)
async def provide_items(giveaway: tables.Giveaway = fastapi.Depends(deps.dep_giveaway),
                        current_user: tables.User = fastapi.Depends(deps.dep_admin),
                        session: Session = fastapi.Depends(deps.dep_session)):

    items = sortedcontainers.SortedList(
        [item for item in giveaway.items if item.obtainable], 
        key=lambda i: -i.value
    )
    """:class:`list` of items which can be obtained from the giveaway, always ordered by descending :attr:`.tables.Item.value`."""

    partecipants = sortedcontainers.SortedList(
        [
            GiveawayPartecipant(
                user=entry.user,
                current_value=0,
                seed=random.random(),
            )
            for entry in giveaway.signups
        ],
        key=lambda gp: gp.current_value + gp.seed
    )
    """:class:`list` of :class:`.GiveawayPartecipant`s, always sorted by ascending :attr:`.GiveawayPartecipants.current_value` and :attr:`.GiveawayPartecipants.seed`."""

    # Continue until everything has been given away
    while items:
        # Pop the highest-value item
        item: tables.Item = items.pop(0)
        # Pick the lowest-value user
        user: GiveawayPartecipant = partecipants.pop(0)
        # It's a match!
        user.current_value += item.value
        item.winner = user.user
        item.obtainable = False
        # Readd the user to the partecipants
        partecipants.add(user)

    session.commit()

    return giveaway

import datetime
import json
import os

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
import requests

router = fastapi.routing.APIRouter(
    prefix="/api/item/v1",
    tags=["Item v1"]
)


@router.get("/{item_id}", dependencies=[Depends(auth.implicit_scheme)], response_model=models.full.ItemFull)
async def get_item(
        item: tables.Giveaway = fastapi.Depends(deps.dep_item_weaker),
        current_user: tables.User = fastapi.Depends(deps.dep_user)):
    return item


@router.post("/", dependencies=[Depends(auth.implicit_scheme)], response_model=models.full.ItemFull)
async def create_item(item: models.edit.ItemEdit,
                      current_user: tables.User = fastapi.Depends(deps.dep_admin),
                      session: Session = fastapi.Depends(deps.dep_session)
                      ):
    # Add data retrieval from steam to populate the data json column.
    return crud.quick_create(session, tables.Item(name=item.name, giveaway_id=item.giveaway_id,
                                                  obtain_action=item.obtain_action, data=item.data))


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


@router.patch("/take/{item_id}", dependencies=[Depends(auth.implicit_scheme)], response_model=models.full.ItemObtain)
async def take_item(current_user: tables.User = fastapi.Depends(deps.dep_user),
                    item: tables.Item = fastapi.Depends(deps.dep_item),
                    session: Session = fastapi.Depends(deps.dep_session)
                    ):
    item.taken = True
    session.commit()
    return item


@router.patch("/send/{item_id}", dependencies=[Depends(auth.implicit_scheme)], response_model=models.full.ItemFull)
async def send_item(exchange: models.edit.Exchange,
                    current_user: tables.User = fastapi.Depends(deps.dep_user),
                    item: tables.Item = fastapi.Depends(deps.dep_item),
                    session: Session = fastapi.Depends(deps.dep_session)
                    ):
    if item.taken:
        raise ResourceNotFound
    new_winner = crud.quick_retrieve(session, tables.User, id=exchange.user_id)
    item.winner_id = new_winner.id
    session.commit()
    return item


@router.get("/steam/{appid}", dependencies=[Depends(auth.implicit_scheme)], response_model=models.edit.SteamData)
async def get_steam_data(appid: str, current_user: tables.User = fastapi.Depends(deps.dep_user)):
    data = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}&l=english",
                        headers={"Content-Type": "application/json"})
    if data.status_code == 200:
        return models.edit.SteamData(data=json.loads(data.text))
    raise ResourceNotFound



def get_itad_lowest(appid: int) -> float:
    """
    Get the lowest price a game has ever been from the `IsThereAnyDeal API <https://itad.docs.apiary.io/>`_.

    Returned price is in cents (``249`` for 2.49 €).
    """

    itad_api_key = os.environ["BALOCCO_ITAD_KEY"]

    r = requests.get(f"https://api.isthereanydeal.com/v02/game/plain/", params=dict(
        key=itad_api_key,
        shop="steam",
        game_id=f"app/{appid}",
    ))
    r.raise_for_status()
    r = r.json()
    
    app_plain: str = r["data"]["plain"]

    r = requests.get(f"https://api.isthereanydeal.com/v01/game/lowest/", params=dict(
        key=itad_api_key,
        plains=app_plain,
        region="eu1",
        country="IT",
    ))
    r.raise_for_status()
    r = r.json()

    lowest: float = r["data"][app_plain]["price"]

    return int(lowest * 100)

import json
from uuid import UUID

import fastapi
from fastapi import Security
from fastapi_auth0 import Auth0User
from balocco.database import tables, engine
from balocco.server import crud
from balocco.server.deps.database import dep_session
from balocco.server.errors import InvalidCredentials, ResourceNotFound
from balocco.server.authentication import auth

__all__ = (
    "dep_user",
    "dep_admin",
)


def dep_user(
        session: engine.Session = fastapi.Depends(dep_session),
        user: Auth0User = Security(auth.get_user)
):
    try:
        email: str = user.email
        if email is None:
            raise InvalidCredentials
    except Exception as e:
        raise InvalidCredentials
    try:
        user_db = crud.quick_retrieve(session, tables.User, email=user.email)
        return user_db
    except ResourceNotFound:
        first = False
        try:
            crud.quick_retrieve(session, tables.User)
        except ResourceNotFound:
            first = True
        user_db = tables.User(username=user.email, email=user.email)
        crud.quick_create(session, user_db)
        if first:
            server = session.query(tables.Server).first()
            if not server:
                crud.quick_create(session, tables.Server(name="Unconfigured OpenDictionary Server",
                                                         motd="As an administrator, please configure me.",
                                                         logo_uri="", custom_colors=json.dumps({}),
                                                         admin_id=user_db.id))
            else:
                server.admin_id = user_db.id
                session.commit()
                session.refresh(server)
        return user_db


def dep_admin(
        user: tables.User = fastapi.Depends(dep_user)
):
    if not user.admin_of:
        raise InvalidCredentials
    return user

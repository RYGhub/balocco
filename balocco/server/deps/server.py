import json
from balocco.database import tables, engine
from balocco.server import crud
from balocco.server.deps.database import dep_session
from balocco.server.errors import ResourceNotFound
import fastapi

__all__ = (
    "dep_server",
)


def dep_server(session: engine.Session = fastapi.Depends(dep_session)):
    try:
        server = crud.quick_retrieve(session, tables.Server)
    except ResourceNotFound:
        server = crud.quick_create(session, tables.Server(name="Unconfigured Balocco Server",
                                                          motd="As an administrator, please configure me.",
                                                          logo_uri="", custom_colors=json.dumps({})))
    return server

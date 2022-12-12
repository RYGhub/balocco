import pathlib
import fastapi
import pkg_resources
import sqlalchemy.exc
from starlette.middleware.cors import CORSMiddleware

from balocco.server.errors import ApiException
from balocco.server.handlers import handle_api_error, handle_sqlalchemy_not_found, \
    handle_sqlalchemy_multiple_results, handle_generic_error
from balocco.server.routes.api.users.v1.router import router as router_api_user_v1
from balocco.server.routes.api.server.v1.router import router as router_api_server_v1
from balocco.server.routes.api.giveaway.v1.router import router as router_api_giveaway_v1
from balocco.server.routes.api.item.v1.router import router as router_api_item_v1
from fastapi_pagination import add_pagination

with open(pathlib.Path(__file__).parent.joinpath("description.md")) as file:
    description = file.read()

app = fastapi.FastAPI(
    debug=__debug__,
    title="Balocco",
    description=description,
    version="0.1",
)

origins = ["https://balocco-navi.fermitech.info"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_api_user_v1)
app.include_router(router_api_server_v1)
app.include_router(router_api_giveaway_v1)
app.include_router(router_api_item_v1)

app.add_exception_handler(ApiException, handle_api_error)
app.add_exception_handler(sqlalchemy.exc.NoResultFound, handle_sqlalchemy_not_found)
app.add_exception_handler(sqlalchemy.exc.MultipleResultsFound, handle_sqlalchemy_multiple_results)
app.add_exception_handler(Exception, handle_generic_error)

add_pagination(app)

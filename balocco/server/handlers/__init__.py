import typing as t

import fastapi
import sqlalchemy.exc

from balocco.server import errors


# noinspection PyUnusedLocal
async def handle_api_error(request: fastapi.Request, exc: errors.ApiException) -> fastapi.Response:
    return exc.to_response()


# noinspection PyUnusedLocal
async def handle_sqlalchemy_not_found(request: fastapi.Request, exc: sqlalchemy.exc.NoResultFound) -> t.NoReturn:
    raise errors.ResourceNotFound()


# noinspection PyUnusedLocal
async def handle_sqlalchemy_multiple_results(request: fastapi.Request, exc: sqlalchemy.exc.MultipleResultsFound) -> t.NoReturn:
    raise errors.MultipleResultsFound()


# noinspection PyUnusedLocal
async def handle_generic_error(request: fastapi.Request, exc: Exception) -> fastapi.Response:
    raise errors.ApiException()

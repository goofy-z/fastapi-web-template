import time
from fastapi import FastAPI
from starlette.requests import Request

from .fastapi_globals import GlobalsMiddleware, g
from .session import DbSessionMiddleware


def register_http_middleware(app: FastAPI):
    """
    add middleware
    """
    # use g.db for get sqla session
    app.add_middleware(DbSessionMiddleware)

    # the global object: g
    app.add_middleware(GlobalsMiddleware)

import sys
import uvloop
import asyncio
import logging
import uvicorn


from app.ws import create_ws_manager
from core.utils.api_exception import http_exception_handler, APIException
from core.config.common import config
from core.middleware import register_http_middleware
from core.storage import create_db
from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

sys.setrecursionlimit(1500)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def configure_models():
    """
    add model to sqla metadata
    """
    # +gencode:register-router


def register_router(app: FastAPI):
    """
    注册路由
    """
    # +gencode:register-router
    from app.ws.apis import router as ws_router

    app.include_router(ws_router, prefix="/wss")


def init_sync(app):
    register_http_middleware(app)
    register_router(app)
    configure_models()


def init_async():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # if cleanup: 'RuntimeError: There is no current event loop..'
        loop = None

    if loop and loop.is_running():
        loop.create_task(create_db())
        loop.create_task(create_ws_manager())


app = FastAPI(
    name=config.SERVICE_NAME,
    openapi_url="/v1/openapi/openapi.json",
    docs_url="/v1/openapi/docs",
    redoc_url="/v1/openapi/redoc",
    debug=not config.PROD,
    exception_handlers={APIException: http_exception_handler},
)


init_sync(app)
init_async()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="debug", debug=not config.PROD)

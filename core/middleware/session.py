from sqlalchemy.ext.asyncio import session
from starlette.types import ASGIApp, Receive, Scope, Send
from . import g
from core.storage import db


class DbSessionMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "lifespan":
            session = db.session()
            # add global session
            g.db = session

            # add sql log
            g.sql_log = []
            try:
                await self.app(scope, receive, send)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()
            finally:
                await session.close()
        else:
            await self.app(scope, receive, send)
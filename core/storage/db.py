import time

from sqlalchemy import orm, event, false
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine
from core.config.common import config
from .model import Base, HasPrivate


class SQLAlchemy(object):
    def __init__(self, database_url=None, echo=False):
        self.engine = None
        self.session = None

        if database_url:
            self.update_engine(database_url, echo)

    def update_engine(self, database_url, echo):
        self.engine = create_async_engine(
            database_url, echo=echo, pool_size=20, max_overflow=5, future=True, query_cache_size=1500  # 设置缓存sql条数
        )
        self.session = self.create_session()

    def create_session(self, options=None):
        return sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)


async def create_db(app=None, auto_create_table=config.DB_MIGRATION):
    db.update_engine(config.DATABASE_URL, echo=config.SHOW_SQL)
    print("db init success")
    if auto_create_table:
        async with db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # show_sql控制, 收集每一条执行sql记录存放到g对象里，最终会在接口返回报文里添加这些记录
    if config.RETURN_SQL:
        @event.listens_for(db.engine.sync_engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            conn.info.setdefault("query_start_time", []).append(time.time())

        @event.listens_for(db.engine.sync_engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            total = time.time() - conn.info["query_start_time"].pop(-1)
            tmp = [parameters] if not executemany else parameters
            from core.middleware import g
            for i in tmp:
                g.sql_log.append({"sql": (statement % i).replace("\n", ""), "duration": f"{int(total * 1000)} ms"})


@event.listens_for(Session, "do_orm_execute")
def _add_filtering_criteria(execute_state):
    """
    soft delete
    more detail: https://docs.sqlalchemy.org/en/14/_modules/examples/extending_query/filter_public.html
    """

    if (
        not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("include_private", False)
    ):
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(
                HasPrivate,
                lambda cls: cls.deleted == false(),
                include_aliases=True,
            )
        )


db = SQLAlchemy()

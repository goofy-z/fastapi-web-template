from datetime import datetime
import time
import logging
from sqlalchemy import Boolean, Column, orm, event, false
from sqlalchemy.orm.query import Query
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import update
from core.middleware import g

LOG = logging.getLogger(__name__)


class HasPrivate(object):
    """Mixin that identifies a class as having private entities"""

    deleted = Column(Boolean, default=False, index=True)


class _Model(HasPrivate):
    """
    Base Model: 包含了 Model 的共有字段和方法
    """

    created_at = Column(DATETIME, nullable=False, default=lambda: datetime.now())
    updated_at = Column(DATETIME, nullable=False, default=lambda: datetime.now(), onupdate=lambda: datetime.now())
    deleted_at = Column(DATETIME, nullable=False, default=lambda: datetime.now())
    # deleted = Column(Boolean, default=False, index=True)

    async def delete(self):
        """
        soft delte
        """
        await g.db.execute(
            update(self.__class__)
            .where(self.__class__.id == self.id)
            .values({"deleted": True, "deleted_at": datetime.now()})
            .execution_options(synchronize_session="evaluate")
        )


Base = declarative_base(cls=_Model, name="Model")

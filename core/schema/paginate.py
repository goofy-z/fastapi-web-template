from typing import Any, Optional
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func


async def paginate_handler(
    page: int,
    limit: int,
    data: Optional[Any] = None,
    db: Optional[Session] = None,
    stmt: Optional[select] = None,
    total: Optional[int] = None,
):
    """
    数据分页
    """
    if page > 0:
        offset = (page - 1) * limit
    else:
        page = 1
        offset = 0
    if db and select:
        res = await db.execute(stmt.offset(offset).limit(limit))
        res = res.scalars().all()
        res_total = total or await db.scalar(select(func.count()).select_from(stmt))
    else:
        res = data[offset : offset + limit]
        res_total = total or len(data)

    return {
        "total_count": res_total,
        "current_page": page,
        "total_page": (res_total // limit) or 1,
        "data": res,
    }

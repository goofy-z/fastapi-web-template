import logging
import asyncio

from fastapi import Request


async def base(request: Request):
    """
    基础依赖，你可以当作钩子函数来处理
    如果需要扩展其他的dependen，需要注意调用顺序
    另外你需要知道的一点是，fastapi中 dependencies如果是非异步函数则会用线程池进行处理
    - 1. 在线程池里contextvar的修改将不起作用
    """
    from core.middleware.fastapi_globals import g

    lang = request.headers.get("Accept-Language")
    if lang:
        g.locale = lang.split(",")[0]
    else:
        g.locale = "zh-CN"

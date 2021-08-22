import random
import hashlib

from typing import Optional
from fastapi import WebSocket
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect
from app.ws.schema import BroadcastMsgReq


from app.ws import manager
from app.ws.ws import html


async def ws_view(
    websocket: WebSocket, client_id: int, session: Optional[str] = "qeqe", transport: Optional[str] = "websocket"
):
    """
    websocket服务
    """
    res = await manager.connect_with_token(websocket)
    if not res:
        return
    try:
        while True:
            await manager.receive_json(websocket)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


async def test_html_view():
    """
    测试html
    """
    return HTMLResponse(html)


async def sockjs_info_view(t: Optional[int]):
    """
    伪造sockjs的info接口
    """
    data = {
        "entropy": random.randint(1, 2147483647),
    }
    return data


async def broadcast_msg_view(req: BroadcastMsgReq):
    """
    广播消息
    """
    msg = req.msg
    await manager.broadcast(req.msg)
    return "success"

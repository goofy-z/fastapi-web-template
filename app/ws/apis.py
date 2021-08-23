from app.ws.schema import SockJSInfoRes
from fastapi.applications import FastAPI
from app.ws.views import broadcast_msg_view, ws_view, test_html_view
from fastapi import APIRouter


router = APIRouter(tags=["websocket"])

router.add_api_websocket_route(
    name="websocket连接",
    path="/{client_id}/{session}/{transport}",
    endpoint=ws_view,
)


router.add_api_route(
    name="websocket测试",
    path="/test.html",
    endpoint=test_html_view,
)


router.add_api_route(name="群推消息", path="/wss/broadcast_msg", methods=["POST"], endpoint=broadcast_msg_view)

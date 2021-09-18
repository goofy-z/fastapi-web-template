import json
import logging

import jwt
import asyncio
from typing import Dict, List
from datetime import datetime, timedelta

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(debug=True)

LOG = logging.getLogger(__name__)

class ConnectionManager:
    _hb_handle = None  # heartbeat event loop timer
    _hb_task = None  # gc task

    def __init__(self):
        self.active_connections: Dict[List[WebSocket]] = []
        self.heartbeat = 10

    async def connect(self, session: WebSocket):
        await session.accept()
        self.active_connections.append(session)

    async def connect_with_token(self, session: WebSocket):
        """
        需要token创建ws连接
        """
        await session.accept()
        # 恢复一条消息代表接收到请求
        await self.send_personal_message("o", session)

        # 初始化连接时加上心跳检查时间
        self.flush_session_expire_time(session)

        # if self._hb_task:
        #     print(self._hb_task.result())
        self.active_connections.append(session)

        # 第一次消息必须发送token过来
        try:
            token = await session.receive_json()
            if isinstance(token, list):
                token = json.loads(token[0])
            elif not isinstance(token, dict):
                token = json.loads(token)
        except WebSocketDisconnect:
            return
        except Exception as e:
            await self.send_personal_message(f"token error", session)
            await self.disconnect(session)
            return False

        if token.get("Op") == "bind":
            try:
                sessionID = token.get("SessionID")
                payload = jwt.decode(
                    sessionID.encode("utf-8"), "31e37738-559a-47f3-8b16-5fa27a2ed410", algorithms="HS256"
                )
                user_id = payload.get("user_id")
                setattr(session, "user_id", user_id)
                # 再次刷新失效时间
                self.flush_session_expire_time(session)
                # 发送一条消息回应token验证成功
                await self.send_personal_message('a[{"result":"success"}]', session)
                return True
            except:
                await self.send_personal_message(f"You token is inviled", session)
                await self.disconnect(session)
        else:
            await self.send_personal_message(f"need token", session)
            await self.disconnect(session)

    async def receive_json(self, session: WebSocket):
        """
        获取json格式的websocket数据
        """
        res = await session.receive_json()
        self.flush_session_expire_time(session)
        return res

    async def send_personal_message(self, message: str, session: WebSocket):
        await session.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            msg = "a" + json.dumps([message])
            await connection.send_text(msg)

    def start(self):
        # logging.info("start manager")
        if not self._hb_handle:
            loop = asyncio.get_running_loop()
            self._hb_handle = loop.call_later(self.heartbeat, self._heartbeat)

    def stop(self):
        if self._hb_handle is not None:
            self._hb_handle.cancel()
            self._hb_handle = None
        if self._hb_task is not None:
            self._hb_task.cancel()
            self._hb_task = None

    async def disconnect(self, session: WebSocket):
        """
        关闭连接
        """
        await session.close()
        self.remove_session(session)

    def remove_session(self, session):
        """
        移除缓存的session
        """
        if session in self.active_connections:
            LOG.info(f"session close {self.get_session_id(session)}")
            self.active_connections.remove(session)

    def _heartbeat(self):
        """
        启动定时task
        """
        if self._hb_task is None:
            loop = asyncio.get_running_loop()
            self._hb_task = loop.create_task(self._heartbeat_task())

    async def _heartbeat_task(self):
        """
        心跳检测
        """
        sessions = self.active_connections
        if sessions:
            now = datetime.now()

            idx = 0
            while idx < len(sessions):
                session = sessions[idx]
                if session.expire_time < now:
                    session_id = self.get_session_id(session)
                    # 删除超时session
                    try:
                        await self.send_personal_message("h time out", session)
                        logging.warn(f"heart beat check timeout {session_id}")
                        await self.disconnect(session)
                    except Exception as e:
                        LOG.info(f"session {session_id} check failed {str(e)}")
                    continue
                # 没有超时的设置下次超时时间, 但是索引不变
                await self.send_personal_message("h[]", session)
                idx += 1

        self._hb_task = None
        loop = asyncio.get_running_loop()
        self._hb_handle = loop.call_later(self.heartbeat, self._heartbeat)

    def flush_session_expire_time(self, session: WebSocket):
        """
        刷新session的过期时间
        """
        setattr(session, "expire_time", datetime.now() + timedelta(seconds=self.heartbeat))

    def get_session_id(self, session):
        """
        提取session的id
        """
        if hasattr(session, "user_id"):
            session_id = session.user_id
        else:
            session_id = session.url
        return session_id


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8080/wss/${client_id}/dada/dadda`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


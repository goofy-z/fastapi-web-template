import asyncio

from app.ws.ws import ConnectionManager

manager = ConnectionManager()


async def create_ws_manager():
    manager.start()

from typing import List, Optional

from pydantic.fields import Field
from core.schema import BaseSchema


class SockJSInfoRes(BaseSchema):
    cookie_needed: bool = False
    entropy: int
    origins: List[str] = ["*:*"]
    websocket: bool = True


class BroadcastMsgReq(BaseSchema):
    msg: str = Field(description="推送消息内容")

import jwt

from fastapi import Header
from starlette.responses import JSONResponse

from core.config.common import config
from core.middleware import g


async def auth(Authorization: str = Header(...)):
    """
    接口认证依赖，这个是和base依赖分隔的，你得注意先后顺序
    """
    header_type = "Bearer"
    header_name = "Authorization"
    algorithms = "HS256"
    # 只支持从header中获取jwt token, 存在token，将解析并设置user_id
    auth = Authorization
    if not auth:
        msg = "Need Header Authorization".format(header_name, header_type)
        JSONResponse({"error_info": msg, "error_type": "auth_error"}, status_code=401)
    parts = auth.split()
    if len(parts) != 2 or parts[0] != header_type:
        msg = "Bad {} header. Expected value '{} <JWT>'".format(header_name, header_type)
        return JSONResponse({"error_info": msg, "error_type": "auth_error"}, status_code=401)
    try:
        payload = jwt.decode(parts[1], config.TOKEN_SECRET_KEY, algorithms=algorithms)
    except Exception as e:
        msg = f"Bad token {str(e)}"
        return JSONResponse({"error_info": msg, "error_type": "auth_error"}, status_code=401)
    # TODO check user_id 
    g.user_id = payload.get("user_id")

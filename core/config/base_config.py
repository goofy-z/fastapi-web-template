import os


def str2bool(v):
    if v is None or isinstance(v, bool):
        return v
    return v.lower() in ("yes", "true", "t", "1")


def str2int(v):
    if v is None:
        return v
    if v == "":
        return None
    return int(v)


def str2float(v):
    if v is None:
        return v
    return int(v)


class Base:
    # ------------------- need config ---------------------
    DATABASE_MYSQL_URL = os.getenv("DATABASE_MYSQL_URL", "root:dangerous@127.0.0.1:3600/kongtianbei")

    # ------------------- option ---------------------
    CONFIG_NAME = "BASE"
    SERVICE_NAME = os.getenv("SERVICE_NAME", "fastapi-web-template")

    TZ = os.getenv("TZ", "Asia/Shanghai")

    TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY", "token_secret_key")

    # db
    DATABASE_URL = os.getenv("DATABASE_URL", f"mysql+aiomysql://{DATABASE_MYSQL_URL}?charset=utf8mb4")
    SHOW_SQL = str2bool(os.getenv("SHOW_SQL", "False"))
    RETURN_SQL = str2bool(os.getenv("RETURN_SQL", "True"))
    DATABASE_URL_ENCODING = os.getenv("DATABASE_URL_ENCODING", "utf8mb4")

    DB_POOL_RECYCLE = str2int(os.getenv("DB_POOL_RECYCLE", 3600))
    DB_MAX_OVERFLOW = str2int(os.getenv("DB_MAX_OVERFLOW", 20))
    DB_POOL_SIZE = str2int(os.getenv("DB_POOL_SIZE", 5))

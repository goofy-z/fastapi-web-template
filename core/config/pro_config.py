import os

from .base_config import Base, str2bool


class ProdConfig(Base):
    CONFIG_NAME = "PROD"
    
    PROD = str2bool(os.getenv("PROD", "False"))

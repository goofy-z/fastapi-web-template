from fastapi import Depends
from .auth import auth
from .base import base

auth_dependen = Depends(auth)
base_dependen = Depends(base)

import decimal
import datetime

from typing import Any, Optional, Generic, List
from pydantic import BaseModel, create_model
from pydantic.fields import Field, T
from pydantic.main import BaseConfig
from pydantic.generics import GenericModel


class SchemaConfig(BaseConfig):
    ...
    orm_mode = True
    json_encoders = {
        datetime: lambda v: v.timestamp() * 1000,
        decimal.Decimal: lambda v: float(v),
    }


class BaseSchema(BaseModel):
    __config__ = SchemaConfig


class DataSchema(GenericModel, Generic[T]):
    """普通json序列化器"""

    data: T


class PageSchema(GenericModel, Generic[T]):
    """分页序列化器"""

    data: List[T]
    total_count: int = Field(..., description="总条数")
    total_page: int = Field(..., description="总页数")
    current_page: int = Field(..., description="当前页")

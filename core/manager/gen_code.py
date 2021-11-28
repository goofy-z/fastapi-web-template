import shutil
import os
import sys

from .base import CommandBase, str2camel


apis_file = """
from fastapi import APIRouter

from core.dependencies import base_dependen
from core.schema.base import DataSchema, PageSchema
from app.{app_name}.views import list_{app_name}_view, create_{app_name}_view, delete_{app_name}_view
from app.{app_name}.schema import {AppName}ListRes


router = APIRouter(prefix="/v1/{app_name}", tags=["{app_name} project"])

router.add_api_route(
    name="list {app_name}",
    path="/",
    endpoint=list_{app_name}_view,
    methods=["GET"],
    response_model=PageSchema[{AppName}ListRes],
    dependencies=[base_dependen,]
)

router.add_api_route(
    name="create {app_name}",
    path="/",
    endpoint=create_{app_name}_view,
    methods=["POST"],
    dependencies=[base_dependen,]
)

router.add_api_route(
    name="delete {app_name}",
    path="/",
    endpoint=delete_{app_name}_view,
    methods=["DELETE"],
    dependencies=[base_dependen,]
)
"""

schema_file = """
from typing import List, Optional
from core.schema import BaseSchema
from pydantic.fields import Field


class {AppName}ListRes(BaseSchema):
    id: Optional[str] = Field(description="id")
    name: Optional[str] = Field(description="名称")
    description: Optional[str] = Field(description="描述")

class {AppName}CreateReq(BaseSchema):
    name: Optional[str] = Field(description="名称")
    description: Optional[str] = Field(description="描述")

"""

views_file = """
from typing import Any, Optional
from app.{app_name}.{app_name} import list_{app_name}, create_{app_name}, delete_{app_name}
from app.{app_name}.schema import {AppName}CreateReq


async def list_{app_name}_view(
    page: Optional[int] = 1,
    limit: Optional[int] = 10,
):
    return await list_{app_name}(page, limit)

async def create_{app_name}_view(item: {AppName}CreateReq):
    await create_{app_name}(item.name, item.description)
    return {{"data": "success"}}

async def delete_{app_name}_view(record_id: str):
    await delete_{app_name}(record_id)
    return {{"data": "success"}}

"""

app_util_file = """
from sqlalchemy import select, insert
from core.middleware import g
from core.schema import paginate_handler
from core.utils.api_exception import NotFoundException
from core.i18n import gettext
from app.{app_name}.models import {AppName}


async def list_{app_name}(page: int, limit: int):
    stmt = select({AppName})
    return await paginate_handler(page=page, limit=limit, db=g.db, stmt=stmt)

async def create_{app_name}(name: str, description: str):
    return await g.db.execute(insert({AppName}).values({{"name": name, "description": description}}))

async def delete_{app_name}(record_id: str):
    obj = await g.db.get({AppName}, record_id)
    if not obj:
        raise NotFoundException(gettext("record not found"))
    await obj.delete()
    return

"""

model_file = """
import uuid

from core.storage import Base
from sqlalchemy import Column, String


class {AppName}(Base):
    __tablename__ = "{app_name}"
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(128), nullable=False)
    description = Column(String(512), nullable=False)

"""


class StartAppCommand(CommandBase):
    """
    自动生成标准模块代码
    """

    # the command
    command_str = "startapp"

    # command description
    command_desc = ["[app_name]: 自动生成app名称为[app_name]标准模块代码"]

    # default app name is 'demo'
    app_name = "demo"

    # the app module root dir
    root = "./app"

    # copyright
    copyright_str = ""

    @classmethod
    def execute(cls, app_name):
        cls.app_name = app_name
        cls.init_dir()
        cls.add_apis_file()
        cls.add_app_util_file()
        cls.add_model_file()
        cls.add_scheme_file()
        cls.add_view_file()
        cls.runner_file_handler()
        print("create app ' %s ' success" % app_name)

    @classmethod
    def init_dir(cls):
        """
        create app module dir
        """
        cls.root = os.path.join(cls.root, cls.app_name)
        if os.path.exists(cls.root):
            sys.stderr.write(f"app {cls.app_name} already exists")
            sys.exit(1)
        os.makedirs(cls.root)
        with open(os.path.join(cls.root, "__init__.py"), "w") as f:
            f.write(cls.copyright_str)

    @classmethod
    def add_apis_file(cls):
        """
        创建目录和init文件
        """
        api_file_path = os.path.join(cls.root, f"apis.py")
        with open(api_file_path, "w") as f:
            f.write(cls.copyright_str)
            f.write(apis_file.format(AppName=str2camel(cls.app_name), app_name=cls.app_name))

    @classmethod
    def add_model_file(cls):
        """
        创建模型文件
        """
        api_file_path = os.path.join(cls.root, "models.py")
        with open(api_file_path, "w") as f:
            f.write(cls.copyright_str)
            f.write(model_file.format(AppName=str2camel(cls.app_name), app_name=cls.app_name))

    @classmethod
    def add_scheme_file(cls):
        """
        创建schema文件
        """
        api_file_path = os.path.join(cls.root, "schema.py")
        with open(api_file_path, "w") as f:
            f.write(cls.copyright_str)
            f.write(schema_file.format(AppName=str2camel(cls.app_name), app_name=cls.app_name))

    @classmethod
    def add_view_file(cls):
        """
        创建view文件
        """
        api_file_path = os.path.join(cls.root, f"views.py")
        with open(api_file_path, "w") as f:
            f.write(cls.copyright_str)
            f.write(views_file.format(AppName=str2camel(cls.app_name), app_name=cls.app_name))

    @classmethod
    def add_app_util_file(cls):
        """
        创建controller文件
        """
        api_file_path = os.path.join(cls.root, f"{cls.app_name}.py")
        with open(api_file_path, "w") as f:
            f.write(cls.copyright_str)
            f.write(app_util_file.format(AppName=str2camel(cls.app_name), app_name=cls.app_name))

    @classmethod
    def runner_file_handler(cls):
        """
        register router and configure sqla model
        """
        new_c = []
        with open("main.py", "r+") as f:
            f.seek(0)
            while True:
                c = f.readline()
                new_c.append(c)
                if c == "":
                    break
                elif "+gencode:register-router" in c:
                    new_c.append(f"    from app.{cls.app_name}.apis import router as {cls.app_name}_router\n")
                    new_c.append(f"    app.include_router({cls.app_name}_router)\n\n")
                elif "+gencode:configure-model" in c:
                    new_c.append(f"    # noinspection PyUnresolvedReferences\n")
                    new_c.append(f"    from app.{cls.app_name} import models\n\n")

        with open("main.py", "w") as f:
            f.writelines(new_c)

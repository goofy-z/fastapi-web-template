##简介

这是一个`fastapi`的脚手架项目，解释器版本至少是python3.7 +，项目集成了`sqlalchemy2(1.4+)`、`JWT Auth`、`websocket`、`i18n`等常用功能，项目的目录结构也比较简单，也封装了一系列的web开发过程中会用到的工具，欢迎大家给项目提提建议。

###目录结构：

```
.
├── app  # 业务应用目录，下属多个应用模块
│   ├── __init__.py
│   ├── demo  # 应用模块demo
│   │   ├── apis.py  # 路由定义
│   │   ├── demo.py  # 模块工具方法定义
│   │   ├── models.py  # ORM model类定义
│   │   ├── schema.py  # 序列化类定义
│   │   └── views.py  # 视图函数定义
│   └── ws  # websocket模块
├── core  # 项目核心
│   ├── config  # 项目配置文件
│   ├── dependencies  # fastapi依赖定义
│   ├── i18n  # 国际化翻译
│   ├── manager  # manager工具
│   ├── middleware  # ASGI中间件定义
│   ├── schema  # 基础schema
│   ├── storage  # SQLA相关
│   └── utils  # 工具目录
├── docs  # 项目文档
├── app.py  # 入口文件
├── manage.py  # manager工具
├── Dockerfile  # 就是一个DOckerfile
├── README.md
└── requirements.txt  # 依赖文件
```



###主要功能：

#### 1. SQLAlchemy

`1.4+`的版本，这个版本支持异步IO调用，但是相应的得使用异步的数据库适配器，这里使用的是`aiomysql`, 同时1.4版本已经支持SQLA的2.0写法，当然也是兼容旧版写法的。[两者区别具体查看文档](https://docs.sqlalchemy.org/en/14/changelog/migration_20.html)

与SQLA相关的代码在`/core/storage`下：

- `model.py`: 定义了ORM表结构映射基础对象`Base`， 集成它来关联db中的表。
- `db.py`: 初始化SQLA，添加一些监听事件。

应用代码中引入`session`可以直接从全局对象`g`中获取:

```shell
from core.middleware import g
g.db.execute(...)
```

获取`engine`对象

```
from core.storage import db
db.engine.execute(...)
```

#### 2.dependencies

项目下所有的fastapi依赖注入函数都在`/core/dependencies`：

- auth_dependen: 基础依赖注入，所有的AP都需要引入这个依赖，用于提取请求头中的`Accept-Language`来设置全局变量`local`, 用于`i18n`的翻译。
- auth_dependen: 基于`Authorization`请求头的JWT认证。

#### 3. config

项目的配置文件目录，分为两种环境配置文件`dev`和`prod`。启动项目时引入哪个配置文件取决于环境变量配置`CONFIG_NAME`，默认是`dev`。

已有配置：

- CONFIG_NAME： 引入配置文件类型
- SERVICE_NAME：项目名称
- TZ：时区
- TOKEN_SECRET_KEY：JWT密钥
- DATABASE_MYSQL_URL：数据库DSN
- SHOW_SQL：是否打开SQLA日志
- RETURN_SQL：是否在接口返回SQL记录
- DB_POOL_RECYCLE：数据库连接释放事件
- DB_MAX_OVERFLOW：连接池缓冲个数
- DB_POOL_SIZE： 连接池大小

#### 4. schema

项目的序列化和反序列化是基于pydantic实现的，业务应用需要继承`BaseSchema`来扩展各自需要的序列化器。提供两种序列化器：

- DataSchema： 普通序列化器
- PageSchema： 分页序列化器

还提供了数据分页器：`paginate_handler`，可以接收`select`对象或迭代对象，返回分页后的数据字典。

#### 5. i18n

创建翻译文件在后面的`manager.py`里会有介绍，如果是已有的翻译文件直接放入`/core/i18n/lang`里。同时，项目里需要使用翻译的地方可以如下使用，具体翻译成何种语言取决于全局变量`g.locale`

```python
from core.i18n import gettext
t = gettext("test") # t为翻译后的内容
```

#### 6. manager.py

项目下有一个类似`django`的项目管理工具，现在提供了两个命令：

1. startapp [appname]

   在`/app`下创建一个标准的应用目录，且实现了一套增删改查的代码

2. babel [add|run]

   **add**: 检测代码中的引入了`gettext`的地方，并更新翻译文件`message.po`

   **run**: 编译message.po。

#### 7. middleware

项目下的`/core/middleware`是所有的ASGI的中间件，目前共有两个中间件

- `fastapi-globals.py`： `g`对象的实现，基于contextvar实现
- `session.py`: 注册全局`session`

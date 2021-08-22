import gettext
import logging
import os

from babel.support import Translations
from starlette.datastructures import Headers

TRANSLATIONS = {
    # 获取当前文件所在目录，翻译文件就在当前目录下
    "zh-CN": Translations.load(os.path.split(os.path.realpath(__file__))[0], locales=["zh_CN"]),
    "en-US": Translations.load(os.path.split(os.path.realpath(__file__))[0], locales=["en_US"]),
}


translations = TRANSLATIONS.get("en_US")


def gettext(msg: str):
    from core.middleware.fastapi_globals import g

    t = TRANSLATIONS.get(g.locale) if g.locale else TRANSLATIONS.get("en_US")
    return t.ugettext(msg)

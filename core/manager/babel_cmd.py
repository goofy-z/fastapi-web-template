import shutil
import os
import sys

from .base import CommandBase, str2camel


class BabelCommand(CommandBase):
    """
    i18n翻译
    """

    # 命令
    command_str = "babel"
    # 命令描述
    command_desc = ["add: 生成翻译文件", "run: 编译翻译文件"]

    @classmethod
    def execute(cls, action):
        if action == "add":
            cls.add_babel()
        elif action == "run":
            cls.run_babel()

    @classmethod
    def add_babel(cls):
        """
        创建翻译文件
        """
        if os.system("pybabel extract -F core/i18n/babel.cfg -k gettext -o core/i18n/messages.pot ."):
            sys.stderr.write("生成messages.pot文件失败\n")
            sys.exit(1)
        # # 是否已经创建了翻译文件
        # if not os.path.exists("core/i18n/zh_CN"):
        #     if os.system("pybabel init -i core/i18n/messages.pot -d core/i18n/ -l zh_CN"):
        #         sys.stderr.write("生成翻译文件失败\n")
        #         sys.exit(1)
        if os.system("pybabel update -i core/i18n/messages.pot -d core/i18n/"):
            sys.stderr.write("更新翻译文件失败\n")
            sys.exit(1)
        sys.stdout.write("\n***************** ")
        sys.stdout.write("生成翻译文件成功，需要更新文件: core/i18n/zh_CN/LC_MESSAGES/messages.po")
        sys.stdout.write(" *****************\n")

    @classmethod
    def run_babel(cls):
        """
        编译翻译文件
        """
        if os.system("pybabel compile -d core/i18n/"):
            sys.stderr.write("生成messages.pot文件失败")
            sys.exit(1)
        sys.stdout.write("\n***************** ")
        sys.stdout.write("编译成功")
        sys.stdout.write(" *****************\n")
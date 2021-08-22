"""fast
项目管理工具
用法:
    python manage.py [command] [args]
创建app：
    描述：创建一个规范的app
    command: startapp
    args: app_name 模块名
创建i18n翻译：
    描述：通过flask-babel自动生成或编译翻译文件
    command: babel
    args:
        add: 添加翻译文件，之后需要手动去给翻译文件增加中文翻译
        run: 编译翻译文件
"""

import sys

from core.manager import ManagementUtility

# class FlaskBabelCommand(CommandBase):
#     """
#     i18n翻译
#     """

#     # 命令
#     command_str = "babel"
#     # 命令描述
#     command_desc = ["add: 生成翻译文件", "run: 编译翻译文件"]

#     @classmethod
#     def execute(cls, action):
#         if action == "add":
#             cls.add_babel()
#         elif action == "run":
#             cls.run_babel()

#     @classmethod
#     def add_babel(cls):
#         """
#         创建翻译文件
#         """
#         if os.system("pybabel extract -F static/i18n/babel.cfg -k lazy_gettext -o static/i18n/messages.pot ."):
#             sys.stderr.write("生成messages.pot文件失败\n")
#             sys.exit(1)
#         # 是否已经创建了翻译文件
#         if not os.path.exists("static/i18n/zh"):
#             if os.system("pybabel init -i static/i18n/messages.pot -d static/i18n/ -l zh_CN"):
#                 sys.stderr.write("生成翻译文件失败\n")
#                 sys.exit(1)
#         if os.system("pybabel update -i static/i18n/messages.pot -d static/i18n/"):
#             sys.stderr.write("更新翻译文件失败\n")
#             sys.exit(1)
#         sys.stdout.write("\n***************** ")
#         sys.stdout.write("生成翻译文件成功，需要更新文件: static/i18n/zh_CN/LC_MESSAGES/messages.po")
#         sys.stdout.write(" *****************\n")

#     @classmethod
#     def run_babel(cls):
#         """
#         编译翻译文件
#         """
#         if os.system("pybabel compile -d static/i18n/"):
#             sys.stderr.write("生成messages.pot文件失败")
#             sys.exit(1)
#         sys.stdout.write("\n***************** ")
#         sys.stdout.write("编译成功")
#         sys.stdout.write(" *****************\n")


def execute_from_command_line(argv=None):
    """
    创建管理工具实例，并执行命令
    """
    utility = ManagementUtility(argv)
    utility.execute()


if __name__ == "__main__":
    execute_from_command_line(sys.argv)

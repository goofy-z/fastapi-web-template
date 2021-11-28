import os
import sys

from .base import CommandBase


def registry_command():
    # noinspection PyUnresolvedReferences
    from .gen_code import StartAppCommand
    from .babel_cmd import BabelCommand


class ManagementUtility:
    """
    管理程序类
    """

    def __init__(self, argv=None):
        self.argv = argv
        # 项目名
        self.prog_name = os.path.basename(self.argv[0])

    def main_help_text(self):
        """
        帮助文档
        """
        desc = CommandBase.get_command_desc()
        out = "支持命令:\n"
        for k, v in desc.items():
            out = out + " " * 4 + k + ": "
            if isinstance(v, list):
                out += "\n" + "\n".join([" " * 8 + i for i in v]) + "\n"
            else:
                out += v + "\n"
        return out + "\n"

    def fetch_command(self, subcommand):
        commands = CommandBase.get_commands()
        try:
            return commands[subcommand]
        except KeyError:
            sys.stderr.write("Unknown command: %r\nType '%s help' for usage.\n" % (subcommand, self.prog_name))
            sys.exit(1)

    def execute(self):
        """
        执行command
        """
        try:
            command = self.argv[1]
        except IndexError:
            command = "help"
        if command == "help":
            sys.stdout.write(self.main_help_text())
            sys.exit(0)
        executor = self.fetch_command(command)
        executor(*self.argv[2:])


registry_command()

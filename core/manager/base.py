import os
import sys


class CommandMetaclass(type):
    registry_commands = dict()
    commands_desc = dict()

    def __new__(cls, name, bases, attrs):
        obj = type.__new__(cls, name, bases, attrs)
        if name == "CommandBase":
            return obj

        command_str = name
        command_desc = "..."
        executor = None
        for k, v in attrs.items():
            if k == "execute":
                executor = obj.execute
            # 指定命令名
            if k == "command_str":
                command_str = v
            # 指定命令描述
            if k == "command_desc":
                command_desc = v
        cls.registry_commands[command_str] = executor
        cls.commands_desc[command_str] = command_desc
        return obj


class CommandBase(object, metaclass=CommandMetaclass):
    """
    command基类，所有的继承类只能实现类方法
    """

    @classmethod
    def get_commands(cls):
        return CommandMetaclass.registry_commands

    @classmethod
    def get_command_desc(cls):
        return CommandMetaclass.commands_desc

    @classmethod
    def execute(cls, *args, **kwargs):
        """
        子类必须实现execute方法
        """
        raise NotImplementedError


def str2camel(string):
    """
    字符串转驼峰
    """
    return "".join(list(map(lambda x: x.capitalize(), string.split("_"))))
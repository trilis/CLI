import re
import subprocess
from src import enviroment
from src.commands import *


def get_command(args):
    """
    return Command instance according to the command
    :param args: arguments
    :return: Command instance
    """
    if args == []:
        return EmptyCommand()
    first = args[0]
    m = re.match("^(\w+)=(.+)$", first)
    if m:
        return AssignmentCommand(m.group(1), m.group(2))
    builtins = {
        "echo": echo,
        "cat": cat,
        "cd": cd,
        "ls": ls,
        "wc": wc,
        "pwd": pwd,
        "exit": exit_
    }
    if first in builtins.keys():
        return BuiltInCommand(builtins[first], args[1:])
    else:
        return ExternalCommand(args)


class Command:
    def launch(self, context, input_text):
        raise NotImplementedError


class EmptyCommand(Command):
    def launch(self, context, input_text):
        return input_text


class AssignmentCommand(Command):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def launch(self, context, input_text):
        enviroment.add_value(self.name, self.value)
        return ""


class BuiltInCommand(Command):
    def __init__(self, command_function, args):
        self.function = command_function
        self.args = args

    def launch(self, context, input_text):
        return self.function(self.args, context, input_text)


class ExternalCommand(Command):
    def __init__(self, args):
        self.args = args

    def launch(self, context, input_text):
        process = subprocess.run(self.args, input=input_text.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 check=True, cwd=context.get_current_path())
        return process.stdout.decode()


def perform(commands_parts, context):
    """
    performs sequential execution of commands
    :param commands_parts: output of parse method
    :return: output of last command
    """
    commands = [get_command(args) for args in commands_parts]
    input_text = ""
    for command in commands:
        try:
            input_text = command.launch(context, input_text)
        except Exception as e:
            print(e)
    return input_text

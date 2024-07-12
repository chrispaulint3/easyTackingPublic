import enum
from robot.global_var import CommandState
from robot.config import *


def validate_input(command):
    if len(command) <= 0:
        return CommandState.INVALID
    elif command[0] in task_commands:
        if command[0] == "c":
            if len(command) <= 1:
                return CommandState.INVALID
        return CommandState.SUCCESS
    elif command[0] in quit_commands:
        return CommandState.QUIT

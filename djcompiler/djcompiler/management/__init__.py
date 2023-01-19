import os
import sys
from djcompiler.management.command import BaseCommand
from djcompiler.management.command import buildfile, buildpy, compile
from typing import Dict


class CommandUtility:
    """
    Encapsulate the logic of the djcompiler utilities.
    """
    commands: Dict[str, BaseCommand] = {
        "compile": compile.CompileProject,
        "buildfile": buildfile.BuildFile,
        "buildpy": buildpy.BuildPY,
        "--help" or "help": compile.CompileProject
    }

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        if self.prog_name == "__main__.py":
            self.prog_name = "python -m djcompiler"

    def get_command(self):
        command = self.commands.get(self.argv[1], "help")()
        if len(self.argv) > 1:
            command = self.commands.get(self.argv[1], "help")(self.argv[2:])
        if not command:
            raise f"command {command} is not available use help command to show commands"
        return command

    def execute(self):
        return self.get_command().execute()


def execute_from_command_line(argv=None):
    """Run a CommandUtility."""
    utility = CommandUtility(argv)
    return utility.execute()

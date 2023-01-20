import os
import sys
from djcompiler.management.command import BaseCommand, buildfile, buildpy, compile


class Help(BaseCommand):
    description: str = "\n\tThis command shows all commands available and how the usage of each one of them"

    def commands_description(self):
        for command_name, command_class in commands.items():
            print(f"djcompiler {command_name}: {command_class.description}")

    def execute(self):
        self.commands_description()


commands: dict = {
    "buildfile": buildfile.BuildFile,
    "buildpy": buildpy.BuildPY,
    "compile": compile.CompileProject,
    "help": Help,
    "--help": Help,
}


class CommandUtility:
    """
    Encapsulate the logic of the djcompiler utilities.
    """

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        if self.prog_name == "__main__.py":
            self.prog_name = "python -m djcompiler"

    def get_command(self):
        try:
            command = commands.get(self.argv[1], "help")()
        except IndexError:
            command = commands.get("compile")()
        if len(self.argv) > 1:
            command = commands.get(self.argv[1], "help")(self.argv[2:])
        if not command:
            raise f"command {command} is not available use help command to show commands"
        return command

    def execute(self):
        return self.get_command().execute()


def execute_from_command_line(argv=None):
    """Run a CommandUtility."""
    utility = CommandUtility(argv)
    utility.execute()

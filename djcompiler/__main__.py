"""
Invokes djcompiler when the djcompiler module is runing as a script.

Example: python -m djcompiler
"""
from djcompiler.management import execute_from_command_line

if __name__ == "__main__":
    execute_from_command_line()

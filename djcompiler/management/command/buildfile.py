from djcompiler.management.command import BaseCommand


class BuildFile(BaseCommand):
    description: str = "\n\tThis command generate a djcompiler configs file " \
                       "that has configurations needed to run djcompiler compile" \
                       "\n\tNOTE: Run it in project working directory."
    compiler_config: str = """# Project details
project_name=DjCompiler
project_author=author
project_version=1.0.0
# Compiler data
build_directory=build
other_files_needed=manage.py .env __init__.py
ignored_files=manage.py compiler.py
ignored_dirs=venv/ cython/ .git/ .idea/ build/ __pycache__/"""

    def write_compiler_settings(self):
        with open(".djcompiler", "w") as f:
            f.writelines(self.compiler_config)

    def execute(self):
        self.write_compiler_settings()
        return ".djcompiler settings file was generated successfully."

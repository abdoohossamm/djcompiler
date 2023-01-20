from djcompiler.management.command import BaseCommand


class BuildPY(BaseCommand):
    description: str = "\n\tThis build a djcompiler script that when you run compile the project " \
                       "\n\tNOTE: Run it in project working directory."
    compiler = """
from djcompiler import DjangoCompiler


if __name__ == "__main__":
    compiler: DjangoCompiler = DjangoCompiler(
        project_name="DjCompiler",
        project_author="author",
        project_version="1.0.0",
        build_directory="build",
        other_files_needed=["manage.py", ".env", "__init__.py"],
        ignored_files=["manage.py", "setup.py", "compiler.py"]
    )
    ignored = compiler.initial_ignored_dirs + ["django_compiler/"]
    compiler.set_ignored(ignored)
    compiler.compile_project()
    """

    def write_compiler_script(self):
        with open("compiler.py", "w") as f:
            f.writelines(self.compiler)
        return "wrote the compiler.py successfully"

    def execute(self):
        self.write_compiler_script()
        return "compiler.py was generated successfully."

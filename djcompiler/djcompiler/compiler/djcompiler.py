"""
A django Cython compiler that compiles django projects into C and outputs it to build folder.
"""
import sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import Cython
from Cython.Build import cythonize
import os
import shutil
from typing import List, Set


class DjangoCompiler:
    """
    A class that compiles django project to C language.
    """
    build_directory: str = ""
    c_dir: str = ""
    migration_dirs: list = []
    ignored_dirs: list = []
    ignored_files: list = []
    initial_ignored_dirs: list = ["venv/", "cython/", ".git/", ".idea/", "build/", "__pycache__/"]

    def __init__(self,
                 ignored_dirs: List[str] = None,
                 build_directory: str = "build",
                 other_files_needed: List[str] = None,
                 ignored_files: List[str] = None,
                 project_name: str = "",
                 project_author: str = "author",
                 project_version: str = "1.0.0",
                 c_dir: str = "",
                 ):
        """
        A class that compiles django project to C language.
        :param ignored_dirs: list[str] -> a list of directories to ignore while building for example the env variables.
        :param build_directory: path to the build output directory.
        :param other_files_needed: files to copy to the build directory like the env file or manage.py script.
        :param c_dir: a path to the C files output.
        """
        if ignored_dirs is None:
            ignored_dirs = []
        if ignored_files is None:
            ignored_files = []
        if other_files_needed is None:
            other_files_needed = []
        self.ignored_dirs = ignored_dirs
        self.ignored_files = ignored_files
        self.build_directory = build_directory
        self.other_files_needed = other_files_needed
        self.project_name = project_name
        self.project_author = project_author
        self.project_version = project_version
        if len(sys.argv) < 2:
            sys.argv = ['setup.py', 'build_ext', '--build-lib', build_directory]
        if '--build-lib' in sys.argv:
            self.build_directory = sys.argv[sys.argv.index('--build-lib') + 1]

    def set_ignored(self, ignored_dirs: List[str] = None, ignored_files: List[str] = None):
        if ignored_dirs:
            self.ignored_dirs = ignored_dirs
        if ignored_files:
            self.ignored_files = ignored_files

    def check_ignored_dirs(self, path_name: str):
        """
        A function to check if the file should be ignored_dirs but checking its path
        :param path_name: path to check if should be ignored_dirs or no
        :return: True if the files should be ignored_dirs and false if shouldn't
        """
        for i in self.ignored_dirs:
            if i in path_name:
                return True
        return False

    def check_ignored_files(self, file_name: str):
        """
        A function to check if the file should be ignored_dirs but checking its path
        :param path_name: path to check if should be ignored_dirs or no
        :return: True if the files should be ignored_dirs and false if shouldn't
        """
        for i in self.ignored_files:
            if i in file_name:
                return False
        return True

    def ext_modules(self) -> Set[Extension]:
        modules: set = set()
        for path, subdirs, files in os.walk("./"):
            if self.check_ignored_dirs(path_name=path):
                continue
            if path.endswith("migrations"):
                new = path.split("./")[1]
                self.migration_dirs.append(f"{new}")
            for name in files:
                if self.check_ignored_files(name) and (name.endswith(".py") or name.endswith(".pyx")) \
                        and not name.startswith("__") \
                        and not name[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    file = os.path.join(path, name)
                    module_name = file.split("./")[1].split('.py')[0]
                    modules.add(Extension(module_name.replace("/", "."), [file]))
        return modules

    def copy_migrations_to_build(self):
        print("#################### Copy migrations modules ####################")
        for dir_path in self.migration_dirs:
            migration_path: str = f"./{self.build_directory}/{dir_path}"
            if self.check_ignored_dirs(path_name=dir_path):
                continue
            try:
                shutil.rmtree(migration_path)
            except FileNotFoundError as e:
                print(f"building migration file {migration_path}")
            shutil.copytree(f"{dir_path}", migration_path)

    def inital_python_modules(self):
        for path, subdirs, files in os.walk(f"./{self.build_directory}"):
            if path.endswith(f"/{self.build_directory}") or f"./{self.build_directory}/temp." in path:
                continue
            f = open(f"{path}/__init__.py", "w")
            f.close()

    def copy_needed_files(self, files: list = None):
        print("#################### Copy needed files ####################")
        if files is None:
            files = self.other_files_needed
        for file in files:
            try:
                shutil.copy(file, f"./{self.build_directory}")
            except FileNotFoundError:
                print(f"file {file} not found")
            except FileExistsError:
                print(f"file {file} already copied")

    def compile_project(self, ext_modules: Set[Extension] = None,
                        cython_dir: str = "cython",
                        compiler_directives: dict = None
                        ) -> None:
        """
        A function that compiles the django project
        :param ext_modules: set[Extension]: not required -> files that should be compiled
        :param cython_dir: str -> the C files output dir.
        :param compiler_directives: dict -> extra compiler option [like the lanugae]
        :return: None
        """
        if ext_modules is None:
            ext_modules = self.ext_modules()
        if compiler_directives is None:
            compiler_directives = {'always_allow_keywords': True, 'language_level': "3"}
        print("#################### Building python modules ####################")
        setup(
            name=self.project_name,
            version=self.project_version,
            author=self.project_author,
            cmdclass={'build_ext': Cython.Distutils.build_ext},
            ext_modules=cythonize(ext_modules, build_dir=cython_dir,
                                  compiler_directives=compiler_directives,
                                  ),

        )
        self.copy_migrations_to_build()
        self.inital_python_modules()
        self.copy_needed_files()

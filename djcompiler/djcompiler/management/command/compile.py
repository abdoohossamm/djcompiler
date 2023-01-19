from djcompiler.management.command import BaseCommand
from djcompiler.management.command import buildfile
from djcompiler.compiler.djcompiler import DjangoCompiler
import sys


class CompileProject(BaseCommand):
    config: dict = {}

    def intial_configs(self):
        try:
            with open(".djcompiler", "r") as f:
                for line in f.readlines():
                    line = line.rstrip()
                    if "#" in line:
                        continue
                    line_split = line.split("=")
                    value = line_split[1]
                    if len(value.split(" ")) > 1:
                        value = value.split(" ")
                    self.config[line_split[0]] = value
        except FileNotFoundError as e:
            print("The config file couldn't be found type 1 to create it or 0 to finish")
            build_file = input(">>> ")
            if build_file == "1":
                config_file = buildfile.BuildFile()
                config_file.execute()
            if build_file == "0":
                exit()

    def execute(self):
        self.intial_configs()
        build_dir_check = self.config.get("build_directory", False)
        build_dir = build_dir_check if build_dir_check else "build"
        sys.argv = ['setup.py', 'build_ext', '--build-lib', f"{build_dir}"]
        compiler = DjangoCompiler(**self.config)
        compiler.compile_project()







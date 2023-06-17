# -*- coding: utf-8 -*-
import os
import sys
from distutils.core import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install_lib import install_lib
import subprocess
from sys import platform

root_dir = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))
funchook_dir = os.path.join(root_dir, "funchook")


class Build(build_ext):
    def run(self):
        if platform == "win32":
            cmake_cmd = """
            cmake.exe ..
            cmake.exe --build . --config Release
            """
            shell = "cmd"
        else:
            cmake_cmd = """
                    cmake -DCMAKE_BUILD_TYPE=Release -DFUNCHOOK_BUILD_TESTS=OFF ..
                    make
                    """
            shell = "bash"
        funchook_build_dir = os.path.join(funchook_dir, "build")
        if not os.path.exists(funchook_build_dir):
            os.mkdir(funchook_build_dir)
        build_script = """
           cd %s
           %s
           """ % (
            funchook_build_dir,
            cmake_cmd,
        )
        process = subprocess.Popen(shell, stdin=subprocess.PIPE, stdout=sys.stdout)
        out, err = process.communicate(build_script.encode("utf-8"))
        build_ext.run(self)
        if platform == "win32":
            return

        funchook_name = "libfunchook.so.1"
        self.copy_file(os.path.join(funchook_build_dir, funchook_name), os.path.join(root_dir, "hook", funchook_name))


class InstallLib(install_lib):
    def run(self):
        install_lib.run(self)


def build_hook_ext():
    platform_args = []
    link_args = []
    extra_compile_args = []
    strict_build_args = []
    runtime_library_dirs = []

    if platform == "win32":
        libraries = ["funchook", "distorm"]
        library_dirs = [
            os.path.join(funchook_dir, "build", "Release"),
        ]
    else:
        libraries = ["funchook"]
        runtime_library_dirs = ["$ORIGIN"]
        library_dirs = [
            os.path.join(funchook_dir, "build"),
        ]
        platform_args = ["-Wno-cast-function-type"]

        extra_compile_args = [
            "-Wall",
            "-Wextra",
            "-Wno-unused-parameter",
            "-Wmissing-field-initializers",
        ]
    extensions = [
        Extension(
            "hook.fh_hook",
            [os.path.join(root_dir, "hook", "fh_hook.c")],
            libraries=libraries,
            include_dirs=[os.path.join(funchook_dir, "include"), ],
            library_dirs=library_dirs,
            runtime_library_dirs=runtime_library_dirs,
            extra_compile_args=extra_compile_args + strict_build_args + platform_args,
            extra_link_args=link_args,
        ),
    ]
    s_args = ["build_ext", "-b", os.path.join(root_dir)]
    setup(name="hook", ext_modules=extensions,
          cmdclass=dict(build_ext=Build, install_lib=InstallLib), script_args=s_args, verbose=True, )


if __name__ == '__main__':
    build_hook_ext()

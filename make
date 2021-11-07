#!/usr/bin/env python3

from os import chdir, getcwd, remove, mkdir
from os.path import join, isfile, isdir
from platform import system
from subprocess import call
from shutil import rmtree, copy, copytree
from sys import argv

OUTPUT = "bin"


def build():
    """ require pyinstaller """
    chdir("src")
    output = join(getcwd(), OUTPUT)
    if not isdir(output):
        print("Creating output directory:", output)
        mkdir(output)
    exit_code = call("pyinstaller -F --noconsole --onefile transclip.py".split(" "))
    print(f"The process has ended with exit code {exit_code}")
    if system() == "Windows":
        copy("dist/transclip.exe", OUTPUT)
    else:
        copy("dist/transclip", OUTPUT)
    print(join(getcwd(), "resources"), join(getcwd(), OUTPUT))
    copytree(join(getcwd(), "resources"), join(join(getcwd(), OUTPUT), "resources"))


def clean():
    path = join(join(getcwd(), "src"), OUTPUT)
    if isdir(path):
        print("Deleting", path)
        rmtree(path)
    path = join(join(getcwd(), "src"), "build")
    if isdir(path):
        print("Deleting", path)
        rmtree(path)
    path = join(join(getcwd(), "src"), "dist")
    if isdir(path):
        print("Deleting", path)
        rmtree(path)
    path = join(join(getcwd(), "src"), "transclip.spec")
    if isfile(path):
        print("Deleting", path)
        remove(path)


def main():
    del argv[0]
    task = argv[0]
    if task == "build":
        build()
    elif task == 'clean':
        clean()
    else:
        print("Task not found")


if __name__ == '__main__':
    main()



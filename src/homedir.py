"""
This module is designed to operate on the working directory,
making available functionalities to create files and directories
as required by the program process.
"""

from pathlib import Path
from os import mkdir
from os.path import isdir, join


def build_path(owner: str, internal: list) -> str:
    """
        This iterative function builds a route according to the host OS making
        use of the join functionality provided by the os.path module.
    """
    new_path = owner
    for chunk in internal:
        new_path = join(new_path, chunk)
    return new_path


def get_home_path() -> str:
    """
        This function returns the path of the working directory for the program.
    """
    home_path = join(Path().home(), ".tcpl")
    if not isdir(home_path):
        mkdir(home_path)
    return home_path


def makedir(path: str) -> str:
    """
    This function is responsible for creating a folder in the location
    specified, thus returning the folder path or otherwise an empty string.
    """
    if not isdir(path):
        try:
            mkdir(path)
        except:
            return ""
    return path


def check_home() -> bool:
    """
        This function is designed to verify the existence of the working
        directory, this verification will automatically create the working
        directory if it does not exist.
    """
    transclip_home_path = get_home_path()
    return len(makedir(transclip_home_path)) > 0


def create_dir(dir_name: str) -> str:
    """
        This function creates a folder within the working directory, thus
        being able to return the directory path.
    """
    dir_path = join(get_home_path(), dir_name)
    return makedir(dir_path)


def create_file(file_name: str, parent=None):
    """
        This function has the ability to create a text file and return the
        stream of the open file, in case of an unexpected error it will
        return a None value.
    """
    if file_name != None and len(file_name) > 0:
        try:
            if parent is not None:
                chunks: list = parent.split("/")
                chunks.append(file_name)
                file_path = build_path(get_home_path(), chunks)
            else:
                file_path = join(get_home_path(), file_name)
            return open(file_path, "a", encoding="utf-8")
        except:
            return None
    else:
        return None

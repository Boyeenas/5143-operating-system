import os
import shutil
"""Shutil module offers high-level operation on a file like a copy, create, and 
remote operation on the file. It comes under Python’s standard utility modules. 
This module helps in automating the process of copying and removal of files and directories.
"""
"""
This function first checks if the length of the params more than 1. If it is, again it checks if the source path provided is directory,if it is a directory then it copies all the content to the destination param using copytree() and the moved file is deleted from source using rmtree().

if the given source param is file then it just moves the contents to destination using move().

lastly if only param is provided,it raises an exception

-> copytree() method from shutil recursively copies an entire directory tree from source to the destination.

-> rmtree() method on the otherhand deletes an entire directory and it's contents.


-> shutil.move() method Recursively moves a file or directory to another location and returns the destination. If the destination directory already exists then src is moved inside that directory. If the destination already exists but is not a directory then it may be overwritten.

"""
def mv(**kwargs):
    """
NAME
    mv - move or rename files and directories
SYNOPSIS
    mv [OPTION]... SOURCE DEST
DESCRIPTION
    Move or rename the SOURCE to DEST.

OPTIONS
    --help
        Display this help message and exit.

    SOURCE
        The source file or directory to move or rename.

    DEST
        The destination file or directory where SOURCE will be moved or renamed.

RETURN VALUE
    This function does not return any value.

EXAMPLES
    mv file.txt new_name.txt
        Rename 'file.txt' to 'new_name.txt'.

    mv source_directory/ destination_directory/
        Move 'source_directory/' to 'destination_directory/'.

    mv --help
        Display help and exit.

"""
    flags=[]
    params=[]
    if 'params' in kwargs:
        params = kwargs['params']
    if 'flags' in kwargs:
        flags = kwargs['flags']
    if len(params)>1:
        if os.path.isdir(params[0]):
            shutil.copytree(params[0], params[1])
            shutil.rmtree(params[0])
        else:
            shutil.move(params[0], params[1])
    else:
        raise Exception("Both Source and Destination paths are required")
    return ""


import os
import shutil

'''
This function first checks if the keys params and flags are there in kwargs and extracts them if they are available.
If provided with the directory path, it will remove the entire directory with the help of shutil module recursively.
shutil is a shell utilities module, it lets us to perform operations on file like copy, move and deleting.
the rmtree() method will delete the entire directory provided as input
'''
def rmdir(**kwargs):
    """
NAME
    rmdir - remove directories
SYNOPSIS
    rmdir [OPTION]... DIRECTORY...
DESCRIPTION
    Remove the DIRECTORY(ies).

OPTIONS
    --help
        Display this help message and exit.

DIRECTORY
    The directory(ies) to remove.

RETURN VALUE
    This function does not return any value.

EXAMPLES
    rmdir empty_directory/
        Remove the directory 'directory/'.

    rmdir --help
        Display help and exit.

"""
    flags=[]
    params=[]
    if 'params' in kwargs:
        params = kwargs['params']
    if 'flags' in kwargs:
        flags = kwargs['flags']
    if params:
       os.rmdir(params[0])
    
    return ""


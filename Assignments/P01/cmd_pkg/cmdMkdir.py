import os
"""MKDIR DESCRIPTION:
This Python code defines a function named mkdir. Here are its actions:
-->It accepts keyword arguments 'params' (providing the name of the new directory to create)
and 'flags' (which are not used in this code).
-->When 'params' is supplied, a directory with the specified name is checked to see if it
 already exists. If it doesn't, it uses os.mkdir() to create a new directory with that name.
-->If 'params' is not provided or is empty, an exception is thrown with the message "New Directory Name is required."
-->The function returns an empty string, indicating that the directory creation attempt was successful.
"""
def mkdir(**kwargs):
    """
NAME
    mkdir - create directories
SYNOPSIS
    mkdir [OPTION]... DIRECTORY...
DESCRIPTION
    Create the DIRECTORY(ies), if they do not already exist.

OPTIONS
    --help
        Display this help message and exit.

DIRECTORY
    The directory or directories to create.

RETURN VALUE
    This function does not return any value.

EXAMPLES
    mkdir new_directory
        Create a directory named 'new_directory'.

    mkdir --help
        Display help and exit.

"""
    flags=[]
    params=[]
    if 'params' in kwargs:
        params = kwargs['params']
    if 'flags' in kwargs:
        flags = kwargs['flags']
    if params:
        if not os.path.isdir(params[0]):
            os.mkdir(params[0])
    else:
        raise Exception("New Directory Name is required")
    return ""

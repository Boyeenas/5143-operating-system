import shutil
import os

# This Python code defines the cp function, which is used to copy files.
# It takes the keyword parameters 'params' (which provide the source and
# destination file paths) and 'flags' (which are not used here).
# If 'params' includes at least two entries, the shutil is used.
# To copy a file from the first path (source) to the second path
# (destination), use the copy2 function. Both the Source and Destination
# paths must be present for 'params' to function, otherwise an exception
# is raised with the message "Both Source and Destination paths are
# required" and an empty string is returned.


# Shutil:
# shutil.move() method Recursively moves a file or directory to another location
# and returns the destination. If the destination directory already exists,
# then src is moved inside that directory. If the destination already exists,
# but is not a directory then it may be overwritten.
# -> copytree() method from shutil recursively copies an entire directory tree
#  from source to the destination.
# -> rmtree() method on the otherhand deletes an entire directory and it's contents.
def cp(**kwargs):
    """
    NAME
        cp - copy files or directories
    SYNOPSIS
        cp [OPTION]... SOURCE DEST
    DESCRIPTION
        Copy SOURCE to DEST.

    OPTIONS
        --help
            Display this help message and exit.

        SOURCE
            The source file or directory to copy.

        DEST
            The destination file or directory where SOURCE will be copied.

    RETURN VALUE
        This function does not return any value.

    EXAMPLES
        cp file.txt new_file.txt
            Copy the file 'file.txt' to 'new_file.txt'.


        cp --help
            Display help.
    """
    flags = []
    params = []
    if "params" in kwargs:
        params = kwargs["params"]
    if "flags" in kwargs:
        flags = kwargs["flags"]
    if len(params) > 1:
        if os.path.isdir(params[0]):
            shutil.copytree(params[0], params[1])
        else:
            shutil.copyfile(params[0], params[1])
    else:
        raise Exception("Both Source and Destination paths are required")

    return ""

import os


# pwd command Descritpion:
# It simply returns the current working directory as a string.
def pwd(**kwargs):
    """
    NAME
        pwd - print the current working directory
    SYNOPSIS
        pwd
    DESCRIPTION
        Print the current working directory.

    OPTIONS
        --help
            Display this help message and exit.

    RETURN VALUE
        The current working directory as a string.

    EXAMPLES
        pwd
            Print the current working directory.

        pwd --help
            Display help and exit.
    """
    return os.getcwd()

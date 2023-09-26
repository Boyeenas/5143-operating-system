import os

# Utility to get a password and/or the current user name.
import getpass

# Who command description:
# Returns and displays the name of the user who is currently logged in


def who(**kwargs):
    """
    NAME
        who - display the username of the current user
    SYNOPSIS
        who
    DESCRIPTION
        Display the username of the current user.

    OPTIONS
        --help
            Display this help message and exit.

    RETURN VALUE
        The username of the current user as a string.

    EXAMPLES
        who
            Display the username of the current user.

        who --help
            Display help and exit.
    """
    return getpass.getuser()

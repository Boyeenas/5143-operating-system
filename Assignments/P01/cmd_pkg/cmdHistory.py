from history import History


# HISTORY DESCRIPTION:
# This Python code defines the history function, which retrieves and displays a history
# of instructions or activities using the History module.
# -->It imports the History module.
# -->It creates a structured history string by using a list comprehension to iterate
# through the history items.
# -->The formatted string contains the item number (beginning with 1) and the
# corresponding history item text.
# -->Finally, it returns the formatted history as a string, with each item on a new line.
def history(**kwargs):
    """
    NAME
        history - display command history
    SYNOPSIS
        history
    DESCRIPTION
        Display a list of previously executed commands.

    OPTIONS
        --help
            Display this help message and exit.

    RETURN VALUE
        A string containing a numbered list of previously executed commands.

    EXAMPLES
        history
            Display the command history.

        history --help
            Display help and exit.
    """
    return "\n".join(
        [
            f"{i+1} {History.get_history_item(i + 1)}"
            for i in range(History.get_current_history_length())
        ]
    )

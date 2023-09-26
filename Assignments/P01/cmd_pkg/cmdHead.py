# Head Command Description:
# A Python function called head that takes keyword arguments (**kwargs).
# It checks if three specific keyword arguments ('params', 'flags', and 'data') are present in kwargs.
# If 'params' is present, it assumes it's a list with a file path and reads the first file's content.
# If 'data' is present, it takes its value as text data.
# Then, it splits the text into lines and returns the first 10 lines of text.
# 'output' variable holds the result that the function returns.


def head(**kwargs):
    """
    NAME
        head - display the beginning of a text file or provided text data
    SYNOPSIS
        head [OPTION]... [FILE]...
    DESCRIPTION
        Display the first 10 lines of FILE(s) or provided text data.

    OPTIONS
        --help
            Display this help message and exit.

        -n
            Display the first NUM lines instead of the default 10.

        FILE
            The file(s) to display the beginning of. If not provided, the function displays the beginning of the provided text data.

    RETURN VALUE
        A string containing the first 10 lines (or specified number of lines) of the text data or file(s).

    EXAMPLES
        head file.txt
            Display the first 10 lines of 'file.txt'.

        head -n 5 file.txt
            Display the first 5 lines of 'file.txt'.

        head --help
            Display help and exit.
    """
    if "params" in kwargs:
        params = kwargs["params"]
    if "flags" in kwargs:
        flags = kwargs["flags"]
    if "data" in kwargs:
        data = kwargs["data"]

    output = ""
    text = ""
    number_of_lines = 10
    # print(kwargs)
    if params:
        filepath = params[0]
        with open(filepath, "r") as f:
            text = f.read()
    elif data:
        text = data

    lines = text.split("\n")
    if len(lines) < number_of_lines:
        output = text
    else:
        output = "\n".join(lines[:number_of_lines])

    return output

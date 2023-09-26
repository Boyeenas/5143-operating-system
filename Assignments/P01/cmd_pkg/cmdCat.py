    """
    CAT DESCRIPTION:
The Python code given defines a method named cat that concatenates 
the contents of text files specified in the 'params' parameter. 
It determines whether the parameter 'params' is present, divides 
comma-separated file paths, reads and concatenates the contents of 
each path into a single text string, and then returns it.
 When 'params' is not given, an exception is raised with the message 
"File Path is Required."
"""


def cat(**kwargs):
    """
NAME
    cat - concatenate files and print on the standard output
SYNOPSIS
    cat [OPTION]... [FILE]...
DESCRIPTION
    Concatenate FILE(s) and print on the standard output.

OPTIONS
    --help
        Display this help message and exit.

    FILE
        The file(s) to concatenate and print. Multiple files can be provided, separated by commas.

RETURN VALUE
    A string containing the concatenated content of the specified files.

EXAMPLES
    cat file1.txt file2.txt
        Concatenate the contents of 'file1.txt' and 'file2.txt' and print on the standard output.

    cat --help
        Display help and exit.

"""
    if 'params' in kwargs:
        params = kwargs['params']
    if 'flags' in kwargs:
        flags = kwargs['flags']
    
    if params:
        files=[]
        for param in params:
            if "," in param:
                files+=param.split(",")
            else:
                files.append(param)
        text=""
        for file in files:
            with open(file , "r") as f:
                text+= f.read()
        return text
    else:
        raise Exception("File Path is Required")
    
        

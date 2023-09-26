'''
1. It determines whether the keyword arguments contain the terms
 "params," "flags," and "data."
2. If 'params' is given, it reads the contents of the file into the
 'text' variable under the assumption that the first element of 'params' is a file path.
3. If 'data' is given, it sets 'text' to the given data.
4. The 'text' is then divided into lines, and a check is made to see
  if there are less lines than the default (or provided) number of lines, which is 10 lines. 
  If so, it returns the whole 'text'; if not, it sets the output to last 10 lines starting from end of the file and returns it.
 '''

def tail(**kwargs):
    """
NAME
    tail - display the end of a text file or provided text data
SYNOPSIS
    tail [OPTION]... [FILE]...
DESCRIPTION
    Display the last 10 lines of FILE(s) or provided text data.

OPTIONS
    -n, --lines=NUM
        Display the last NUM lines instead of the default 10.

    --help
        Display this help message and exit.

    FILE
        The file(s) to display the end of. If not provided, the function displays the end of the provided text data.

RETURN VALUE
    A string containing the last 10 lines (or specified number of lines) of the text data or file(s).

EXAMPLES
    tail file.txt
        Display the last 10 lines of 'file.txt'.

    tail -n 5 file.txt
        Display the last 5 lines of 'file.txt'.

    

    tail --help
        Display help and exit.

"""
    if 'params' in kwargs:
        params = kwargs['params']
    if 'flags' in kwargs:
        flags = kwargs['flags']
    if 'data' in kwargs:
        data = kwargs['data']
    
    output=""
    text=""
    number_of_lines=10

    if params:
        filepath=params[0]
        with open(filepath , "r") as f:
            text=f.read()
    elif data:
        text=data

    lines=text.split("\n")
    if len(lines)<number_of_lines:
        output= text
    else:
        output= "\n".join(lines[len(lines)-number_of_lines-1:])

    
    return output

   
        

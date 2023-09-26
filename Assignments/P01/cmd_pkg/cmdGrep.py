 """
    GREP DESCRIPTION:
This Python code defines the grep function. 
-->It allows you to search for a specific term within text data or files.
-->It looks for keyword arguments such as 'params' (which contain keyword 
and file paths), 'flags' (which indicate search choices), and 'data' 
(which is provided directly).
-->It extracts the keyword and, depending on the existence of certain flags,
 either searches for and lists files that contain the keyword or looks for 
occurrences of the keyword in a given file or data.
-->The function provides the search results as a string, which includes 
either the filtered file names or the lines that include the term.
-->If the keyword 'params' is not provided or is missing, an exception is raised.
"""


def grep(**kwargs):
       """
NAME
    grep - search for a keyword in text data or file content
SYNOPSIS
    grep KEYWORD [FILE]...
DESCRIPTION
    Search for occurrences of KEYWORD in FILE(s) or provided text data and display matching lines.

OPTIONS
    --help
        Display this help message and exit.

    KEYWORD
        The keyword to search for in the text data or files.

    FILE
        The file(s) in which to search for the KEYWORD. If not provided, the function searches in the provided text data.

RETURN VALUE
    A string containing the lines that contain the KEYWORD.

EXAMPLES
    grep "search_term" file.txt
        Search for occurrences of "search_term" in 'file.txt'.

    grep --help
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
    if params:
        keyword=params[0]
        if len(params)>1:
            if "l" in flags:
                filter_files=[]
                for filepath in params[1:]:
                    
                    with open(filepath,"r") as f:
                        text=f.read()
                        
                        if keyword in text:
                            filter_files.append(filepath)
                output="\n".join(filter_files)
            else:
                filepath=params[1]
                with open(filepath,"r") as f:
                    text+=f.read()
                outputlines=[]
                lines=text.split("\n")
                for line in lines:
                    if keyword in line:
                        outputlines.append(line)
                output="\n".join(outputlines)
           
        else:
            text=data
            outputlines=[]
            lines=text.split("\n")
            for line in lines:
                if keyword in line:
                    outputlines.append(line)
            output="\n".join(outputlines)
    else:
        raise Exception("Keyword is Required")
    return output

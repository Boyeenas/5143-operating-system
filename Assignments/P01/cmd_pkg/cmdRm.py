import os
import shutil
"""
Shutil module offers high-level operation on a file like a copy, create, 
and remote operation on the file. It comes under Python’s standard utility modules.
 This module helps in automating the process of copying and removal of files and directories

"""

"""
RM DESCRIPTION:
This function removes the files from the directory.
Intially it checks if the there is params and if they are it checks for a wildcard operator, if it exists then it extracts and assigns the start and end parts of a pattern based on the asterisk character in the first parameter. 
if the dirname is empty string, the current working directory will be assigned to the dirname
using os.getcwd().
Then the function will iterate over each file in the directory and checks if the file starts and ends with file that was extraced eariler using wildcard.if the file meets this conditon it will be removed.
"""
def rm(**kwargs):
    """
NAME
    rm - remove files
SYNOPSIS
    rm [OPTION]... FILE...
DESCRIPTION
    Remove the FILE(s).

OPTIONS
    -r
        Recurse into non-empty folder to delete all

    --help
        Display this help message and exit.

FILE
    The file(s) to remove.

RETURN VALUE
    This function does not return any value.

EXAMPLES
    rm file.txt
        Remove 'file.txt'.

    rm --help
        Display help and exit.

"""
    flags=[]
    params=[]
    if 'params' in kwargs:
        params = kwargs['params']
    if 'flags' in kwargs:
        flags = kwargs['flags']
    if params:
        if "*" in params[0]:
            start,end=os.path.basename(params[0]).split("*")
            
            dirname=os.path.dirname(params[0])
            if dirname=="":
                dirname=os.getcwd()
            for file in os.listdir(dirname):
                
                if file.startswith(start) and file.endswith(end):
                    os.remove(os.path.join(dirname,file))
        elif "r" in flags:
            shutil.rmtree(params[0])
        else:
            os.remove(params[0])
    
    return ""


import os
import time
import stat
from colorama import Fore, Style, init


RESET = Style.RESET_ALL
RED = Fore.RED
BLUE = Fore.BLUE
ORANGE = Fore.MAGENTA
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW


'''
This function returns a boolean output based on the filepath provided has hidden attributes in it or not.
The stat module retrives information about a file.
'''
def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

'''
This funtion returns a table of the data given.
'''
def print_table(data,header=None):
    table=""
    if not data:
        print("No data to display.")
        return

    # Find the maximum width for each column
    col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]

    # Print the header
    if header:
        header_list = [str(item).center(width) for item, width in zip(header, col_widths)]
        table+="  ".join(header_list)+"\n"
        table+="-" * (sum(col_widths) + len(col_widths) * 3 - 1)+"\n"

        #print("  ".join(header_list))
        #print("-" * (sum(col_widths) + len(col_widths) * 3 - 1))

    # Print the data rows
    for row in data:
        formatted_row = [str(item).ljust(width) for item, width in zip(row, col_widths)]
        #print("  ".join(formatted_row))
        table+="  ".join(formatted_row)+"\n"
    return table

'''
This function takes an iterable as paramter and it converts that into string and then it pads the data to match the widest string and returns it
'''
def columnify(iterable):
    # First convert everything to its repr
    strings = [repr(x) for x in iterable]
    # Now pad all the strings to match the widest
    widest = max(len(x) for x in strings)
    padded = [x.ljust(widest) for x in strings]
    return padded

'''
The colprint function will organize the elements in the colunms with a specified width
'''
def colprint(iterable, width=72):
    output=""
    columns = columnify(iterable)
    colwidth = len(columns[0])+2
    perline = (width-4) // colwidth
    
    for i, column in enumerate(columns):
        output+=column+" "

        if i % perline == perline-1:
            output+="\n"

    output+="\n"
    return output

'''
This function converts the data to human readale format
'''
def bytes_to_human_readable(byte_size):
    # Define the suffixes for different units
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    # Handle the case where the byte_size is 0
    if byte_size == 0:
        return "0B"

    # Calculate the appropriate unit and convert the size
    i = 0
    while byte_size >= 1024 and i < len(suffixes) - 1:
        byte_size /= 1024.0
        i += 1

    # Format the result with a maximum of two decimal places
    result = f"{byte_size:.2f} {suffixes[i]}"
    return result

'''
This function helps provide information about a file or directory given its path, including its size, last modified date and time, and file name.
'''
def get_file_info(file_path):
    try:
        stat_info = os.stat(file_path)
        # Field 1 - Size
        #permission = oct(stat.S_IMODE(stat_info.st_mode))
        permission_string = str(stat.filemode(stat_info.st_mode))


        # Field 2 - Size
        if os.path.isdir(file_path):
            size = "<DIR>"
        else:
            size = stat_info.st_size
        
        # Field 3 - Last modified date and time
        last_modified = time.strftime("%b %d %H:%M", time.localtime(stat_info.st_mtime))
        
        # Field 4 - File name
        file_name = os.path.basename(file_path)
        return [permission_string,size,last_modified,file_name]
    except FileNotFoundError:
        return "File or folder not found."
    
'''
The ls function lists files in a directory based on specified parameters and flags.
The flag -a displays the hidden files in the directory
-l displays detailed information of the file or directory including permissions, owner, group and more
-h displays data in human readale format
'''
def ls(**kwargs):
    """
NAME
    ls - list files and directories in the current directory
SYNOPSIS
    ls [OPTION]... [DIRECTORY]...
DESCRIPTION
    List files and directories in the specified DIRECTORY or the current directory.

OPTIONS
    -a
        List all files and directories, including hidden ones.

    -l
        Use a long listing format, displaying additional file details.

    -h
        Display file sizes in human-readable format (e.g., KB, MB).

    --help
        Display this help message and exit.

DIRECTORY
    The directory to list files and directories from. If not provided, lists the contents of the current directory.

RETURN VALUE
    A string containing the list of files and directories in the specified directory.

EXAMPLES
    ls
        List files and directories in the current directory.

    ls /path/to/directory
        List files and directories in '/path/to/directory'.

    ls -a
        List all files and directories, including hidden ones.

    ls -l
        Use a long listing format to display additional file details.

    ls -h
        Display help and exit.

"""

    flags=[]
    params=[]
    if 'params' in kwargs:
        params = kwargs['params']
    if 'flags' in kwargs:
        flags = kwargs['flags']


    showHidden = "a" in flags
    longListing = "l" in flags
    humanReadableSizes = "h" in flags
    path=os.getcwd()
    if params:
        path=params[0]

    filesList=[]
    for file in os.listdir(path):
        if not has_hidden_attribute(os.path.realpath(os.path.join(path,file))) or showHidden:
            if longListing:
                
                file_info=get_file_info(os.path.join(path,file))
                if humanReadableSizes and file_info[1]!="<DIR>":
                    file_info[1]=bytes_to_human_readable(file_info[1])
                

                file_info[0]=RED+file_info[0]+RESET
                if file_info[1]=="<DIR>":
                    file_info[1]=YELLOW+str(file_info[1])+RESET
                else:
                    file_info[1]=BLUE+str(file_info[1])+RESET

                file_info[2]=ORANGE+file_info[2]+RESET
                file_info[3]=GREEN+file_info[3]+RESET


                filesList.append(file_info)
                
            else:
                filesList.append(file)

    if longListing:
        return print_table(filesList)

    else:
        return colprint(filesList,100)
    

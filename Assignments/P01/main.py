##P01
## Divya Podila , Soundarya Boyeena, Rakesh Rapalli
## Basic implementaion of Shell 
## Work in progress.. Implemented ls,ls -a,ls -h ,ls -lah, DIR, pwd , arrow key UP for history
import os
import stat
import time


home_directory=os.getcwd()
cwd=os.getcwd()

def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
def print_table(data,header=None):
    if not data:
        print("No data to display.")
        return

    # Find the maximum width for each column
    col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]

    # Print the header
    if header:
        header_list = [str(item).center(width) for item, width in zip(header, col_widths)]
        print(" | ".join(header_list))
        print("-" * (sum(col_widths) + len(col_widths) * 3 - 1))

    # Print the data rows
    for row in data:
        formatted_row = [str(item).ljust(width) for item, width in zip(row, col_widths)]
        print(" | ".join(formatted_row))

def columnify(iterable):
    # First convert everything to its repr
    strings = [repr(x) for x in iterable]
    # Now pad all the strings to match the widest
    widest = max(len(x) for x in strings)
    padded = [x.ljust(widest) for x in strings]
    return padded

def colprint(iterable, width=72):
    columns = columnify(iterable)
    colwidth = len(columns[0])+2
    perline = (width-4) // colwidth
    
    for i, column in enumerate(columns):
        print(column,end=" ")
        if i % perline == perline-1:
            print('\n', end="")
    print("")

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

def get_file_info(file_path):
    try:
        stat_info = os.stat(file_path)

        # Field 1 - Size
        if os.path.isdir(file_path):
            size = "📁"
        else:
            size = stat_info.st_size
        
        # Field 2 - Last modified date and time
        last_modified = time.strftime("%b %d %H:%M", time.localtime(stat_info.st_mtime))
        
        # Field 3 - File name
        file_name = os.path.basename(file_path)
        return [size,last_modified,file_name]
    except FileNotFoundError:
        return "File or folder not found."





def ls(params):
    if not params:
        params=[""]
    showHidden = "a" in params[0]
    longListing = "l" in params[0]
    humanReadableSizes = "h" in params[0]

    filesList=[]
    for file in os.listdir(cwd):
        if not has_hidden_attribute(os.path.realpath(os.path.join(cwd,file))) or showHidden:
            if longListing:
                
                file_info=get_file_info(os.path.join(cwd,file))
                if humanReadableSizes and file_info[0]!="📁":
                    file_info[0]=bytes_to_human_readable(file_info[0])
                                        
                filesList.append(file_info)
                
            else:
                filesList.append(file)

    if longListing:
        print_table(filesList)

    else:
        colprint(filesList,100)


        
def cd(path=None):
    global cwd
    if path == "..":
        back_folder=os.path.dirname(os.path.realpath(cwd))
        os.chdir(back_folder)
    elif path == "~":
        os.chdir(home_directory)
    else:
        os.chdir(os.path.join(cwd,path))
    cwd=os.getcwd()

def mkdir(path):
    os.mkdir(path)
def pwd():
    print(cwd)

while True:
    cmd=input("% ").split()

    command = cmd[0]
    params = cmd[1:]

    if command == "ls":
        ls(params)
        
    elif command == "cd":
        cd(params[0])

    elif command == "mkdir":
        mkdir(params[0])

    elif command == "pwd":
        pwd()


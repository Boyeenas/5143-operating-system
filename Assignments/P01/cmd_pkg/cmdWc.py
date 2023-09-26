'''
This function returns the count of word, character and lines of a specified file when given as its input parameter.

The function first checks if the keys params and flags are there in kwargs if they are then it extracts and assigns them to a variable.

The flag -l displays the count of lines in the file.
The flag -w displays the count of words in the file.
The flag -m displays the count of characters in the file.
And if there is no flag is provided, it displays all the counts.
'''
def wc(**kwargs):
    """
NAME
    wc - count lines, words, and characters in text
SYNOPSIS
    wc [OPTION]... [FILE]...
DESCRIPTION
    Count lines, words, and characters in FILE(s) or provided text data and display the result.

OPTIONS
    -l, --lines
        Display the number of lines.

    -w, --words
        Display the number of words.

    -m, --characters
        Display the number of characters.

    --help
        Display this help message and exit.

    FILE
        The file(s) to count lines, words, and characters in. If not provided, the function counts the provided text data.

RETURN VALUE
    A string containing the counts of lines, words, and characters.

EXAMPLES
    wc file.txt
        Count lines, words, and characters in 'file.txt' and display the result.

    wc -l file.txt
        Count lines in 'file.txt' and display the result.

    wc -w file.txt
        Count words in 'file.txt' and display the result.

    wc -m file.txt
        Count characters in 'file.txt' and display the result.

    wc --help
        Display help and exit.

"""
    if 'params' in kwargs:
        params = kwargs['params']
    if 'flags' in kwargs:
        flags = kwargs['flags']
    if 'data' in kwargs:
        data = kwargs['data']
    
    showLines = "l" in flags or len(flags)==0
    showwords = "w" in flags or len(flags)==0
    showalpha = "m" in flags or len(flags)==0

    output=""
    text=""
    if params:
        with open(params[0],"r") as f:
            text=f.read()
    elif data:
        text=data
    
    if showLines:
        if text:
            output+=str(len(text.strip("\n").split("\n")))+" "
        else:
            output+="0 "
    if showwords:
        if text:
            longline=text.replace("\n"," ").strip()
            words=len(longline.split(" "))
            output+=str(words)+" "
        else:
            output+="0 "
    if showalpha:
        output+=str(len(text))+" "
    return output

   

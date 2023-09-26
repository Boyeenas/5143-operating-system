####################################################
#  ____             _____         ______    _____  #
# |       |  |    |      |       |      |  |       #
# |____   |  |____| _____|  ___  |      |  |_____  #
#      |  |       |      |       |      |        | #
# _____|  |       | _____|       |______|   _____| #
#                                                  #
####################################################

####################################################
#       _____           _____                      #
#      |     |         |     |      |              #
#      |_____|  _____  |     |      |              #
#      |               |     |      |              #
#      |               |_____|      |              #
#                                                  #
####################################################

####################################################
#        ***IMPLEMENTATION OF A :*****             #
#                                                  #
#     *******  *                *    *             #
#     *        *                *    *             #
#     *        *       *******  *    *             #
#     *******  ******* *     *  *    *             #
#           *  *     * *******  *    *             #
#           *  *     * *        *    *             #
#     *******  *     * *******  *    *             #
####################################################

####################################################
#                                                  #
# *TEAM MEMBERS:*                                  #
# 1. Divya Podila                                  #
# 2. Soundarya Boyeena                             #
# 3. Rakesh Rapalli                                #
#                                                  #
####################################################


# Import required modules
from cmd_pkg import *
from history import History
import os
import sys
from colorama import Fore, Style, Back


if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def show_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

# Define ANSI color coding constants for formatting output to make it look prettier
RESET = Style.RESET_ALL
RED = Fore.RED
BLUE = Fore.BLUE
ORANGE = Fore.LIGHTYELLOW_EX
GREEN = Fore.GREEN
BLACK = Fore.BLACK
WHITE_BACK = Back.WHITE
line_cursor = 0  # the cursor is at the beginning of the command line.


# FUNCTION FOR: COMMAND PARSING
# Basic Idea:
# We initialized an empty dictionary called "command" to store all the command components.
# It checks if the command contains spaces.
# If not, it considers the whole command as "name" and returns the command dictionary.
# If there are spaces " " it splits the command into parts after each space.
# First part is command[0] for name, command[1:] remaining for
# "FLAGS(-)","PARAMS","Directives(--)"


def parseCommand(cmd):
    command = {"name": "", "params": [], "flags": [], "directives": []}
    if " " in cmd:
        cmd = cmd.replace("<", "")
        splitedCommand = cmd.split(" ")
    else:
        command["name"] = cmd
        return command

    command["name"] = splitedCommand[0]

    for i in splitedCommand[1:]:
        if "--" in i:
            command["directives"].append(i.strip("--"))
        elif "-" in i:
            command["flags"] += list(i.strip("-"))
        elif i != "":
            command["params"].append(i)

    return command


# FUNCTION FOR: splitting a cmd into multiple cmds and file redirection handling.
# Basic Idea:
# This function takes a single string as input and initializes another
# dictionary called "parsedcmd" to store info about multiple commands and file redirections.
# Then we store cmd into commandsString to track the command after splitting.
def splitcmd(cmd):
    parsedcmd = {"commands": [], "appendFile": "", "writeFile": ""}

    commandsString = cmd
    # if the command contains >>(file appending), it splits the string cmd string into
    # two parts using split(">>").
    # Firstpart:"splitedCMD[0]" => commands before >>,then store it in "commandsString".
    # whitespace is stripped using strip()
    # Secondpart:"splitedCMD[1]" => the file to which the output should be appended,
    # and it's stored in the "appendFile field" of the dictionary parsedcmd.

    if ">>" in cmd:
        splitedCMD = cmd.split(">>")
        commandsString = splitedCMD[0].strip()
        parsedcmd["appendFile"] = splitedCMD[1].strip()

    # if the command contains >(file writing), it splits the string cmd string into
    # two parts using split(">").
    # Firstpart:"splitedCMD[0]" => commands before >,then store it in "commandsString".
    # whitespace is stripped using strip()
    # Secondpart:"splitedCMD[1]" => the file to which the output should be appended,
    # and it's stored in the "writeFile field" of the dictionary parsedcmd.

    elif ">" in cmd:
        splitedCMD = cmd.split(">")
        commandsString = splitedCMD[0].strip()
        parsedcmd["writeFile"] = splitedCMD[1].strip()

    # initializing a list called "commands" to hold individual command strings.
    # Checking if the commandsString contains multiple commands separated by pipes(|).
    # If | is found,it splits commandsString into seperate strings using split("|"),
    # and assigns cmds to the commands list.
    commands = [commandsString]
    if "|" in commandsString:
        commands = commandsString.split("|")

    # iterate through the commands list,For each command,we call the"parseCommand"to parse
    # the command string into name, parameters, flags, directives
    # and append the resulting dictionary to the commands list in the parsedcmd dictionary.
    for command in commands:
        parsedcmd["commands"].append(parseCommand(command.strip()))

    return parsedcmd


# creating instance of commandshelper class
cmdhelper = CommandsHelper()

# creating instance of our getch
getch = Getch()

# concatenates the green color escape code with the "percent symbol",
# percent symbol will be displayed in green.
# set default command prompt
prompt = GREEN + "%" + RESET


# FUNCTION FOR: displaying a command string at the bottom of the terminal.
# Basic Idea:
# To clear the current command line by overwriting it with spaces and then
# display the provided cmd.


def print_cmd(cmd,cursor=True):
    """This function "cleans" off the command line, then prints
    whatever cmd that is passed to it to the bottom of the terminal.
    """
    # padding to make sure that any previous content on the command line is overwritten
    # by spaces,clearing the line.
    padding = " " * 80

    # moves the cursor to the beginning of the current line.
    sys.stdout.write("\r" + padding)
    if cursor:
        if len(cmd)<=line_cursor:
            cmd+=" "
        #changing char background and foreground color at cursor position
        cmd=cmd[:line_cursor]+WHITE_BACK+BLACK+cmd[line_cursor]+RESET+cmd[line_cursor+1:] 
    
    sys.stdout.write("\r" + prompt + cmd)
    # output is immediately written to the terminal.
    # To avoid output buffering
    sys.stdout.flush()


if __name__ == "__main__":
    cmd = ""  # empty cmd variable

    print_cmd(cmd)  # print to terminal
    hide_cursor()
    history_cursor = 1

    # loop forever
    while True:
        # read a character(but don't print-> getch)
        char = getch()

        # user pressed Ctrl-C (b"\x03") or if the current command is "exit
        # Then sys.exit() terminate shell.
        if char == b"\x03" or cmd == "exit":  # ctrl-c
            show_cursor()
            sys.exit()

        # user pressed the backspace key (b"\x08")
        elif char == b"\x08":
            # cmd = cmd[:-1]
            # and if line_cursor is not at the beginning (0),

            if line_cursor != 0:
                # backspace operation by removing the character
                # before the cursor position (line_cursor - 1) from the cmd string.
                # and update the line_cursor to move the cursor back by 1.
                cmd = cmd[: line_cursor - 1] + cmd[line_cursor:]
                if line_cursor > 0:
                    line_cursor -= 1

            print_cmd(cmd)
            # moving cursor back to the correct position within the line after backspace.
            if len(cmd) - line_cursor != 0:
                sys.stdout.write("\x1b[%dD" % (len(cmd) - line_cursor))

            history_cursor = History.get_current_history_length() + 1

        elif char == b"\xe0":  # arrow key pressed
            # null = getch()                  # waste a character
            direction = getch()  # grab the direction

            if direction == b"H":  # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                # prints out 'up' then erases it (just to show something)

                if history_cursor - 1 > 0:
                    history_cursor -= 1
                    cmd = History.get_history_item(history_cursor)
                print_cmd(cmd)
                line_cursor = len(cmd)

            elif direction == b"P":  # down arrow pressed
                # get the NEXT command from history (if there is one)
                # prints out 'down' then erases it (just to show something)
                if history_cursor < History.get_current_history_length():
                    history_cursor += 1
                    cmd = History.get_history_item(history_cursor)
                print_cmd(cmd)
                line_cursor = len(cmd)
                # cmd = cmd[:-1]

            elif direction == b"M":  # right arrow pressed
                # move the cursor to the right on your command prompt line
                # prints out 'right' then erases it (just to show something)
                # print("\033[%dD" % (line_cursor),end="")
                if line_cursor < len(cmd):
                    line_cursor += 1

                # sys.stdout.write('\x1b[%dD'%(-1))

                print_cmd(cmd)
                #if len(cmd) - line_cursor != 0:
                    #sys.stdout.write("\x1b[%dD" % (len(cmd) - line_cursor))

                # cmd = cmd[:-1]

            elif direction == b"K":  # left arrow pressed
                # moves the cursor to the left on your command prompt line
                # prints out 'left' then erases it (just to show something)
                # sys.stdout.write('\x1b[1D')
                # print("\033[%dD" % ( line_cursor),end="")
                if line_cursor > 0:
                    line_cursor -= 1
                # sys.stdout.write('\x1b[%dD'%(1))

                print_cmd(cmd)

                #if len(cmd) - line_cursor != 0:
                    #print("\033[%d;%dH" % (9, line_cursor+2),end="")
                    #sys.stdout.write("\x1b[%dD" % (len(cmd) - line_cursor))

                # cmd = cmd[:-1]

            # print_cmd(cmd)                  # print the command (again)

        elif char == b"\r":  # return pressed
            # This 'elif' simulates something "happening" after pressing return
            # cmd = "Executing command...."   #
            print_cmd(cmd,cursor=False)

            # if the cmd (current user input) starts with an exclamation mark.
            if cmd.startswith("!"):
                # checks if the rest of the command is a valid positive integer.
                if cmd.strip("!").isnumeric():
                    # converts the numeric part of the command (without the "!") to an
                    # integer and stores t in "n".
                    # "n" is the index of a command in the command history.
                    n = int(cmd.strip("!"))
                    # n<= the current length of the command history.
                    if n <= History().get_current_history_length():
                        # If yes,retrieve the command from the command history using
                        # "get_history_item" method of the History object and
                        # assign it to the cmd variable.
                        cmd = History().get_history_item(n)
                        # set the line_cursor to the length of the new cmd string.
                        # Places cursor at the end of the history command.
                        line_cursor = len(cmd)
                    else:
                        # if not,it clears the cmd variable and prints an empty line
                        cmd = ""
                        print()

            else:
                print()
                try:
                    # parse the command string into a structured format and
                    # return it as a dictionary called struccmd
                    struccmd = splitcmd(cmd)
                    output = ""
                    for command in struccmd["commands"]:
                        # if the command has a "help" directive
                        if "help" in command["directives"]:
                            # If the "help" directive is found, it calls a method gethelp()
                            # help information for the given command.
                            output = cmdhelper.gethelp(command)
                        else:
                            # run the current command and give output
                            output = cmdhelper.run(command, output)
                    # check if the struccmd dictionary has an "appendFile" field,
                    # i.e.,the output should be appended to a file.
                    if struccmd["appendFile"] != "":
                        # if yes,open the specified file in append mode
                        # and write the output string to it.
                        with open(struccmd["appendFile"], "a") as f:
                            f.write(output)
                    # If not,check if the struccmd dictionary has a "writeFile" field,
                    # i.e.,the output should be written to a file.
                    elif struccmd["writeFile"] != "":
                        ##If "writeFile" field is present,open the specified file in
                        # write mode and write the output string to it.
                        with open(struccmd["writeFile"], "w") as f:
                            f.write(output)
                    # neither "appendFile" nor "writeFile" fields are present,
                    # check if the output string is not empty.Print output
                    elif output:
                        print(output)
                    # After processing the commands,log the current cmd into a historylog
                    # for future reference.
                    History.log(cmd)
                    # update the history_cursor to the position after the last command
                    history_cursor = History.get_current_history_length() + 1
                    # reset the cmd variable to an empty string and set line_cursor to 0 to reset the cursor position.
                    cmd = ""  # reset(since we just executed it)
                    line_cursor = 0
                except Exception as e:
                    # log the current cmd
                    History.log(cmd)
                    history_cursor = History.get_current_history_length() + 1

                    cmd = ""  # reset command to nothing (since we just executed it)
                    line_cursor = len(cmd)
                    # create an error message string Error_Msg by formatting the exception e
                    # with ANSI escape codes for red color (RED)
                    # and reset the color (RESET) to highlight the error message in red.
                    Error_Msg = f"{RED}{e}{RESET} "
                    # print the error message to the terminal.
                    print(Error_Msg)
            # call the print_cmd() function to print an empty command prompt,
            # clear the line for the next user input.
            print_cmd(cmd)  # now print empty cmd prompt

        # if no exception
        else:
            # update the cmd string by inserting the decoded character char,
            # at the current cursor position (line_cursor)
            # user input is added to the command line.
            cmd = cmd[:line_cursor] + char.decode() + cmd[line_cursor:]
            # history_cursor is updated to point to the end of the command history,
            history_cursor = History.get_current_history_length() + 1
            # line_cursor +1 to move the cursor position one step to the right.
            line_cursor += 1
            # print the updated cmd string with the new char added to the terminal.
            print_cmd(cmd)  # print the cmd out

            # move the cursor back to the correct position within the line if needed.
            #if len(cmd) - line_cursor != 0:
                # instruct the terminal to move the cursor left by 5 positions.
                #sys.stdout.write("\x1b[%dD" % (len(cmd) - line_cursor))

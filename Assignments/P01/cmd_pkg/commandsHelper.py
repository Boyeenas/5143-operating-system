import os,sys

from cmd_pkg.cmdLs import ls
from cmd_pkg.cmdPwd import pwd
from cmd_pkg.cmdMkdir import mkdir
from cmd_pkg.cmdCd import cd
from cmd_pkg.cmdCp import cp
from cmd_pkg.cmdMv import mv
from cmd_pkg.cmdRm import rm
from cmd_pkg.cmdRmdir import rmdir


from cmd_pkg.cmdCat import cat
from cmd_pkg.cmdHead import head
from cmd_pkg.cmdTail import tail


from cmd_pkg.cmdGrep import grep
from cmd_pkg.cmdWc import wc

from cmd_pkg.cmdSort import sort
from cmd_pkg.cmdWho import who


from cmd_pkg.cmdExit import exit
from cmd_pkg.cmdHistory import history

"""This line defines a new class named CommandsHelper"""
class CommandsHelper(object):
    """
    This function iterates over globals.items() and if one of the values is "callable"
    meaning it is a function, then I add it to a dictionary called 'invoke'. I also
    add the functions '__doc__' string to a help dictionary.

    Methods:
        exists (string) : checks if a command exists (dictionary points to the function)
        help (string) : returns the doc string for a function 
    """
    """
    It defines a class constructor (__init__) that initializes the invoke and help dictionaries.
      The global symbol table is traversed, with the exception of the 'Commands' symbol, and 
      callable functions or methods are added to the invoke dictionary while their docstrings are 
      kept in the help dictionary. This is a mechanism that is frequently used in command-line 
      interfaces or systems to link functions or methods with commands and offer documentation for them.
    """
    def __init__(self):
        self.invoke = {}
        self.help = {}

        for key, value in globals().items():
            if key != 'Commands' and callable(value):
                self.invoke[key] = value
                self.help[key] = value.__doc__
"""
 exists method is used to determine whether a given command (cmd) exists within 
 the context of the class, based on its presence as a key in the invoke attribute.
   It returns True if the command exists and False if it does not.
"""
    def exists(self,cmd):
        return cmd in self.invoke
    """
    It defines a method named run within a class. It expects two parameters:
      cmd, a dictionary defining a command to be executed, and data, some data required 
      for the command. The exists method is used first to determine whether the provided 
      command exists within the class. If the command is present, it tries to carry it 
      out by invoking the relevant function or method with the arguments and information supplied. 
      If the command is not understood, it raises an exception and displays an error message
     explaining the situation. This code is used to execute commands and deal with situations 
     in which an improper command is given.
    """
    def run(self,cmd,data):
        if self.exists(cmd["name"]):
            return self.invoke[cmd["name"]](params=cmd["params"],flags=cmd["flags"],data=data)
        else:
            com_name=cmd["name"]
            raise Exception(f"{com_name} is not recognized as an internal command")
        
    """
    It defines a method called 'gethelp' within a class. It takes a single parameter, 
    'cmd', this method checks if the specified command exists within the class using the
    'exists' method. If the command exists, it retrieves and returns the associated
    documentation or help information for that command from the 'help' dictionary. 
"""
    def gethelp(self,cmd):
        if self.exists(cmd["name"]):
            return self.help[cmd["name"]]
        



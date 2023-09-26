# Class Name: History
# Description:
# history tracking for storing and retrieving previously executed command strings,
# by index and find the total number of commands in history.


class History:
    value = []

    # create an instance of History,returns the class itself.
    def __new__(cls):
        return cls

    # to retrieve a history command string with index i
    # takes the class cls as  first parameter and i as its second parameter.
    # retrieve the command string at i-1
    # Return the command string at the specified index.
    @classmethod
    def get_history_item(cls, i):
        return cls.value[i - 1]

    # return the current length (number of commands).
    @classmethod
    def get_current_history_length(cls):
        return len(cls.value)

    # for adding a new command string to the history.
    # class "cls" is 1st parameter and the cmd (command string)is the 2nd parameter.
    # append the cmd to the list "value" ,and add it to the history.
    @classmethod
    def log(cls, cmd):
        return cls.value.append(cmd)

from sqliteCRUD import SQLiteCrud
from prettytable import PrettyTable
from datetime import datetime
from rich import print
from rich.box import SIMPLE
from rich.table import Table
from permission import convert_permission
import random

# This FileSystem class represents a file system,
# managing directories and files within an SQLite database.
# It offers methods for listing items, creating directories, changing permissions,
# and handling file operations like copying, moving, and removing.
# navigate the file system with a cd method and view the current directory with pwd.


class FileSystem:
    def __init__(self, db_name=None):
        if not db_name:
            self.db_name = "filesystem.sqlite"
        else:
            self.db_name = db_name
        self.crud = SQLiteCrud(db_name)
        self.cwd = "/home/user"
        self.cwdid = 0
        self.pwdid = 0
        self.hidden = None

    # GetFileID Description:
    # The `__getFileId` method is for obtaining the file or folder ID based on a provided path
    # relative to the current working directory.
    # 1.`path (str)`: The path for which you want to determine the corresponding file or folder ID.
    # The method begins with the current working directory ID (`self.cwdid`) and iterates
    # through the path components. It handles relative paths (e.g., `./` and `..`)
    # and searches for matching file or folder entries in the "files_data" table within
    # the database. If a match is found, it updates the current path ID accordingly.
    # If the provided path leads to a file or folder, it returns the corresponding ID.
    # If not found or an error occurs, it returns `None`.
    # This method is crucial for navigating and identifying files and folders within the database structure.

    def __getFileId(self, path):
        cur_path_id = self.cwdid
        if path.startswith("./") or path == ".":
            path = path[1:].strip("/")

        for folder in path.split("/"):
            if folder == "..":
                prevfile = self.crud.search("files_data", {"id": cur_path_id})
                if prevfile:
                    cur_path_id = prevfile[0][1]
                else:
                    return None
                continue
            files = self.crud.search("files_data", {"name": folder, "pid": cur_path_id})
            if files:
                cur_path_id = files[0][0]
            else:
                return None
        return cur_path_id

    """
    This function mimicks the ls command.First the data is retrived from the file_data in the database we have created 
    using the search method and the needed columns have been added.Now the data has been added to the created columns and 
	prints to the console as output
	"""

    def list(self, a=False):
        # Getting the parent id from the current working directory
        conditions = {"pid": str(self.cwdid)}
        files = self.crud.search("files_data", conditions)
        # Imported Table from rich where it helps print the data in a table like format
        table = Table(show_header=True, header_style="bold blue", box=SIMPLE)
        table.add_column("Filename", style="dim", width=20)
        table.add_column("Owner", width=10)
        table.add_column("Permissions", width=12)
        table.add_column("Size", justify="right")
        table.add_column("Hidden", justify="right")
        # Iterating over each file and getting the size from the table in database
        for file in files:
            # self.size = f'{random.randint(1,20)} KB'
            size = file[5]
            # if size == 0:
            #     size = f'{0} KB'
            # else:
            # The size retrived from the files_data is converted to Kb to be human readable mimicking the ls -h command here
            sizes_in_kb = float(size) / 1024.0
            size = f"{sizes_in_kb:.1f} KB"
            # check is made to see if the current file is hidden file or not if it is the hidden column in the data base
            # table sets to true otherwise false
            self.hidden = file[2].startswith(".")
            self.hidden = "True" if self.hidden else "False"
            # This mimicks the command ls -a where it will print the hidden files to the console when the a is true other
            # -wise all the files except for the hidden files will be printed as output
            if a or not file[2].startswith("."):
                table.add_row(file[2], file[7], file[-1], str(size), self.hidden)

            # if h:
            #     table.add_row(file[2], file[7], file[-1], str(self.result),self.hidden)
        print(table)

    """
    This function mimicks the command mk dir by creating a new directory and the created folder will be pushed to the 
	table in the data base  
    """

    def make_directory(self, name):
        self.hidden = name.startswith(".")
        self.hidden = "True" if self.hidden else "False"
        # Generating a random number to be pushed into the table for the size of a file/dir
        size = random.randint(1000, 3000)
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.crud.insert_data(
            "files_data",
            (
                None,
                self.cwdid,
                name,
                current_datetime,
                current_datetime,
                size,
                "directory",
                "user",
                "group",
                self.hidden,
                "rwxr-xr-x",
            ),
        )
        print(f"[bold green]Folder '{name}' created.[/bold green]")

    # The method first obtains the ID of the file or directory using the private __getFileId
    # method. Then, it converts the human-readable permission string into a format suitable
    # for the database using the convert_permission function.
    # Finally, it updates the permissions for the specified file or directory in the
    # "files_data" table, ensuring that the permissions are adjusted as per the provided input.
    # This method is crucial for managing access control within the database's file structure.
    def chmod(self, path, permission):
        pathid = self.__getFileId(path)
        newper = convert_permission(permission)
        self.crud.update_data("files_data", "permissions", newper, "id", pathid)

        """ Change the permissions of a file
            1) will need the file / folder id

            2) select permissions from the table where that id exists
            3) 
        Params:
            id (int) :  id of file or folder
            permission (string) : +x -x 777 644

            if its a triple just overwrite or update table 

        Example:
            +x 
            p = 'rw-r-----'
            p[2] = x
            p[5] = x
            p[8] = x
        """
        pass

    # PWD:
    # The pwd function uses text formatting tags like [bold cyan] and [green]
    # to style and color the current directory path when printing it.
    # It presumes that a self.cwd attribute exists that contains the directory
    # path and is probably meant to be used in a setting that permits text
    # formatting, like a command-line interface or terminal with a library
    # like rich.
    def pwd(self):
        print(f"[bold cyan]Current Directory:[/bold cyan] [green]{self.cwd}[/green]")

    # copy method is used to copy a file or directory from frompath to topath.
    # It checks to see if the source file or directory already exists;
    # if not, an error message is printed.
    # The target file or directory name is then extracted from topath, and the
    # ID of the parent directory is then retrieved.
    def copy(self, frompath, topath):
        fromfile_id = self.__getFileId(frompath)
        if fromfile_id is None:
            print(
                f"[bold red]Error: Source file or directory '{frompath}' not found.[/bold red]"
            )
            return

        topathname = topath.strip("/").split("/")[
            -1
        ]  # Extract the target file/directory name

        topath_id = self.__getFileId("/".join(topath.strip("/").split("/")[:-1]))

        # Check if the target file/directory already exists
        if topath_id is None:
            print(
                f"[bold red]Error: Target  directory '{topath}' not exists.[/bold red]"
            )
            return

        # Fetch the source file/directory details
        source_data = self.crud.search("files_data", {"id": fromfile_id})

        if source_data:
            source_data = list(source_data[0])
            source_data[0] = None  # Set the ID to None to create a new entry
            source_data[
                1
            ] = topath_id  # Set the parent directory to the current directory
            source_data[2] = topathname  # Set the new name
            self.crud.insert_data("files_data", source_data)

            # Notify the user about the successful copy operation
            target_path = topath if topath != "." else "current directory"
            print(
                f"[bold green]File or folder '{frompath}' copied to {target_path}.[/bold green]"
            )
        else:
            print(
                f"[bold red]Error: Source file or directory '{frompath}' not found.[/bold red]"
            )

    ##Move:
    # It obtains the source file or directory's ID and its filename from the
    # given frompath and  retrieves the target directory's ID based on the
    # todirectory.
    # The code searches the system's database for the file or directory entry
    # and, if it is located, updates its record to reflect the transfer to the
    # new directory and inserts this modified record into the database.
    # The original file or directory record is then deleted from the old location.
    # A message is printed, notifying the user that the file specified by frompath
    # has been successfully moved to either the "current directory" or the specified
    # target directory, with green text formatting.

    def move(self, frompath, todirectory):
        fromid = self.__getFileId(frompath)
        filename = frompath.split("/")[-1]

        toid = self.__getFileId(todirectory)

        files = self.crud.search("files_data", {"id": fromid})
        if files:
            file = list(files[0])
            file[0] = None
            file[1] = toid
            file[2] = filename
            self.crud.insert_data("files_data", file)
            self.crud.delete_data("files_data", "id", files[0][0])
            path = todirectory
            if path == ".":
                path = "current directory"
            print(f"[bold green]File '{frompath}' moved to {path}.[/bold green]")

    # Remove Description:
    # The method iterates through the provided paths, obtaining their corresponding IDs
    # using the private __getFileId method. It then calls the delete_data method to remove
    # these files or folders from the "files_data" table within the database.
    # After successfully removing all specified paths,
    # it generates a message indicating which files were removed and
    # prints this message in green text. This method provides a way to delete files
    # and folders from the database, keeping the file structure in sync with the
    # database records.
    def remove(self, paths):
        for path in paths:
            pathid = self.__getFileId(path)

            self.crud.delete_data("files_data", "id", pathid)
            msg = " , ".join(paths)
        print(f"[bold green]Files '{msg}' removed.[/bold green]")

    # CD Description:
    # The `cd` method facilitates directory navigation within a database-stored file structure:
    # 1. If the provided path is ".." and the current directory isn't the root (ID not 0),
    # it moves up one level, adjusting the current and parent directory paths and IDs.
    # 2. For non-".." paths, it searches for a directory with the given name in the
    # current directory's subdirectories.
    # 3. If found, it updates the current directory path, ID, and the parent directory ID.
    # This method allows users to navigate through the database's directory structure,
    # maintaining their current working directory.
    def cd(self, path):
        if path == "..":
            if self.cwdid != 0:
                self.cwd = "/".join(self.cwd.split("/")[:-1])
                self.cwdid = self.pwdid
                if self.cwdid != 0:
                    folder = self.crud.search(
                        "files_data", {"id": self.cwdid, "type": "directory"}
                    )

                    self.pwdid = folder[0][1]
                else:
                    self.pwdid = 0
        else:
            folder = self.crud.search(
                "files_data", {"name": path, "pid": self.cwdid, "type": "directory"}
            )
            if folder:
                self.cwd += "/" + folder[0][2]
                self.cwdid = folder[0][0]
                self.pwdid = folder[0][1]

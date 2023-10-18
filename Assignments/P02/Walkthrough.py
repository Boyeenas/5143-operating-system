####################################################
#  ____             _____         ______    _____  #
# |       |  |    |      |       |      |  |       #
# |____   |  |____| _____|  ___  |      |  |_____  #
#      |  |       |      |       |      |        | #
# _____|  |       | _____|       |______|   _____| #
#                                                  #
####################################################

####################################################
#       _____           _____      ______          #
#      |     |         |     |           |         #
#      |_____|  _____  |     |      _____|         #
#      |               |     |     |               #
#      |               |_____|     |______         #
#                                                  #
####################################################

########################################################
#        ***IMPLEMENTATION OF A :*****                 #
#                                                      #
#     ******  *  *      ******* *******       * *****  #
#     *       *  *      *       *      *     *  *      #
#     *       *  *      *       *       *   *   *      #
#     ******  *  *      ******* ******   * *    *****  #
#     *       *  *      *            *    *         *  #
#     *       *  *      *            *    *         *  #
#     *       *  ****** ******* ******    *     *****  #
########################################################

####################################################
#                                                  #
# *TEAM MEMBERS:*                                  #
# 1. Divya Podila                                  #
# 2. Soundarya Boyeena                             #
# 3. Rakesh Rapalli                                #
#                                                  #
####################################################

# Import necessary Modules
import csv
from sqliteCRUD import *
import time
from rich import print
from rich.table import Table
from rich.box import SIMPLE
from fileSystem import FileSystem
from rich.console import Console
import random

# table name
table_name = "files_data"
# columns in the table with datatypes
columns = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "pid INTEGER",
    "name TEXT",
    "created_date TEXT",
    "modified_date TEXT",
    "size INTEGER",
    "type TEXT",
    "owner TEXT",
    "groop TEXT",
    "Hidden TEXT",
    "permissions TEXT",
]
# Load table
data = []
with open("file-sys-primer-data.csv", "r") as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    # Iterate over each row in the CSV file
    for row in csv_reader:
        # size = row[5]
        size = random.randint(1000, 3000)
        # size=round(randint(35,1110))
        hidden = row[2].startswith(".")
        hidden = "True" if hidden else "False"

        data.append(
            (
                row[4],
                row[5],
                row[1],
                row[6],
                row[7],
                size,
                row[0],
                row[2],
                row[3],
                hidden,
                row[-1],
            )
        )

# database name
dbname = "testfilesystem.sqlite"
# connect to SQLite crud
conn = SQLiteCrud(dbname)
# drop previously created tables if any
conn.drop_table(table_name)
# create table and describe it
conn.create_table(table_name, columns)
conn.describe_table(table_name)

for row in data:
    conn.insert_data(table_name, row)


fs = FileSystem(dbname)

# Dummy data for the example
current_directory = "/home/user"

# Demonstrate the commands
print("[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
fs.list(a=True)


print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()

Console().clear()
print("\n[bold blue]Command:[/bold blue] [green]mkdir newfolder[/green]")
fs.make_directory("newfolder")

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
fs.list(a=True)


print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()

Console().clear()
print("\n[bold blue]Command:[/bold blue] [green]cd newfolder[/green]")
fs.cd("newfolder")
fs.pwd()

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
fs.list(a=True)

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()

Console().clear()
print("\n[bold blue]Command:[/bold blue] [green]cd ..[/green]")
fs.cd("..")
fs.pwd()

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
fs.list(a=True)

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()

Console().clear()
print("\n[bold blue]Command:[/bold blue] [green]cd win2k[/green]")
fs.cd("win2k")
fs.pwd()

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
fs.list(a=True)

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()

Console().clear()
print("\n[bold blue]Command:[/bold blue] [green]cd shell[/green]")
fs.cd("shell")
fs.pwd()

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()

print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
fs.list(a=True)

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()

Console().clear()
print("\n[bold blue]Command:[/bold blue] [green]cp StdAfx.c ../Ax.c[/green]")
fs.copy("StdAfx.c", "../Ax.c")

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]cd ..[/green]")
fs.cd("..")
fs.pwd()

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
fs.list(a=True)

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


Console().clear()
print("\n[bold blue]Command:[/bold blue] [green]cd tools[/green]")
fs.cd("tools")
fs.pwd()

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
fs.list(a=True)

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()

Console().clear()
print("\n[bold blue]Command:[/bold blue] [green]mv ../Ax.c trapper[/green]")
fs.move("../Ax.c", "trapper")

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]cd trapper[/green]")
fs.cd("trapper")
fs.pwd()

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
fs.list(a=True)

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()

Console().clear()
print("\n[bold blue]Command:[/bold blue] [green]rm Ax.c process_trap.c[/green]")
fs.remove(["Ax.c", "process_trap.c"])

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
fs.list(a=True)

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()

Console().clear()
print("\n[bold blue]Command:[/bold blue] [green]chmod 467 tests[/green]")
fs.chmod("tests", 467)

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
fs.list(a=True)

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()

Console().clear()
print("\n[bold blue]Command:[/bold blue] [green]mkdir newfolder[/green]")
fs.make_directory(".sampleHidden1")

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]mkdir newfolder[/green]")
fs.make_directory(".sampleHidden2")

print()
print("[bold blue]Press enter to continue[/bold blue]")
prompt = input()


print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
fs.list(a=True)

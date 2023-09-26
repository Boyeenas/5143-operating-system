#### 5143-P01
#### 5143 Shell Project 

#### Group Members

- Rakesh Rapalli
- Divya podila
- soundarya boyeena

#### Overview:
This is a project written in python that implements a basic shell where it runs most of the commands that a shell does.
when you run the shell.py it will ask you for the prompt, there we can give the commands like ls, wc, mkdir and more then based on the commands given, the output will be printed to the terminal.


#### Instructions

import all the packages

Then run the shell.py

For help, type commandName --help


# How to run commands:

1. ls:
   
-> ls -l

-> ls -a 

-> ls -h

-> ls -lah

2.Mkdir:

-> cd P01Final

-> mkdir test

-> ls 

3. cd:
   
-> cd cmd_pkg

->pwd

C:\Users\divya\OS\P01Final\cmd_pkg

4.cd ~ :

->cd ~

->pwd

C:\Users\divya

5. cd .. :
   
-> cd ..

->pwd

C:\Users

7. cp :
   
-> cp cmd_pkg sample

a copy of cmd_pkg should be created with the name of sample.

9. mv:
    
-> mv sample sample1

sample folder gets deleted (same as renaming it to sample1)

11. rm:
    
-> rm cmdCat.py

cmdCat.py is deleted

13. rm -r : (recursive)
    
-> rm -r sample

deletes entire directory with all the contents

15. rm file* / *file /fi*e.py:
    
-> rm sample/cmd*.py

-> rm sample/*.py : every .py will get deleted

-> rm sample/R* : Readme will get deleted

17. rmdir:
    
-> rmdir sample

   won't delete sample has contents in it
   
-> so, mkdir test

-> rmdir test

   delete the directory test as it doesn't have any contents.

19. cat:
    
-> cat cmdCat.py cmdCd.py

Gives contents of both the files int the terminal

-> cat cmdCat.py cmdCd.py > out.py

both files contents will be displayed in a new file called OUT

13. Head:
    
->head cmdCat.py

Prints first 10 lines of the file

15. Tail:
    
-> Tail cmdCat.py

Last 10 lines

17. Grep:
    
-> grep cat cmdCat.py

prints all the lines that has cat keyword in the mentioned file

->grep -l cat cmdCat.py cmdCd.py

cmdCat.py

returns only file names that ha cat keyword

16. wc:

->wc cmdCat.py

Lines,words,characters(m) :45 455 1229

->wc -l cmdCat.py

Gives 45

->wc -w cmdCat.py

455

->wc -m cmdCat.py

1229

18. redirect std out > :
    
->ls > out.py

18.redirect std in < :

-> head < cmdCat.py

first 10 lines of a file will be read and printed

19. redirect append >> :
    
-> ls >> out.py

Appends contents to the end of file

->wc getch.py

37 273 843

-> wc getch.py >> out.py

appends wc into out.py

21. Pipe | :
    
-> ls | wc

-> ls | sort

sorts output of ls (ASCII)

-> ls | sort cmdCat.py > out.py 

23. Who:
    
returns current user logged in

25. history
    
prints history

27. !linenumber :
    
!161 returns 161st command from history list. We can run the command again from there.


***Commands***:

![whodidwhat](https://github.com/divyapodila/5143-P01/assets/123696771/5e6d9f09-aabf-4bc8-b884-20ded6d87109)



***Non Working Components***

Not implemented:

1. chmodxxx : Permissions
-> Last minute - couldnt work on it before deadline

2. Less :
-> Found it difficult to implement
-> How to make it print per page
   
3. head -n filename & tail -n filename:

-> Needed parsing level changes. Thought it would disturb the current parsing of commands. Last minute - could'nt implement before the     deadline.


***References***

- For cursor position left and right
  
 https://stackoverflow.com/questions/5174810/how-to-turn-off-blinking-cursor-in-command-window#:~:text=Just%20use%20print('%5C033,%2C%20end%3D%22%22)%20

- For ANSII color codes

  https://codehs.com/tutorial/andy/ansi-colors

- For shutil module

 https://www.geeksforgeeks.org/delete-an-entire-directory-tree-using-python-shutil-rmtree-method/


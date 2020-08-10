import os
from .io import Colors

# print banner
print(Colors.tangerine, Colors.bold, end="", sep="")
print("Course Registration Tool 1.3")
print(Colors.brick, end="", sep="")
print("""License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.""")
print(Colors.reset)


# go to root directory
os.chdir(os.path.join(os.getcwd(), '..'))

# create directories if they don't exist
if not os.path.isdir('config'):
    os.mkdir('config')
if not os.path.isdir('logs'):
    os.mkdir('logs')
# create files if they don't exist
files = [os.path.join('config','config.json'), os.path.join('config','ifttt.key'), os.path.join('logs','register.log')]
for file in files:
    with open(file, 'a+') as f:
        pass

# import logging after files have been created
from .logging import logger
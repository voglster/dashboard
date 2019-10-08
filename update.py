import os


os.system("git fetch")
update_available = "behind" in os.popen("git status").read()

if update_available:
    os.system("supervisorctl stop qboard")
    os.system("git pull")
    os.system("supervisorctl start qboard")

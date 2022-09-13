from os import system
from time import sleep

t = 25 * 60  # 25 minutes

sleep(t)
system("touch works")
system("killall psi")

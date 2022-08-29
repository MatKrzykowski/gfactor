from os import system
from time import sleep

t = 25 * 60  # 40 minutes

sleep(t)
system("touch works")
system("killall psi")
# system("killall python && killall psi")
# system("echo Done >> log")

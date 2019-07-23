import subprocess
import time

while True:
    proc = subprocess.Popen("python3 main.py", shell=True) # for some reason this avoids a bug where the bot doesn't play anything when not started from a shell
    proc.communicate()
    print("Process ended. Restarting in 5s...")
    time.sleep(5)
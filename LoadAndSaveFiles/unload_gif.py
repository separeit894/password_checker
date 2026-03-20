import os
from core import CheckingExeOrCode
def UnloadGif():
    gif_path = CheckingExeOrCode()
    if gif_path.exists():
        with open(gif_path, "rb") as fileRead:
            src = fileRead.read()
            print(f"Файл {gif_path} прочитан")
            
        with open("how_to_disable_the_lock_threshold.gif", "wb") as fileWrite:
            fileWrite.write(src)
            print(f"Файл записан")
    
    
if __name__ == "__main__":
    UnloadGif()
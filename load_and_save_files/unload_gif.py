from core import checking_exe_or_code
import os

HOW_TO_DISABLE_THE_LOCK_THRESHOLD="how_to_disable_the_lock_threshold.gif"

def unload_gif():
    gif_path = checking_exe_or_code()
    if gif_path.exists():
        with open(gif_path, "rb") as fileRead:
            src = fileRead.read()
            print(f"Файл {gif_path} прочитан")

        with open(HOW_TO_DISABLE_THE_LOCK_THRESHOLD, "wb") as fileWrite:
            fileWrite.write(src)
            print("Файл находится в текущей директории")


if __name__ == "__main__":
    unload_gif()

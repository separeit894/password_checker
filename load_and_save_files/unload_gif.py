from core import checking_exe_or_code

HOW_TO_DISABLE_THE_LOCK_THRESHOLD="how_to_disable_the_lock_threshold.gif"

def unload_gif():
    gif_path = checking_exe_or_code()
    if gif_path.exists():
        with open(gif_path, "rb") as fileRead:
            src = fileRead.read()
            print(f"[+] File {gif_path} read")

        with open(HOW_TO_DISABLE_THE_LOCK_THRESHOLD, "wb") as fileWrite:
            fileWrite.write(src)
            print("--> File in current directory")


if __name__ == "__main__":
    unload_gif()

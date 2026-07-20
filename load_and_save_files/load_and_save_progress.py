import json
import os


# Save Progress
def save_progress(username, print_try, characters, length, try_id, tryed, mask=None,wordlist=None,):
    from core import (
        get_file,
        get_encoding
    )
    
    PROGRESS_FILE = get_file()
    MY_ENCODING = get_encoding()

    with open(PROGRESS_FILE, "w", encoding=MY_ENCODING) as f:
        json.dump(
            {
                "username": username,
                "print_try": print_try,
                "characters": characters,
                "mask": mask,
                "wordlist": wordlist,
                "length": length,
                "try_id": try_id,
                "tryed": tryed,
            },
            f,
            indent=4,
        )


# Load Progress
def load_progress():
    try:
        from core import (
            get_encoding,
            get_file
        )
        
        PROGRESS_FILE = get_file()
        MY_ENCODING=get_encoding()

        # if file with progress, that takes his value
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "r", encoding=MY_ENCODING) as f:
                return json.load(f)
        else:
            if not os.path.isfile(PROGRESS_FILE):
                # if File not found -> file create
                with open(PROGRESS_FILE, "w", encoding=MY_ENCODING) as f:
                    json.dump({}, f, indent=4)  
                print(f"[+] File '{PROGRESS_FILE}' was create.\n")
                return False

    except FileNotFoundError:
        print(f"[-] File {PROGRESS_FILE} not found.")
        return False
    except json.JSONDecodeError as e:
        print(f"[-] Error decoding JSON: {e}")
        return False


if __name__ == "__main__":
    save_progress()
    load_progress()

import sys

from pathlib import Path

# Constants

MY_ENCODING = "utf-8"
PROGRESS_FILE = "progress.json"

# Logon32

LOGON32_LOGON_INTERACTIVE = 2
LOGON32_PROVIDER_DEFAULT = 0

# Encoding

def set_encoding(encoding):
    global MY_ENCODING
    MY_ENCODING = encoding

def get_encoding():
    return MY_ENCODING

# Filename Progress

def set_file(filename):
    global PROGRESS_FILE
    PROGRESS_FILE = filename
    
def get_file():
    return PROGRESS_FILE

# For stable gif file upload

def checking_exe_or_code() -> str:
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
        print(f"EXE BASE_PATH : {base_path}")
        gif_path = base_path / "assets" / "how_to_disable_the_lock_threshold.gif"
    else:
        base_path = Path(__file__).parent
        print(f"CODE BASE_PATH : {base_path}")

        gif_path = base_path / ".." / "assets" / "how_to_disable_the_lock_threshold.gif"

    return gif_path


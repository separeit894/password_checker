import sys
from pathlib import Path

MY_ENCODING = "utf-8"
PROGRESS_FILE = "progress.json"

LOGON32_LOGON_INTERACTIVE = 2
LOGON32_PROVIDER_DEFAULT = 0


def set_encoding(encoding):
    global MY_ENCODING
    MY_ENCODING = encoding


def set_file(filename):
    global PROGRESS_FILE
    PROGRESS_FILE = filename


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


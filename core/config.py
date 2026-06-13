import sys

from pathlib import Path

# Constants

MY_ENCODING = "utf-8"
PROGRESS_FILE = "progress.json"

# Console Encoding

console_encoding = None

def set_console_encoding(value: str):
    global console_encoding
    from .encodings_console import get_dict_windows_code
    Windows_Code = get_dict_windows_code()
    console_encoding = MY_ENCODING
    
    find_code_encoding_console = False
    
    for k, v in Windows_Code.items():
        if v == value:
            print(f"[+] Значения совпадают: {v}")
            console_encoding = k
            find_code_encoding_console = not find_code_encoding_console
    
    if not find_code_encoding_console:
        print("[-] Кодировка не найдена!")
        sys.exit(1)
    

def get_console_encoding():
    return console_encoding

# Dict Windows Page

def get_key_and_value_dict_windows_code_console():
    from .encodings_console import get_dict_windows_code
    Windows_Code = get_dict_windows_code()
    print(f"{'KEY':<6}: VALUE")
    for key, value in Windows_Code.items():
        print(f"{key:<6}: {value}")
        
    sys.exit(0)

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

exec_command_powershell = True

def set_exec_command_powershell(value: bool):
    global exec_command_powershell
    exec_command_powershell = value

def get_exec_command_powershell() -> bool:
    return exec_command_powershell

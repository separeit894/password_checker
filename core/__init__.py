from .config import (
    LOGON32_LOGON_INTERACTIVE,
    LOGON32_PROVIDER_DEFAULT,
    checking_exe_or_code,
    set_encoding,
    set_file,
    get_encoding,
    get_file,
    get_exec_command_powershell,
    set_exec_command_powershell,
    set_console_encoding,
    get_key_and_value_dict_windows_code_console
)

VERSION = "5.5.3"

from .list_users import list_users as list_users

from ctypes import wintypes
import ctypes

# Function, which work with cyrillic 
LogonUser = ctypes.windll.advapi32.LogonUserW
LogonUser.argtypes = (
    wintypes.LPCWSTR,  # username
    wintypes.LPCWSTR,  # domain
    wintypes.LPCWSTR,  # password
    wintypes.DWORD,  # Input type
    wintypes.DWORD,  # Provider
    ctypes.POINTER(wintypes.HANDLE),  # Token
)

__all__ = [
    "LOGON32_LOGON_INTERACTIVE", 
    "LOGON32_PROVIDER_DEFAULT", 
    "checking_exe_or_code", 
    "list_users", 
    "set_encoding", 
    "set_file", 
    "get_file",
    "get_encoding", 
    "LogonUser",
    "VERSION",
    "get_exec_command_powershell",
    "set_exec_command_powershell",
    "set_console_encoding",
    "get_key_and_value_dict_windows_code_console"
]
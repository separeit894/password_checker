from .config import (
    LOGON32_LOGON_INTERACTIVE,
    LOGON32_PROVIDER_DEFAULT,
    checking_exe_or_code,
    set_encoding,
    set_file,
    get_encoding,
    get_file
)

from .list_users import list_users as list_users

from ctypes import wintypes
import ctypes

# Эта функция потребуется для того, чтобы консоль могла работать с кирилицей
LogonUser = ctypes.windll.advapi32.LogonUserW
LogonUser.argtypes = (
    wintypes.LPCWSTR,  # Имя пользователя
    wintypes.LPCWSTR,  # Домен
    wintypes.LPCWSTR,  # Пароль
    wintypes.DWORD,  # Тип входа
    wintypes.DWORD,  # Провайдер
    ctypes.POINTER(wintypes.HANDLE),  # Токен
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
    "LogonUser"
]
from .config import MY_ENCODING, PROGRESS_FILE, CheckingExeOrCode,set_encoding, set_file
from .list_users import list_users

from ctypes import wintypes
import ctypes

# Эта функция потребуется для того, чтобы консоль могла работать с кирилицей
LogonUser = ctypes.windll.advapi32.LogonUserW
LogonUser.argtypes = (
    wintypes.LPCWSTR,  # Имя пользователя
    wintypes.LPCWSTR,  # Домен
    wintypes.LPCWSTR,  # Пароль
    wintypes.DWORD,    # Тип входа
    wintypes.DWORD,    # Провайдер
    ctypes.POINTER(wintypes.HANDLE)  # Токен
)
import ctypes
import win32api

from core import (
    LogonUser,
    LOGON32_LOGON_INTERACTIVE,
    LOGON32_PROVIDER_DEFAULT,
)


def authentificate_user(username: str, password: str):
    try:
        token = ctypes.c_void_p()  # Создаем токен
        result: bool = LogonUser(
            username,
            None,  # Локальная учетная запись
            password,
            LOGON32_LOGON_INTERACTIVE,
            LOGON32_PROVIDER_DEFAULT,
            ctypes.byref(token),
        )

        if not result:
            raise Exception()
        else:
            print(f"[+] Аутентификация пользователя {username} по паролю {password} прошла успешно.")


    except:
        print(f"[-] Ошибка аутентификации : {win32api.GetLastError()}")


if __name__ == "__main__":
    username = input("Enter name : ")
    password = input("Enter password : ")
    user_token = authentificate_user(username, password)

import ctypes
import win32api

from core import (
    LogonUser,
    LOGON32_LOGON_INTERACTIVE,
    LOGON32_PROVIDER_DEFAULT,
)


def authentificate_user(username: str, password: str):
    try:
        token = ctypes.c_void_p()  # Create token
        result: bool = LogonUser(
            username,
            None,  # Local account
            password,
            LOGON32_LOGON_INTERACTIVE,
            LOGON32_PROVIDER_DEFAULT,
            ctypes.byref(token),
        )

        if not result:
            raise Exception()
        else:
            print(f"[+] User authentication {username} by password {password} It went successfully.")


    except:
        print(f"[-] Error authentication : {win32api.GetLastError()}")


if __name__ == "__main__":
    username = input("Enter name : ")
    password = input("Enter password : ")
    user_token = authentificate_user(username, password)

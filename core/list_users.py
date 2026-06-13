import subprocess
import sys

from .encodings_console import get_encoding_name

run_learn_encoding = None

def list_users():
    global run_learn_encoding
    try:
        user_list = []

        
        run_learn_encoding = subprocess.run(
            ["cmd", "/c", "chcp"], capture_output=True, text=True, check=True
        )
        result_learn_encoding = run_learn_encoding.stdout.split(": ")[1].split("\n")[0]
        
        from .config import get_console_encoding
        console_encoding = get_console_encoding()
        if console_encoding is None:
            result_learn_name_encoding = get_encoding_name(int(result_learn_encoding))
        else:
            result_learn_encoding = int(console_encoding)
            result_learn_name_encoding = get_encoding_name(int(console_encoding))
        
        UPPER_PRINT = f"[IMPORTANT INFO] The encoding used: {result_learn_encoding} : {result_learn_name_encoding}".upper()
        print(UPPER_PRINT)
        
        from .config import get_exec_command_powershell
        if get_exec_command_powershell():
            result = subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Get-WmiObject",
                    "-Class Win32_UserAccount",
                    '-Filter "LocalAccount=True" | Select-Object Name',
                ],
                capture_output=True,
                text=True,
                check=True,
                encoding=result_learn_name_encoding,
                errors="ignore",
            )

            # получаем список пользователей
            res_print = result.stdout.strip()
            # Разделяем по слову, получая из этого список
            res_print_splt = res_print.splitlines()

            """
            Этот цикл нужен для того чтобы проверить есть ли пользователь 
            у которого внутри имени есть пробел по типу 'test user'
            если да, то он добавляет его в список 
            """

            for re in res_print_splt[2:]:
                cleaned_line = re.strip()

                words = cleaned_line.split("\n")

                clean_word = []
                for word in words:
                    clean_word.append(word)

                # Добавляем в список уже имена
                user_list.extend(clean_word)
            # Возвращаем конечный список пользователей
            return user_list
        
        else:
            # Выполняем через net user
            result = subprocess.run(
                [
                    "cmd",
                    "/c",
                    "net",
                    "user"
                ],
                capture_output=True,
                text=True,
                check=True,
                encoding=result_learn_name_encoding,
                errors="ignore",
            )
            print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        sys.exit()


if __name__ == "__main__":
    list_users()

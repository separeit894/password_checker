import subprocess
import sys

from .encodings_console import get_encoding_name

# Функция, которая будет брать список пользователь в Windows
def list_users():
    try:
        user_list = []
        # Выполняем команду net user
        
        encoding_result = subprocess.run(['cmd', '/c', 'chcp'], capture_output=True, text=True, check=True)
        res = encoding_result.stdout.split(": ")[1].split("\n")[0]
        res_name = get_encoding_name(int(res))
        print(f"encoding result: {res}, {res_name}")
        
        result = subprocess.run(['powershell', '-Command', 'net user'], capture_output=True, text=True, check=True, encoding=res_name, errors="ignore")
        
        # получаем список пользователей
        res_print = result.stdout.strip()
        # Разделяем по слову, получая из этого список
        res_print_splt = res_print.splitlines()
        

        """
        Этот цикл нужен для того чтобы проверить есть ли пользователь 
        у которого внутри имени есть пробел по типу 'test user'
        если да, то он добавляет его в список 
        """
        for re in res_print_splt[3:-1]:
            cleaned_line = re.strip()

            words = cleaned_line.split()

            combined_words = []
            i = 0
            while i < len(words):
                if i < len(words) - 1 and words[i] + ' ' + words[i + 1] in cleaned_line:
                    combined_words.append(words[i] + ' ' + words[i + 1])  # Объединяем два слова
                    i += 2  # Пропускаем следующее слово
                else:
                    combined_words.append(words[i])  # Добавляем текущее слово
                    i += 1
            print(re)   

            # Добавляем в список уже имена с пробелами
            user_list.extend(combined_words)
        # Возвращаем конечный список пользователей
        return user_list

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        sys.exit()


if __name__ == "__main__":
    list_users()

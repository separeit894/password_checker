import subprocess
import sys


def list_users():
    try:
        user_list = []
        # Выполняем команду net user
        result = subprocess.run(['net', 'user'], capture_output=True, text=True, check=True, encoding="866")
        # Выводим результат
        res_print = result.stdout
        res_print_splt = res_print.splitlines()


        for re in res_print_splt[4:-2]:
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

            user_list.extend(combined_words)

        return user_list

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        sys.exit()


if __name__ == "__main__":
    list_users()

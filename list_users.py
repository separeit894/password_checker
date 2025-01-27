import subprocess
import sys


def list_users():
    try:
        user_list = """"""
        # Выполняем команду net user
        result = subprocess.run(['net', 'user'], capture_output=True, text=True, check=True, encoding="866")
        # Выводим результат
        print(result.stdout)

        for re in result.stdout:
            user_list += re

        return user_list

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        sys.exit()


if __name__ == "__main__":
    list_users()

import subprocess
import sys

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

        return user_list

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        sys.exit()


if __name__ == "__main__":
    list_users()

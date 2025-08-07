import json
import os
import sys

from .config import MY_ENCODING


progress_file = "progress.json"
# Функция для сохранения прогресса
def save_progress(account, characters, length, try_id, tryed):
    with open(progress_file, 'w', encoding=MY_ENCODING) as f:
        json.dump(
            {
                "account": account,
                'print_try': "y",
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
        # Если файл с прогрессом существует, то он возвращает данные из этого файла
        if os.path.exists(progress_file):
            with open(progress_file, 'r', encoding=MY_ENCODING) as f:
                return json.load(f)
        else:
            if not os.path.isfile(progress_file):
                # Если файл не существует, создаем его с пустым объектом
                with open(progress_file, 'w') as f:
                    json.dump({}, f, indent=4)  # Записываем пустой объект в файл
                # print(f"Файл '{progress_file}' был создан.")

    except FileNotFoundError:
        print("Файл 'progress.json' не найден.")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return None
    return None

if __name__ == "__main__":
    save_progress()
    load_progress()
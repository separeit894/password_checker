import json
import os


progress_file = "progress.json"
# Функция для сохранения прогресса
def save_progress(account,characters, length, try_id, tryed):
    with open(progress_file, 'w', encoding="cp1251") as f:
        json.dump(
            {"account": account,
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
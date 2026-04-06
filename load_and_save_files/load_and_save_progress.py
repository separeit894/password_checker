import json
import os


# Функция для сохранения прогресса
def save_progress(username, print_try, characters, length, try_id, tryed):
    from core import MY_ENCODING
    from core import PROGRESS_FILE

    with open(PROGRESS_FILE, "w", encoding=MY_ENCODING) as f:
        json.dump(
            {
                "username": username,
                "print_try": print_try,
                "characters": characters,
                "length": length,
                "try_id": try_id,
                "tryed": tryed,
            },
            f,
            indent=4,
        )


# Функция для загрузки прогресса
def load_progress():
    try:
        from core import MY_ENCODING
        from core import PROGRESS_FILE

        # Если файл с прогрессом существует, то он возвращает данные из этого файла
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "r", encoding=MY_ENCODING) as f:
                return json.load(f)
        else:
            if not os.path.isfile(PROGRESS_FILE):
                # Если файл не существует, создаем его с пустым объектом
                with open(PROGRESS_FILE, "w", encoding=MY_ENCODING) as f:
                    json.dump({}, f, indent=4)  # Записываем пустой объект в файл
                print(f"Файл '{PROGRESS_FILE}' был создан.")

    except FileNotFoundError:
        print(f"Файл {PROGRESS_FILE} не найден.")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return None
    return None


if __name__ == "__main__":
    save_progress()
    load_progress()

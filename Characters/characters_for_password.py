import string


digits_progress = 0
ascii_progress = 0
russian_letter_progress = 0
punc_progress = 0

# Кирилица
russian_letters = "абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


# Функция, в которой пользователь будет выбирать, те символы которые будут использоваться в подборе
def characters_password(characters):
    level = 0
    req_types = [
        "Вы хотите использовать числа для подбора: ( Y/n ) ",
        "Вы хотите использовать латинские буквы для подбора: ( Y/n ) ",
        "Вы хотите использовать кириллицу для подбора: ( Y/n ) ",
        "Вы хотите использовать специальные символы для подбора: ( Y/n ) ",
    ]

    while True:
        if level == 4:
            break
        level += 1
        digits = str(input(f"{req_types[level - 1]}: "))
        if digits.lower() in ["y", "д"]:
            if level == 1:
                # Добавляет цифры в список
                characters += string.digits

            if level == 2:
                # Добавляет в список Латиницу в список
                characters += string.ascii_letters

            if level == 3:
                # Добавляет кирилицу в список
                characters += russian_letters

            if level == 4:
                # Добавляет специальные символы в список
                characters += string.punctuation

        elif digits.lower() in ["n", "н"]:
            # Пропускает
            pass
        else:
            # Если он написал что-то кроме y или n, он потребует ещё раз ввести
            print("Вы неправильно ввели, а нужно ( y / n )!")
            level -= 1

    # В итоге возвращаем список символов, которые выбрал пользователь
    return characters


if __name__ == "__main__":
    characters_password(characters="")

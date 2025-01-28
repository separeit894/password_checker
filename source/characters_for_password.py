import string
# characters = ''

digits_progress = 0
ascii_progress = 0
russian_letter_progress = 0
punc_progress = 0

russian_letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
def charactes_password(characters):
    level = 0
    req_types = ["Вы хотите использовать числа для подбора: ( Y/n ) ",
                 "Вы хотите использовать латинские буквы для подбора: ( Y/n ) ",
                 "Вы хотите использовать кириллицу для подбора: ( Y/n ) ",
                 "Вы хотите использовать специальные символы для подбора: ( Y/n ) "]

    while True:
        if level == 4:
            break
        level += 1
        digits = str(input(f"{req_types[level - 1]}: "))
        if digits.lower() in ["y", "д"]:
            if level == 1:
                characters += string.digits
                # digits_progress += 1
            if level == 2:
                characters += string.ascii_letters
                # ascii_progress += 1
            if level == 3:
                characters += russian_letters
                # russian_letter_progress += 1
            if level == 4:
                characters += string.punctuation
                # punc_progress += 1
        elif digits.lower() in ["n", "н"]:
            pass
        else:
            print("Вы неправильно ввели, а нужно ( y / n )!")
            level -= 1

    return characters

if __name__ == "__main__":
    charactes_password(characters="")
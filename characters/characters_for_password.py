import string

digits_progress = 0
ascii_progress = 0
russian_letter_progress = 0
punc_progress = 0

# Cyrrilyc
lowercase_russian_letters = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
uppercase_russian_letters = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
russian_letters = lowercase_russian_letters + uppercase_russian_letters


# Characters
def characters_password(characters):
    level = 0
    req_types = [
        "[..] Do you want to use digits for selection: ( Y/n ) ",
        "[..] Do you want to use Latin letters for selection: ( Y/n ) ",
        "[..] Do you want to use Cyrillic for selection: ( Y/n ) ",
        "[..] Do you want to use special characters for matching: ( Y/n ) ",
    ]

    while True:
        if level == 4:
            break
        level += 1
        digits = str(input(f"{req_types[level - 1]}: "))
        if digits.lower() in ["y", "д"]:
            if level == 1:
                # Append Digits
                characters += string.digits

            if level == 2:
                # Append Ascii letters
                characters += string.ascii_letters

            if level == 3:
                # Append Cyrillic letters
                characters += russian_letters

            if level == 4:
                # Append Special characters
                characters += string.punctuation

        elif digits.lower() in ["n", "н"]:
            # Skip
            pass
        else:
            # Error
            print("[-] You entered it incorrectly, but it is necessary ( y / n )!")
            level -= 1

    # Return string characters
    return characters


if __name__ == "__main__":
    characters_password(characters="")

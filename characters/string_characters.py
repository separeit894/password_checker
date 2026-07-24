from .characters_for_password import (
    string,
    russian_letters,
    lowercase_russian_letters,
    uppercase_russian_letters
)

# print all chracters built in here
def print_characters():
    print(f"{'Digits':<19}: {string.digits}")
    print(f"{'Ascii Letters:':<19}: {string.ascii_letters}")
    print(f"{'Rus. letters':<19}: {russian_letters}")
    print(f"{'Punctuation':19}: {string.punctuation}")
    
    print("[+] VERBOSE: ")
    print(f"{'Lower Ascii Let.':<19}: {string.ascii_lowercase}")
    print(f"{'Upper Ascii Let.':<19}: {string.ascii_uppercase}")
    print(f"{'Lower Rus. Let.':<19}: {lowercase_russian_letters}")
    print(f"{'Upper Rus. Let.':<19}: {uppercase_russian_letters}")
    
if __name__ == "__main__":
    pass
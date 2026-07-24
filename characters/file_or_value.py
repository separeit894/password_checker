import os
import argparse

def test_value_or_file(value):
    if os.path.isfile(value):
        from core import get_encoding
        with open(value, "r", encoding=get_encoding()) as file:
            src = file.read()
            print(f'src : {src}')
        
        return src
        # return open(value, 'r')
    elif isinstance(value, str):
        return value
    
    raise argparse.ArgumentTypeError(f"'{value}' не является файлом или 'stdin'")

if __name__ == "__main__":
    pass
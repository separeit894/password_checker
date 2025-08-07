def get_encoding_name(code_page):    
    WINDOWS_CODE_PAGES = {
        437: 'cp437',    # US DOS
        708: 'iso8859-6', # Arabic (ASMO 708)
        709: '',         # Arabic (ASMO 449+, BCON V4)
        710: 'cp864',    # Arabic (Transparent Arabic)
        720: 'cp864',    # Arabic (ISO)
        850: 'cp850',    # Multilingual Latin-1
        852: 'cp852',    # Slavic (Latin-2)
        855: 'cp855',    # Cyrillic (Russian)
        857: 'cp857',    # Turkish
        858: 'cp858',    # Multilingual Latin-1 + Euro
        860: 'cp860',    # Portuguese
        861: 'cp861',    # Icelandic
        862: 'cp862',    # Hebrew
        863: 'cp863',    # Canadian French
        864: 'cp864',    # Arabic
        865: 'cp865',    # Nordic DOS
        866: 'cp866',    # Russian DOS
        869: 'cp869',    # Greek (DOS)
        874: 'cp874',    # Thai (Windows)
        932: 'shift_jis',# Japanese
        936: 'gbk',      # Chinese (Simplified)
        949: 'cp949',    # Korean
        950: 'big5',     # Chinese (Traditional)
        1200: 'utf-16-le',# UTF-16 Little Endian
        1201: 'utf-16-be',# UTF-16 Big Endian
        1250: 'cp1250',   # Central European
        1251: 'cp1251',   # Cyrillic
        1252: 'cp1252',   # Western European
        1253: 'cp1253',   # Greek
        1254: 'cp1254',   # Turkish
        1255: 'cp1255',   # Hebrew
        1256: 'cp1256',   # Arabic
        1257: 'cp1257',   # Baltic
        1258: 'cp1258',   # Vietnamese
        65001: 'utf-8',   # UTF-8 (важно!)
    }


    """Возвращает имя кодировки по номеру Windows Code Page"""
    return WINDOWS_CODE_PAGES.get(code_page)

# Примеры:

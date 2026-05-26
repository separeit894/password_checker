# Password Checker

![Recommended Python Versions](assets/recommended_python_version.svg) ![License](assets/license.svg) ![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/separeit894/password_checker/total?label=GitHub%20Downloads&color=%230099ff) ![SourceForge Downloads](https://img.shields.io/sourceforge/dt/password-checker?label=SourceForge%20Downloads&color=%23ff8400)
<hr>

Проект, сделанный на Python, предназначен для проверки аутентификации пароля к учетной записи Windows.
<hr>

## Cодержание

- [Password Checker](#password-checker)
- [Cодержание](#cодержание)
- [Установка скрипта](#установка-скрипта)
  - [Установить зависимости](#установить-зависимости)
  - [Запустить скрипт](#запустить-скрипт)
- [Тестирование скрипта](#тестирование-скрипта)
- [Используемые библиотеки](#используемые-библиотеки)
- [АРГУМЕНТЫ](#аргументы)
- [Ответственность пользователя](#ответственность-пользователя)

## Установка скрипта

Клонируйте репозиторий

```bash
git clone https://github.com/separeit894/password_checker
```

### Установить зависимости 

```bash
pip install -r requirements.txt
```

### Запустить скрипт

**В командной строке Windows ввести:**

```bash
python main.py
```

## Тестирование скрипта

Перед тестированием **отключите ограничение на количество попыток входа в учетную запись!** В противном случае ваша учетная запись Windows может быть заблокирована.

![here how to disable the lookthreshold ](assets/how_to_disable_the_lock_threshold.gif)


## Используемые библиотеки

* Pillow
* pygame
* pywin32


## Аргументы

[Документация по применению аргументов к программе](docs/ARGUMENTS.md)


## Ответственность пользователя

**Используя этот проект, вы соглашаетесь с тем, что несете полную ответственность за его использование. Разработчик не несёт ответственности за любые убытки, повреждения или другие последствия, возникающие в результате использования данного программного обеспечения. Пожалуйста, используйте его на свой страх и риск.**


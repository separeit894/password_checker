### Password_Checker

Проект, сделанный на Python 3.12.0, предназначен для подбора пароля к учетной записи Windows.

## Установка

```bash
git clone https://github.com/separeit894/password_checker
```
### git clone https://github.com/separeit894/password_checker

Затем нужно установить зависимости ( Если не предпочитаете exe файл или он у вас не запускается )

```bash
pip install -r requirements.txt
```

## Запуск программы

В командной строке Windows ввести: python main.py
Важно ещё учитывать разрядность операционной системы ( x32 или x64 ). Если у вас 32 битная Windows, то запускаете файл "main_32", если нет, то запускаете "main_64"

## Тестирование 

Перед тестированием отключите ограничение на количество попыток входа в учетную запись! В противном случае ваша учетная запись Windows может быть заблокирована.

## Используемые библиотеки
* pywin32
* itertools
* string
* ctypes
* time

## Ответственность пользователя

Используя этот проект, вы соглашаетесь с тем, что несете полную ответственность за его использование. Разработчики не несут ответственности за любые убытки, повреждения или другие последствия, возникающие в результате использования данного программного обеспечения. Пожалуйста, используйте его на свой страх и риск.


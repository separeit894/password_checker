@echo off
REM Создание виртуального окружения
python -m venv venv

REM Активация виртуального окружения
call venv\Scripts\activate

REM Обновление pip
python -m pip install --upgrade pip

REM Установка зависимостей из requirements.txt
pip install -r req_3.8.txt

REM Деактивация виртуального окружения (по желанию)
deactivate

echo Установка завершена!
pause

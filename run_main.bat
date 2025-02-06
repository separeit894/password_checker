@echo off

REM Активация виртуального окружения
call venv\Scripts\activate

REM Запуск main.py
python main.py

REM Деактивация виртуального окружения (по желанию)
deactivate

echo Установка и запуск завершены!
pause
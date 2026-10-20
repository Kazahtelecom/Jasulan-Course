@echo off
chcp 65001 >nul
title Web-OOP Mini-LMS

echo ==============================================
echo    Запуск образовательной платформы Web-OOP
echo ==============================================
echo.

:: Переход в директорию проекта
cd /d "%~dp0"

:: Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не найден!
    echo Убедитесь, что Python 3.12+ установлен и добавлен в системную переменную PATH.
    pause
    exit /b 1
)

:: Открытие браузера через 2 секунды после старта сервера
start "" powershell -WindowStyle Hidden -NoProfile -Command "Start-Sleep -Seconds 2; Start-Process http://127.0.0.1:8000"

echo Сайт доступен по адресу: http://127.0.0.1:8000
echo Для остановки сервера нажмите Ctrl + C в этом окне.
echo.

:: Запуск веб-сервера Uvicorn
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause

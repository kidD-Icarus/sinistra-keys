@echo off
REM Sinistra Keys - Windows Build Script v3
REM kidD Icarus / kidDicarus Inc.

echo ========================================
echo   SINISTRA KEYS - Build Script v3
echo   kidD Icarus / kidDicarus Inc.
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.8+ first.
    pause
    exit /b 1
)

echo [1/5] Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo [2/5] Installing dependencies...
pip install python-rtmidi PyQt6 pyinstaller pillow

echo.
echo [3/5] Creating icon...
python create_icon.py
if not exist icon.ico (
    echo WARNING: Icon creation failed, building without icon
)

echo.
echo [4/5] Building standalone .exe using spec file...
echo       (This takes 1-2 minutes, please wait)
echo.
pyinstaller --noconfirm --clean SinistraKeys.spec

echo.
echo [5/5] Done!
echo.
if exist dist\SinistraKeys.exe (
    echo ========================================
    echo   SUCCESS!
    echo   Your app is at: dist\SinistraKeys.exe
    echo ========================================
    echo.
    echo You can copy SinistraKeys.exe anywhere and run it.
    echo No console window should appear.
) else (
    echo ERROR: Build failed. Check the output above.
)
echo.
pause

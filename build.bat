@echo off
REM Sinistra Keys - Windows Build Script
REM Run this in the sinistra-keys folder

echo ========================================
echo   Sinistra Keys - Build Script
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

echo [1/4] Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller pillow cairosvg

echo.
echo [2/4] Converting icon SVG to ICO...
python convert_icon.py

echo.
echo [3/4] Building standalone .exe...
pyinstaller sinistra_keys.spec --clean

echo.
echo [4/4] Done!
echo.
echo Your app is at: dist\SinistraKeys.exe
echo.
pause

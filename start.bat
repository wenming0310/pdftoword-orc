@echo off
echo ========================================
echo   PDF to Word Converter - Startup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.7+
    pause
    exit /b 1
)

echo [SUCCESS] Python installed
python --version
echo.

REM Check if we're in the right directory
if not exist "pdf_to_word_gui.py" (
    echo [ERROR] pdf_to_word_gui.py not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

echo [SUCCESS] Program files found
echo.
echo Starting program...
echo.

REM Run the program
python pdf_to_word_gui.py

if errorlevel 1 (
    echo.
    echo [ERROR] Program exited with error
    pause
)

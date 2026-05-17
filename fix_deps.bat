@echo off
echo ========================================
echo   PDF to Word Converter - Fix Dependencies
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

echo [INFO] Checking and fixing dependencies...
echo.

REM Upgrade pip
echo [1/4] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Reinstall PyQt5
echo [2/4] Reinstalling PyQt5 and PyQt5-tools...
python -m pip uninstall PyQt5 PyQt5-tools -y
python -m pip install PyQt5 PyQt5-tools
echo.

REM Install other dependencies
echo [3/4] Installing other dependencies...
python -m pip install -r requirements.txt
echo.

REM Verify installation
echo [4/4] Verifying installation...
python -c "import PyQt5; print('[SUCCESS] PyQt5 version:', PyQt5.QtCore.PYQT_VERSION_STR)" 2>nul
if errorlevel 1 (
    echo [WARNING] PyQt5 installation may have issues
) else (
    echo [SUCCESS] PyQt5 installed correctly
)
echo.

echo ========================================
echo   Dependencies fixed!
echo ========================================
echo.
echo Now you can:
echo 1. Double-click start.bat to run the program
echo 2. Or run: python pdf_to_word_gui.py
echo.
echo If you still have issues, run diagnose.bat
echo.
pause

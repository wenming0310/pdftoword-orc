@echo off
chcp 65001 >nul
title Install PyQt6 and Dependencies

echo ======================================
echo   Install PyQt6 and Dependencies
echo ======================================
echo.

echo [1/3] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [FAIL] pip upgrade failed
    pause
    exit /b 1
)
echo.

echo [2/3] Uninstalling PyQt5 (if installed)...
python -m pip uninstall PyQt5 -y
echo.

echo [3/3] Installing PyQt6 and dependencies...
python -m pip install -r requirements_pyqt6.txt
if errorlevel 1 (
    echo [FAIL] Installation failed
    pause
    exit /b 1
)
echo.

echo ======================================
echo   Installation Complete!
echo ======================================
echo.
echo Now run:
echo   python pdf_to_word_gui_pyqt6.py
echo.
pause

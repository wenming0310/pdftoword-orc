@echo off
echo ========================================
echo   PDF to Word Converter - Diagnostic
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
if not exist "diagnose_and_fix.py" (
    echo [ERROR] diagnose_and_fix.py not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

echo [SUCCESS] Diagnostic script found
echo.
echo Running diagnostics...
echo.

REM Run diagnostics
python diagnose_and_fix.py

echo.
pause

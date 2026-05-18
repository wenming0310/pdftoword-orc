@echo off
chcp 65001 >nul
title Check PyQt5 Platform Plugin

echo ======================================
echo   Check PyQt5 Platform Plugin
echo ======================================
echo.

echo Checking Python environment...
python -c "import sys; print(f'Python version: {sys.version}')"
if errorlevel 1 (
    echo [FAIL] Python not found or not configured
    pause
    exit /b 1
)

echo.
echo Checking PyQt5 installation...
python -c "import PyQt5; print(f'PyQt5 version: {PyQt5.QtCore.PYQT_VERSION_STR}')"
if errorlevel 1 (
    echo [FAIL] PyQt5 not installed
    echo Run: python -m pip install PyQt5
    pause
    exit /b 1
)

echo.
echo Checking site-packages path...
python -c "import site; print('site-packages:', site.getsitepackages())"

echo.
echo Checking platform plugin directory...
python -c "
import os
import site

paths = [
    os.path.join(site.getsitepackages()[0], 'PyQt5', 'Qt6', 'plugins', 'platforms'),
    os.path.join(site.getsitepackages()[-1], 'PyQt5', 'Qt6', 'plugins', 'platforms'),
    os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'Qt6', 'plugins', 'platforms')
]

found = False
for path in paths:
    if os.path.exists(path):
        print(f'[OK] Found platform plugin dir: {path}')
        files = os.listdir(path)
        if 'qwindows.dll' in files:
            print(f'[OK] Found qwindows.dll')
            found = True
        else:
            print(f'[WARN] qwindows.dll not found in: {path}')
            print(f'  Files in dir: {files}')
    else:
        print(f'[SKIP] Dir not exists: {path}')

if not found:
    print('[FAIL] qwindows.dll not found')
    print('PyQt5 installation may be incomplete')
    exit(1)
"

if errorlevel 1 (
    echo.
    echo [ISSUE] PyQt5 platform plugin missing
    echo Trying to reinstall PyQt5...
    python -m pip uninstall PyQt5 -y
    python -m pip install PyQt5
    if errorlevel 1 (
        echo [FAIL] PyQt5 reinstall failed
        pause
        exit /b 1
    )
)

echo.
echo ======================================
echo   Test Qt Application Startup
echo ======================================
echo.

python -c "
import sys
import os
import site

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(site.getsitepackages()[0], 'PyQt5', 'Qt6', 'plugins', 'platforms')
if not os.path.exists(os.environ['QT_QPA_PLATFORM_PLUGIN_PATH']):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(site.getsitepackages()[-1], 'PyQt5', 'Qt6', 'plugins', 'platforms')
if not os.path.exists(os.environ['QT_QPA_PLATFORM_PLUGIN_PATH']):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'Qt6', 'plugins', 'platforms')

print(f'Plugin path: {os.environ.get(\"QT_QPA_PLATFORM_PLUGIN_PATH\")}')

from PyQt5.QtWidgets import QApplication
app = QApplication([])
print('[OK] Qt application created successfully')
"

if errorlevel 1 (
    echo.
    echo [FAIL] Qt application startup failed
    echo.
    echo Possible issues:
    echo 1. PyQt5 installation incomplete
    echo 2. Windows Visual C++ Redistributable not installed
    echo 3. Antivirus blocking DLL loading
    echo.
    echo Suggestions:
    echo 1. Reinstall PyQt5: python -m pip uninstall PyQt5 -y ^^&^^& python -m pip install PyQt5
    echo 2. Download Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe
    pause
    exit /b 1
)

echo.
echo ======================================
echo   Diagnosis Complete
echo ======================================
echo [OK] PyQt5 platform plugin check passed
echo Now run: python pdf_to_word_gui.py
echo.
pause

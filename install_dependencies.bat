@echo off
echo ==============================================================
echo        Install Python Dependencies
echo ==============================================================
echo.
echo This will install all required libraries for PDF to Word Converter
echo.

echo [Step 1/2] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [Step 2/2] Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo.

echo ==============================================================
echo        Installation Complete
echo ==============================================================
echo.
echo Now let's verify the installation...
echo.
pause

echo Running verification tests...
echo.

python -c "import PyQt5; print('[OK] PyQt5')"
python -c "import fitz; print('[OK] fitz')"
python -c "import pdf2docx; print('[OK] pdf2docx')"
python -c "import pytesseract; print('[OK] pytesseract')"
python -c "import PIL; print('[OK] PIL')"
python -c "import docx; print('[OK] docx')"
python -c "import cv2; print('[OK] opencv')"
python -c "import numpy; print('[OK] numpy')"

echo.
echo If all show [OK], you can now run the program
echo Run: start_program.bat
echo.
pause


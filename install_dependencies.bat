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

echo [Step 2/2] Installing dependencies...
echo This may take several minutes, please wait...
echo.

python -m pip install PyQt5
python -m pip install pymupdf
python -m pip install pdf2docx
python -m pip install pytesseract
python -m pip install Pillow
python -m pip install python-docx
python -m pip install opencv-python
python -m pip install numpy
python -m pip install requests
python -m pip install gitpython

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
python -m pip show numpy >nul 2>&1 && echo [OK] numpy || echo [FAIL] numpy

echo.
echo ==============================================================
echo        All Done!
echo ==============================================================
echo.
echo If all show [OK], you can now run the program
echo Run: start_program.bat
echo.
pause


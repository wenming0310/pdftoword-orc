@echo off
echo ==============================================================
echo                  Test Python Dependencies
echo ==============================================================
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
echo If all show [OK], dependencies are installed correctly
pause


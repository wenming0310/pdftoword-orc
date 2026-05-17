@echo off
echo ==============================================================
echo                  测试Python依赖库
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
echo 如果全部显示 [OK]，说明依赖安装正常
pause


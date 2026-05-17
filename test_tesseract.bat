@echo off
echo ==============================================================
echo                  Test Tesseract OCR
echo ==============================================================
echo.
python -c "import pytesseract; print('Tesseract config:', pytesseract.pytesseract.tesseract_cmd)"
echo.
if exist "D:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo [OK] Tesseract executable found
) else (
    echo [FAIL] Tesseract not found!
)
echo.
python -c "from PIL import Image; import pytesseract; img = Image.new('RGB', (100, 50)); t = pytesseract.image_to_string(img); print('[OK] OCR test passed')"
echo.
pause


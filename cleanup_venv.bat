@echo off
title Cleanup venv Directory

echo ======================================
echo   Cleanup venv Directory
echo ======================================
echo.

if exist "venv" (
    echo [INFO] Found venv directory
    echo [INFO] Deleting venv directory...
    
    REM Try to delete venv folder
    rmdir /s /q "venv" 2>nul
    
    if exist "venv" (
        echo [FAIL] Could not delete venv directory
        echo Please close any programs using venv and try again
    ) else (
        echo [SUCCESS] venv directory deleted
    )
) else (
    echo [INFO] venv directory not found
)

echo.
pause

@echo off
echo ========================================
echo MEESHO SCRAPER - EXECUTABLE BUILDER
echo ========================================
echo.
echo Installing PyInstaller if not installed...
pip install pyinstaller
echo.
echo Building executable...
echo.

pyinstaller --name meesho --onedir --console --noconfirm --clean meesho.py

echo.
echo ========================================
if exist "dist\meesho\meesho.exe" (
    echo BUILD SUCCESSFUL!
    echo.
    echo Executable location: dist\meesho\meesho.exe
    echo.
    echo Double-click dist\meesho\meesho.exe to run
) else (
    echo BUILD FAILED!
)
echo ========================================
pause


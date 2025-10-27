"""
Build script to create meesho.py as executable
This will create meesho.exe that opens in CMD terminal
"""
import PyInstaller.__main__
import sys

# PyInstaller configuration
args = [
    'meesho.py',                    # Source file
    '--name=meesho',                 # Output name
    '--onedir',                      # Create a folder instead of single file
    '--console',                     # Keep console window visible
    '--noconfirm',                   # Overwrite without asking
    '--clean',                       # Clean cache before building
    '--collect-all',                 # Collect all submodules
    'undetected_chromedriver',       # Include all UC modules
    'selenium',                      # Include all Selenium modules
]

try:
    PyInstaller.__main__.run(args)
    print("\n✅ Build completed successfully!")
    print(f"📁 Executable location: dist/meesho/meesho.exe")
except Exception as e:
    print(f"\n❌ Build failed: {e}")
    print("\nMake sure you have PyInstaller installed:")
    print("pip install pyinstaller")
    input("\nPress Enter to exit...")


@echo off

pip --version
pyinstaller --onefile --add-data "..\res;res" ..\main.py
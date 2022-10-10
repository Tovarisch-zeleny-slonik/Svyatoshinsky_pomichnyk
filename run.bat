@echo off
call  %~dp0\venv\Scripts\activate.bat
cd %CD%
python svyatoshabot.py
pause
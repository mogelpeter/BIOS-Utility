@echo off
setlocal

:: Path to Python.exe
set PYTHON_EXE=python

:: Determine the directory in which the batch file is located
set SCRIPT_DIR=%~dp0

:: Path to the Python script in the same directory as the batch file
set SCRIPT_PATH=%SCRIPT_DIR%bios.py

:: Check whether the script is executed as administrator
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator Rights
    powershell -Command "Start-Process '%PYTHON_EXE%' -ArgumentList '%SCRIPT_PATH%' -Verb RunAs"
    exit /b
)

:: Execute the script
"%PYTHON_EXE%" "%SCRIPT_PATH%"
if %errorlevel% neq 0 (
    echo The script has crashed or there was an error. Press any button to close the window...
    pause >nul
)

endlocal
pause

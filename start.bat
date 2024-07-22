@echo off
setlocal

:: Pfad zu Python-Exe
set PYTHON_EXE=python

:: Ermitteln des Verzeichnisses, in dem die Batch-Datei liegt
set SCRIPT_DIR=%~dp0

:: Pfad zum Python-Skript im selben Verzeichnis wie die Batch-Datei
set SCRIPT_PATH=%SCRIPT_DIR%bios.py

:: Überprüfen, ob das Skript als Administrator ausgeführt wird
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo Erneutes Ausführen des Skripts als Administrator...
    powershell -Command "Start-Process '%PYTHON_EXE%' -ArgumentList '%SCRIPT_PATH%' -Verb RunAs"
    exit /b
)

:: Ausführen des Skripts
"%PYTHON_EXE%" "%SCRIPT_PATH%"
if %errorlevel% neq 0 (
    echo Das Skript ist abgestürzt oder es gab einen Fehler. Drücken Sie eine beliebige Taste, um das Fenster zu schließen...
    pause >nul
)

endlocal
pause

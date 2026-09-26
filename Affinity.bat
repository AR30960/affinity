@echo off
setlocal enabledelayedexpansion
title Affinity - Demarrage de l'application
cd /d "%~dp0"

echo ======================================================
echo           DEMARRAGE DE L'APPLICATION AFFINITY
echo ======================================================
echo.

:: 1. Detection de l'interpreteur Python approprie (priorite au venv et pythonw sans console)
set "PYTHON_EXE="
if exist "%~dp0.venv\Scripts\pythonw.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\pythonw.exe"
) else if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
) else (
    where pythonw >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON_EXE=pythonw"
    ) else (
        set "PYTHON_EXE=python"
    )
)

:: 2. Verifier si le serveur ecoute deja sur le port 8765
netstat -ano | findstr /R /C:":8765 .*LISTENING" >nul
if !errorlevel! neq 0 (
    echo [1/2] Lancement du serveur local Affinity en arriere-plan...
    start "" "!PYTHON_EXE!" "%~dp0server.py"
    
    :: Attente active que le serveur soit a l'ecoute (max 10 secondes) sans utiliser timeout qui plante sur redirection
    set /a attempts=0
    :WAIT_LOOP
    ping 127.0.0.1 -n 2 >nul
    netstat -ano | findstr /R /C:":8765 .*LISTENING" >nul
    if !errorlevel! equ 0 (
        echo      Serveur pret et actif sur http://localhost:8765.
    ) else (
        set /a attempts+=1
        if !attempts! lss 10 goto WAIT_LOOP
        echo [ATTENTION] Le serveur met du temps a demarrer. Verification en cours...
    )
) else (
    echo [1/2] Le serveur Affinity est deja actif sur le port 8765.
)

:: 3. Ouverture de la fenetre applicative Bureau Windows
echo [2/2] Ouverture de la fenetre applicative Bureau Windows...

set EDGE_PATH="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not exist %EDGE_PATH% (
    set EDGE_PATH="C:\Program Files\Microsoft\Edge\Application\msedge.exe"
)

if exist %EDGE_PATH% (
    start "" %EDGE_PATH% --app=http://localhost:8765 --window-size=1300,880
) else (
    start http://localhost:8765
)

exit

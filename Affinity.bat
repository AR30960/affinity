@echo off
title Affinity - Demarrage de l'application
cd /d "%~dp0"

echo ======================================================
echo           DEMARRAGE DE L'APPLICATION AFFINITY
echo ======================================================
echo.

:: Verifier si le serveur tourne deja sur le port 8765
netstat -ano | findstr :8765 >nul
if %errorlevel% neq 0 (
    echo [1/2] Lancement du serveur local Affinity...
    start /b python server.py >nul 2>&1
    timeout /t 2 /nobreak >nul
) else (
    echo [1/2] Le serveur Affinity est deja actif sur le port 8765.
)

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

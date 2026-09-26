@echo off
setlocal enabledelayedexpansion
title Affinity - Redemarrage du Serveur
cd /d "%~dp0"

echo ============================================================
echo            REDEMARRAGE DU SERVEUR LOCAL AFFINITY
echo ============================================================
echo.

echo [1/3] Arret du serveur existant sur le port 8765...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /R /C:":8765 .*LISTENING"') do (
    echo       Fermeture du processus PID: %%a...
    taskkill /f /pid %%a >nul 2>&1
)

ping 127.0.0.1 -n 2 >nul

echo [2/3] Relance du serveur en arriere-plan...
cscript //nologo "%~dp0Demarrer_Serveur_ArrierePlan.vbs"

echo [3/3] Verification de l'ecoute...
set /a attempts=0
:CHECK_LOOP
ping 127.0.0.1 -n 2 >nul
netstat -ano | findstr /R /C:":8765 .*LISTENING" >nul
if !errorlevel! equ 0 (
    echo.
    echo ============================================================
    echo    SUCCES : Le serveur Affinity est actif et pret !
    echo    URL : http://localhost:8765
    echo ============================================================
) else (
    set /a attempts+=1
    if !attempts! lss 8 goto CHECK_LOOP
    echo [ATTENTION] Le serveur met du temps a repondre.
)

echo.
timeout /t 3 >nul 2>&1

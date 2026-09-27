@echo off
setlocal enabledelayedexpansion
title Affinity - Sauvegarde de la Base Locale
cd /d "%~dp0"

echo ============================================================
echo      SAUVEGARDE DE SECURITE DE LA BASE LOCALE AFFINITY
echo ============================================================
echo.

if not exist "%~dp0affinity.db" (
    echo [ERREUR] Le fichier affinity.db est introuvable dans ce dossier.
    pause
    exit /b 1
)

if not exist "%~dp0backups" mkdir "%~dp0backups"

:: Generer l'horodatage YYYYMMDD_HHMMSS
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value 2^>nul') do set dt=%%I
if defined dt (
    set "TIMESTAMP=!dt:~0,8!_!dt:~8,6!"
) else (
    set "TIMESTAMP=%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
    set "TIMESTAMP=!TIMESTAMP: =0!"
)

set "BACKUP_FILE=%~dp0backups\affinity_backup_!TIMESTAMP!.db"

copy /y "%~dp0affinity.db" "!BACKUP_FILE!" >nul
if !errorlevel! equ 0 (
    echo [SUCCES] Base de donnees sauvegardee avec succes :
    echo          !BACKUP_FILE!
    echo.
    echo Profils, questions et reponses sont securises.
) else (
    echo [ERREUR] Impossible de copier la base de donnees.
)

echo.
timeout /t 4 >nul 2>&1

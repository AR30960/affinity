@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo   INSTALLATION DU DEMARRAGE AUTOMATIQUE AFFINITY AU BOOT
echo ============================================================
echo.

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "VBS_SCRIPT=%~dp0Demarrer_Serveur_ArrierePlan.vbs"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\Affinity_Server_Autostart.lnk"

:: Verifier l'existence du script VBS
if not exist "%VBS_SCRIPT%" (
    echo [ERREUR] Le fichier %VBS_SCRIPT% est introuvable.
    pause
    exit /b 1
)

:: Creation du raccourci dans le dossier de demarrage via PowerShell
powershell -NoProfile -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = 'wscript.exe'; $s.Arguments = '\"%VBS_SCRIPT%\"'; $s.WorkingDirectory = '%~dp0'; $s.Description = 'Serveur local Affinity en arriere-plan'; $s.Save()"

if exist "%SHORTCUT_PATH%" (
    echo [SUCCES] Le serveur Affinity demarrera desormais automatiquement
    echo          en arriere-plan a chaque ouverture de votre session Windows !
    echo.
    echo Raccourci cree dans :
    echo %SHORTCUT_PATH%
) else (
    echo [ERREUR] Impossible de creer le raccourci de demarrage.
)

echo.
pause

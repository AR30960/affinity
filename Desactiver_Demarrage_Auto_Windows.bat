@echo off
setlocal
echo ============================================================
echo   DESACTIVATION DU DEMARRAGE AUTOMATIQUE AFFINITY
echo ============================================================
echo.

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\Affinity_Server_Autostart.lnk"

if exist "%SHORTCUT_PATH%" (
    del "%SHORTCUT_PATH%"
    echo [SUCCES] Le raccourci de demarrage automatique a ete supprime avec succes.
) else (
    echo [INFO] Aucun demarrage automatique n'etait actif.
)

echo.
pause

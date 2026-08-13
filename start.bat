@echo off
title Xrat Launcher
cd /d "%~dp0"
for /d %%d in (*) do if exist "%%d\Xrat.py" cd "%%d"
if not exist "Xrat.py" (
  echo [ERREUR] Xrat.py introuvable dans ce dossier ou un sous-dossier.
  pause
  exit /b 1
)
python Xrat.py
if errorlevel 1 (
  echo [ERREUR] Python introuvable ou Xrat a plante.
)
pause

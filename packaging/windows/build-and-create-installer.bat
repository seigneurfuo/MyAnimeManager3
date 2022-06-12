@echo off

REM Packaing dans le dossier temporaire
call packaging\windows\build.bat

REM Création de l'installateur
"C:\Program Files (x86)\NSIS\makensis.exe" /V4 packaging\windows\installer.nsi
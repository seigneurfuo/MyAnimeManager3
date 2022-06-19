@echo off
REM 2022.06.05

REM Chemin & config
REM Version TODO: A faire en dynamique
set PRODUCT=MyAnimeManager3
set VERSION=2022.06.05

set ROOTDIR=packaging\windows
set SRCDIR=%ROOTDIR%\src
set BINDIR=%ROOTDIR%\bin
set DISTDIR=%ROOTDIR%\dist

REM Nettoyage avant compilation
rmdir /S /Q %DISTDIR%

REM Clonage
if exist .git\ (
    git clone .git %SRCDIR%
) else (
    echo ".git folder not found"
    exit
)




REM Build
pyinstaller %SRCDIR%/src/MyAnimeManager3.py ^
--name %PRODUCT% ^
--workpath %BINDIR% ^
--distpath %DISTDIR% ^
--noconsole ^
--noupx ^
--onedir

REm --onefile

REM Copie des fichiers utiles

REM Si --onefile
REM xcopy /s /e %ROOTDIR%\%PRODUCT%\src\resources\ %DISTDIR%\resources\
REM xcopy /s /e %ROOTDIR%\%PRODUCT%\src\ui\ %DISTDIR%\ui\

REM Si export dossier
xcopy /s /e %SRCDIR%\src\resources\ %DISTDIR%\%PRODUCT%\resources\
xcopy /s /e %SRCDIR%\src\ui\ %DISTDIR%\%PRODUCT%\ui\

REM Nettoyage après compilation
rmdir /S /Q %SRCDIR%
rmdir /S /Q %BINDIR%

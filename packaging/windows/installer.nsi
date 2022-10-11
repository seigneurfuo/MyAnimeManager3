!define PRODUCT "MyAnimeManager3"
!define SRCPATH "dist\MyAnimeManager3"

# The name of the installer
Name "MyAnimeManager3"

; # The file to write
; !tempfile StdOut
; !echo "${StdOut}"
; !system '"git" info show -s --format=%cd --date=format:"%Y.%m.%d" > "${stdout}"'
; !delfile "${StdOut}"
; !undef StdOut
; Name "MyApp SVN.${SVNREV}"

OutFile "myanimemanager3-${version}-installer-windows.exe"

# Request application privileges for Windows Vista and higher
RequestExecutionLevel admin

# Build Unicode installer
Unicode True

# set desktop as install directory
InstallDir "$PROGRAMFILES\MyAnimeManager3"

; !Include 'MUI.nsh'
; !insertmacro MUI_PAGE_DIRECTORY
; !insertmacro MUI_PAGE_WELCOME
; !insertmacro MUI_PAGE_INSTFILES
; !insertmacro MUI_PAGE_FINISH

Section
    # Affiche le détail de l'installation
    SetDetailsView show

    ; !insertmacro MUI_UNPAGE_CONFIRM
    ; !insertmacro MUI_UNPAGE_INSTFILES
    ; !insertmacro MUI_UNPAGE_FINISH

    # define output path
    SetOutPath $INSTDIR
    
    # Copie des fichiers
    File /r "${SRCPATH}\*"
    
    # Création d'un désinstallateur
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    # Inscription de l'application dans le registre
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MyAnimeManager3" "DisplayName" "MyAnimeManager3"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MyAnimeManager3" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
    
    # Racourcis dans le menu démarrer
    CreateShortcut "$SMPROGRAMS\MyAnimeManager3.lnk" "$INSTDIR\MyAnimeManager3.exe" "$INSTDIR\resources\icon.ico"
SectionEnd


# ----- Uninstaller -----
Section "Uninstall"
    # Affiche le détail de désinstallation
    SetDetailsView show

    #
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MyAnimeManager3"

    # Delete installed file
    Delete "$INSTDIR"
    
    # Delete the uninstaller
    Delete "$INSTDIR\Uninstall.exe"

    # Supression du racoucis dans les programmes
    Delete "$SMPROGRAMS\MyAnimeManager3.lnk"

    # Supression du dossier du programme
    RMDir /r $INSTDIR
SectionEnd
!include "FileFunc.nsh"

!define PRODUCT "MyAnimeManager3"
!define SRCPATH "dist\MyAnimeManager3"
!define UNINSTALLER_REGEDIT_PATH "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT}"

# Le nom de l'installateur
Name "${PRODUCT}"

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
InstallDir "$PROGRAMFILES\${PRODUCT}"

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

    # Définition du répertoire d'installation
    SetOutPath $INSTDIR
    
    # Copie des fichiers
    File /r "${SRCPATH}\*"
    
    # Création d'un désinstallateur
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    # Inscription de l'application dans le registre
    WriteRegStr HKLM "${UNINSTALLER_REGEDIT_PATH}" "DisplayName" "${PRODUCT}"
    WriteRegStr HKLM "${UNINSTALLER_REGEDIT_PATH}" "Publisher" "seigneurfuo" 
    WriteRegStr HKLM "${UNINSTALLER_REGEDIT_PATH}" "DisplayIcon" "$\"$INSTDIR\Uninstall.exe,0$\""
    WriteRegStr HKLM "${UNINSTALLER_REGEDIT_PATH}" "URLInfoAbout" "https://github.com/seigneurfuo/myanimemanager3"

    # ----- Calcul de la taille de l'application -----
    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
    WriteRegDWORD HKLM "${UNINSTALLER_REGEDIT_PATH}" "EstimatedSize" "$0"

    WriteRegStr HKLM "${UNINSTALLER_REGEDIT_PATH}" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
    WriteRegStr HKLM "${UNINSTALLER_REGEDIT_PATH}" "QuietUninstallString" "$\"$INSTDIR\Uninstall.exe$\" /S"
    
    # Racourcis dans le menu démarrer
    CreateShortcut "$SMPROGRAMS\${PRODUCT}.lnk" "$INSTDIR\MyAnimeManager3.exe" "" "$INSTDIR\resources\icon.png"
SectionEnd


# ----- Uninstaller -----
Section "Uninstall"
    # Affiche le détail de désinstallation
    SetDetailsView show

    # Supression de la liste des prograùùes
    DeleteRegKey HKLM "${UNINSTALLER_REGEDIT_PATH}"

    # Delete installed file
    Delete "$INSTDIR"
    
    # Delete the uninstaller
    Delete "$INSTDIR\Uninstall.exe"

    # Supression du racoucis dans les programmes
    Delete "$SMPROGRAMS\${PRODUCT}.lnk"

    # Supression du dossier du programme
    RMDir /r $INSTDIR
SectionEnd
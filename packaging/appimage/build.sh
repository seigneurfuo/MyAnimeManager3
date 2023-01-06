APPDIR="myanimemanager3.AppDir"
REPO_PATH="/home/seigneurfuo/Projets/MyAnimeManager/MyAnimeManager3/"

# Dossier
rm -rf "$APPDIR"
mkdir "$APPDIR"

# Fichiers de base de l'Appimage
cp ./files/AppRun "$APPDIR"
chmod +x "$APPDIR/AppRun"
cp ./files/myanimemanager3.desktop "$APPDIR"
chmod +x "$APPDIR/myanimemanager3.desktop"

# MyAnimeManager3
mkdir -p "$APPDIR/opt"
cp -r "$REPO_PATH/src" "$APPDIR/opt/myanimemanager3"

# Python
chmod +x ./files/python3.10.0-cp310-cp310-manylinux2014_x86_64.AppImage
./files/python3.10.0-cp310-cp310-manylinux2014_x86_64.AppImage --appimage-extract
mv squashfs-root python3.10.0-cp310-cp310-manylinux2014_x86_64

cp -r python3.10.0-cp310-cp310-manylinux2014_x86_64/opt "$APPDIR"
cp -r python3.10.0-cp310-cp310-manylinux2014_x86_64/usr "$APPDIR"

# Pip
pip install --target="$APPDIR/opt/python3.10/lib/python3.10/site-packages" --upgrade -r "$REPO_PATH/requirements.txt" 

sleep 2

# Génération de l'AppImage
ARCH=x86_64 appimagetool "$APPDIR"

# Nettoyage
rm -rfv python3.10.0-cp310-cp310-manylinux2014_x86_64/
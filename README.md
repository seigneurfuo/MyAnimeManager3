# MyAnimeManager 3

La continuation de MyAnimeManager1 et MyAnimeManager2.

![](docs/imgs/2023-08-31-23-07-39.png)

Le projet en version 3 à été commencé en 2018.

## Dépendances
- python3
- python-qt6
- peewee

## Lancement simple sans installation

Après avoir cloné le dépot: on peut lancer la commande suivant pour disposer de thêmes supplémentaires. Elle n'est pas obligatoire:

```sh
git submodule update --init
```

Installer les dépendances suivantes:

- python
- python-qt6
- python-peewee

```sh
python3 src/MyAnimeManager3.py
```

## Compilation & Installation

### Archlinux / Manjaro

```sh
make archlinux-build
make archlinux-install
```

### Windows

Installer: git, nsis, Python3, PyInstaller (```pip install pyinstaller```)
Ensuite: ```pip install -r requirements.txt```

Depuis la racine du projet:
.\packaging\windows\build.bat

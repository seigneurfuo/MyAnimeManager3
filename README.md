# MyAnimeManager 3

La continuation de MyAnimeManager1 et MyAnimeManager2.

![](docs/imgs/2023-08-31-23-07-39.png)

Le projet en version 3 à été commencé en 2018.

## Dépendances
- python3
- python-qt6
- peewee

## Lancement simple sans installation

Clonez le dépot et installez les dépendances suivantes:

- python
- python-qt6
- python-peewee

Lancement: 
```sh
python3 src/MyAnimeManager3.py
```

## Compilation & Installation

### Archlinux / Manjaro

```sh
make archlinux-build
make archlinux-install
```

### Fedora

```sh
make fedora-build
make fedora-install
```

### Windows

- Installer: git, nsis, Python3, PyInstaller (```pip install pyinstaller```)
- Ensuite: ```pip install -r requirements.txt```
- Depuis la racine du projet: ```.\packaging\windows\build.bat```
- Le fichier généré se trouve dans: ```packaging/dist/MyAnimeManager```

#### Version portable

Par défaut, les profiles sont stockés dans le dossier suivant: ```Dossier Utilisateur\.myanimemanager\profiles```

Si vous souhaitez utiliser le programme en version portable (sur une cléf USB par exemple):

- Créer un fichier ```.portable``` dans le dossier ```_internal```

Les données portables se trouvent dans le dossier ```_internal\.myanimemanager3\profiles```


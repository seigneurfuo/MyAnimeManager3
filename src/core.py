import os
from pathlib import Path

app_name = "MyAnimeManager 3"
app_version = "DEV"
app_description = "Un gestionnaire de séries multiplateforme écrit en Python3 et Qt5"
app_name_and_version = "{} - {}".format(app_name, app_version)
release_url = "https://api.github.com/repos/seigneurfuo/MyAnimeManager3/releases/latest"
bugtracker_url = "https://github.com/seigneurfuo/MyAnimeManager3/issues/new"

APPLICATION_DATA_PATH = os.path.join(Path.home(), ".myanimemanager3")
PROFILES_PATH = os.path.join(APPLICATION_DATA_PATH, "profiles")

DEFAULT_CONFIG_DATA = {
    "application_stylesheet": None,
    "fusion_theme": True,
    "backups_limit": 10,
    "updates_check": True,
    "friends_enabled": False,
    "custom_data_enabled": False
}

SEASONS_STATES = [
    {"name": "Indéfinie", "icon": "question.png"},
    {"name": "A voir", "icon": "clock.png"},
    {"name": "En cours", "icon": "film.png"},
    {"name": "Terminée", "icon": "tick.png"},
    {"name": "Abandonné", "icon": "cross.png"},
    {"name": "En pause", "icon": "control-pause.png"},
]

RATING_LEVELS = [
    {"name": "Pas de note", "value": None, "icon": ""},
    {"name": "J'aime pas", "value": -1, "icon": "thumb-down.png"},
    {"name": "J'aime", "value": 1, "icon": "thumb-up.png"},
]

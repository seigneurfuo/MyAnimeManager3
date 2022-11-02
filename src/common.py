#!/bin/env python3
import os
from pathlib import Path

from database import Planning, Seasons
import peewee

from ui.dialogs.view_history import ViewHistoryDialog

app_name = "MyAnimeManager 3"
app_version = "DEV"
app_description = "Un gestionnaire de séries multiplateforme écrit en Python3 et Qt5"
app_name_and_version = "{} - {}".format(app_name, app_version)

APPLICATION_DATA_PATH = os.path.join(Path.home(), ".myanimemanager3")
PROFILES_PATH = os.path.join(APPLICATION_DATA_PATH, "profiles")

SEASONS_STATES = [
    {"name": "Indéfinie", "icon": "question.png"},
    {"name": "A voir", "icon": "clock.png"},
    {"name": "En cours", "icon": "film.png"},
    {"name": "Terminée", "icon": "tick.png"},
    {"name": "Annulée", "icon": "cross.png"},
]

def display_view_history_dialog(season_id):
    # Utilisé pour faire un group concat...
    season = Seasons.get(season_id)

    episodes = (peewee.fn.GROUP_CONCAT(Planning.episode).python_value(
        lambda s: ", ".join([str(i) for i in (s or '').split(',') if i])))

    serie_episodes = Planning().select(Planning.date, Planning.season, episodes.alias('episodes')) \
        .where(Planning.serie == season.serie.id) \
        .group_by(Planning.date).order_by(Planning.date, Planning.episode)

    season_episodes = Planning().select(Planning.date, Planning.season, episodes.alias('episodes')) \
        .where(Planning.season == season.id) \
        .group_by(Planning.date).order_by(Planning.date, Planning.episode)

    dialog = ViewHistoryDialog(season, serie_episodes, season_episodes)
    dialog.exec_()

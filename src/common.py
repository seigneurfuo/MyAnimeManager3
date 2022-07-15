#!/bin/env python3
from database import Planning, Seasons
import peewee

from ui.dialogs.view_history import ViewHistory

app_name = "MyAnimeManager 3"
app_version = "DEV"
app_description = "Un gestionnaire de séries multiplateforme écrit en Python3 et Qt5"
app_name_and_version = "{} - {}".format(app_name, app_name)

SEASONS_STATES = [
    {"name": "Indéfinie", "icon": "question.png"},
    {"name": "A voir", "icon": "clock.png"},
    {"name": "En cours", "icon": "film.png"},
    {"name": "Terminée", "icon": "tick.png"},
    {"name": "Annulée", "icon": "cross.png"},
]

def display_view_history_dialog(season_id):
    # Utilisé pour faire un group concat....
    season = Seasons.get(season_id);
    episodes = (peewee.fn.GROUP_CONCAT(Planning.episode).python_value(
        lambda s: ", ".join([str(i) for i in (s or '').split(',') if i])))
    data = Planning().select(Planning.date, Planning.season, episodes.alias('episodes')) \
        .where(Planning.season == season_id) \
        .group_by(Planning.date).order_by(Planning.date, Planning.episode)

    dialog = ViewHistory(season, data)
    dialog.exec_()

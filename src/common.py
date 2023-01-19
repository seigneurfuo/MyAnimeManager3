#!/bin/env python3
import json
import os

from database import Planning, Seasons
import peewee

from core import DEFAULT_CONFIG_DATA
from ui.dialogs.view_history import ViewHistoryDialog


def display_view_history_dialog(season_id):
    season = Seasons.get(season_id)

    # Utilisé pour faire un group concat...
    episodes = (peewee.fn.GROUP_CONCAT(Planning.episode).python_value(
        lambda s: ", ".join([str(i) for i in (s or '').split(',') if i])))

    serie_episodes = Planning().select(Planning.date, Planning.season, episodes.alias('episodes')) \
        .where(Planning.serie == season.serie.id) \
        .group_by(Planning.date).order_by(Planning.date, Planning.episode)

    season_episodes = Planning().select(Planning.date, Planning.season, episodes.alias('episodes')) \
        .where(Planning.season == season.id) \
        .group_by(Planning.date).order_by(Planning.date, Planning.episode)

    dialog = ViewHistoryDialog(season, serie_episodes, season_episodes)
    dialog.exec()


def load_settings(application_config_folder):
    settings_filepath = os.path.join(application_config_folder, "settings.json")

    if os.path.isfile(settings_filepath):
        with open(settings_filepath, "r") as settings_file:
            print("Chargement de la configuration depuis:", settings_filepath)
            return json.load(settings_file)
    else:
        print("Chargement de la configuration par défaut")
        return DEFAULT_CONFIG_DATA

def save_settings(application_config_folder, data):
    settings_filepath = os.path.join(application_config_folder, "settings.json")

    with open(settings_filepath, "w") as settings_file:
        json.dump(data, settings_file)

def display_friends_dialog():
    pass

#!/usr/bin/python3
import io
import json
import os

from database import Planning, Seasons
import peewee

from core import DEFAULT_CONFIG_DATA, APPLICATION_DATA_PATH
from ui.dialogs.view_history import ViewHistoryDialog


def display_view_history_dialog(parent, season_id):
    season = Seasons.get(season_id)

    # Utilisé pour faire un group concat...
    episodes = (peewee.fn.GROUP_CONCAT(Planning.episode).python_value(
        lambda s: ", ".join([str(i) for i in (s or '').split(',') if i])))

    serie_episodes = Planning().select(Planning.date, Planning.season, episodes.alias('episodes')) \
        .where(Planning.serie == season.serie.id) \
        .group_by(Planning.date, Planning.season).order_by(Planning.date, Planning.episode)

    season_episodes = Planning().select(Planning.date, Planning.season, episodes.alias('episodes')) \
        .where(Planning.season == season.id) \
        .group_by(Planning.date).order_by(Planning.date, Planning.episode)

    dialog = ViewHistoryDialog(parent, season, serie_episodes, season_episodes)
    dialog.exec()


def load_settings():
    settings_filepath = os.path.join(APPLICATION_DATA_PATH, "settings.json")

    if os.path.isfile(settings_filepath):
        with open(settings_filepath, "r") as settings_file:
            print("Chargement de la configuration depuis:", settings_filepath)
            user_config = json.load(settings_file)

        # On vérifie que l'on est le même nombre de cléfs par rapport à la configuration par défaut.
        # Si ce n'est pas le cas, alors on ajoute les cléfs manquantes sur le configuration de l'utilisateur en pernant les valeurs par défaut
        default_config_keys = DEFAULT_CONFIG_DATA.keys()
        user_config_keys = user_config.keys()

        for default_config_key in default_config_keys:
            if default_config_key not in user_config_keys:
                msg = "Ajout de la cléf manquante dans la configuration de l'utilisateur: {}".format(default_config_key)
                print(msg)

                # Application de la nouvelle valeur
                user_config[default_config_key] = DEFAULT_CONFIG_DATA[default_config_key]

        # Sauvegarde des paramètres
        save_settings(user_config)

    else:
        print("Chargement de la configuration par défaut")
        user_config = DEFAULT_CONFIG_DATA

        # Sauvegarde des paramètres
        save_settings(user_config)

    return user_config

def save_settings(data):
    if not os.path.isdir(APPLICATION_DATA_PATH):
        os.makedirs(APPLICATION_DATA_PATH)

    settings_filepath = os.path.join(APPLICATION_DATA_PATH, "settings.json")

    with open(settings_filepath, "w") as settings_file:
        json.dump(data, settings_file)

def file_to_blob(filename):
    if os.path.isfile(filename):
        with open(filename, "rb") as f:
            bytesio = io.BytesIO(f.read())
            return bytesio.getvalue()
    else:
        return False
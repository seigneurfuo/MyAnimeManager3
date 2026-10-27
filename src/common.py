#!/usr/bin/python3
import json
import os

from database import Planning, Seasons
import peewee

from core import DEFAULT_CONFIG_DATA, APPLICATION_DATA_PATH
from ui.dialogs.view_history import ViewHistoryDialog

def display_view_history_dialog(parent, season_id) -> None:
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


def load_settings() -> dict:
    settings_filepath = os.path.join(APPLICATION_DATA_PATH, "settings.json")

    if os.path.isfile(settings_filepath):
        with open(settings_filepath, "r") as settings_file:
            print("Chargement de la configuration depuis:", settings_filepath)
            saved_config = json.load(settings_file)

        # Nouvelles cléfs (valeur par défaut) et anciennes cléfs (supprimées)
        new_keys = DEFAULT_CONFIG_DATA.keys() - saved_config.keys()
        old_keys = saved_config.keys() - DEFAULT_CONFIG_DATA.keys()

        for key in new_keys:
            print(f"Ajout de la cléf manquante dans la configuration de l'utilisateur: {key}")

        for key in old_keys:
            print(f"Suppression de l'ancienne cléf de la configuration de l'utilisateur: {key}")

        # On ne garde que les cléfs connues, en conservant les valeurs de l'utilisateur
        user_config = {key: saved_config.get(key, default_value) for key, default_value in DEFAULT_CONFIG_DATA.items()}

        # Sauvegarde des paramètres uniquement si la configuration a changé
        if new_keys or old_keys:
            save_settings(user_config)

    else:
        print("Chargement de la configuration par défaut")
        user_config = dict(DEFAULT_CONFIG_DATA)

        # Sauvegarde des paramètres
        save_settings(user_config)

    return user_config


def save_settings(data) -> None:
    if not os.path.isdir(APPLICATION_DATA_PATH):
        os.makedirs(APPLICATION_DATA_PATH)

    settings_filepath = os.path.join(APPLICATION_DATA_PATH, "settings.json")

    with open(settings_filepath, "w") as settings_file:
        json.dump(data, settings_file)

def goto_to_serie_data(parent, serie_id, season_id):
    parent.tabWidget.setCurrentIndex(1)
    parent.full_list_tab.set_series_combobox_current_selection(serie_id)
    parent.full_list_tab.set_seasons_table_current_selection(season_id)

#!/usr/bin/python3
import csv
import json
import os
from pathlib import Path
from datetime import datetime, timedelta

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QMessageBox, QCompleter

import core
from database import Seasons, Series

# Pour Nyelson ^._.^
def get_paths() -> tuple[str, str]:
    PORTABLE_PATH = os.path.join(os.path.dirname(__file__))
    is_portable = os.path.isfile(os.path.join(PORTABLE_PATH, ".portable"))
    if is_portable:
        application_data_path = os.path.join(PORTABLE_PATH, ".myanimemanager3")
    else:
        application_data_path = os.path.join(Path.home(), ".myanimemanager3")

    profiles_path = os.path.join(application_data_path, "profiles")

    return application_data_path, profiles_path


def get_duration_list(episodes_count, duration, pause_every, pause_duration, start) -> list[str]:
    ret_list = []
    is_pause = True if pause_every > 0 and pause_duration > 0 else False
    pause_count = 0

    start = datetime.strptime(start, "%H:%M")

    for episode_num in range(episodes_count):
        end = start + timedelta(minutes=duration)
        row = ["Visionnage #{}".format(episode_num + 1), f"{start.hour:02d}:{start.minute:02d}",
               f"{end.hour:02d}:{end.minute:02d}"]

        ret_list.append(row)

        # Décale la plage
        start = end

        # Gestion des pauses - Effectue une pause si episode_num est bien un multiple de pause_every
        if is_pause and (episode_num + 1) % pause_every == 0:
            pause_count += 1
            end = start + timedelta(minutes=pause_duration)
            row = ["Pause #{}".format(pause_count), f"{start.hour:02d}:{start.minute:02d}",
                   f"{end.hour:02d}:{end.minute:02d}"]
            ret_list.append(row)

            # Décale la plage
            start = end

    return ret_list


def export_qtablewidget(qtablewidget, app_data_folder, output_filename) -> str:
    # TODO: case à cocher

    output_directory = os.path.join(app_data_folder, "exports")
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    date = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    output_filepath = os.path.join(output_directory, f"export-{output_filename}-{date}.csv")

    with open(output_filepath, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")

        # Entete
        row_data = []
        for header_index in range(qtablewidget.columnCount()):
            item = qtablewidget.horizontalHeaderItem(header_index)
            row_data.append(item.text())

        csv_writer.writerow(row_data)

        # Données
        for row_index in range(qtablewidget.rowCount()):
            row_data = []
            for col_index in range(qtablewidget.columnCount()):
                item = qtablewidget.item(row_index, col_index)
                text = item.text() if "text" in item.__dir__() else ""
                row_data.append(text)

            csv_writer.writerow(row_data)

    return output_filepath


def get_collection_problems(parent) -> list[str]:
    seasons_passed = []
    messages = []

    # ----- Saisons -----
    seasons = Seasons().select().join(Series).where(Seasons.is_deleted == 0).order_by(
        Seasons.sort_id)

    for season in seasons:
        if season.serie.id not in seasons_passed and season.state != 4:

            # Identifiant à 0
            if season.serie.sort_id == 0 and (season.view_count > 0 or season.watched_episodes > 0):
                seasons_passed.append(season.serie.id)
                msg = parent.tr(
                    f"Série: {season.serie.name}. L'identifiant est toujours \"{season.serie.sort_id}\" alors que des épisodes on déja étés vus.")
                messages.append(msg)

            # Aucune nombre d'épisodes défini
            if season.episodes == 0:
                msg = parent.tr(
                    f"Série: {season.serie.name}. La saison \"{season.name}\" n'a aucun nombre d'épisodes définis.")
                messages.append(msg)

            # Titres de la série vide
            # On supprime tout les espaces. S'il ne reste rien, alors c'est que le tire de la saison est vide.
            if season.name.replace(" ", "") == "":
                msg = parent.tr(f"Série: {season.serie.name}. La saison \"{season.sort_id}\" à un nom vide.")
                messages.append(msg)

    # ----- Séries -----
    series = Series.select(Series.sort_id).where(Series.is_deleted == 0).order_by(Series.sort_id)

    # Vérification des ids manquants pour les séries
    # On vérifie que les ids entre le plus petit et le plus grand existant
    series_sort_ids = [x.sort_id for x in series]
    if len(series_sort_ids) > 1:  # Il faut au moins avoir deux ids
        min_id = series_sort_ids[0]  # Id le plus bas
        max_id = series_sort_ids[-1] + 1  # Id le plus haut
        range_ids_list = range(min_id, max_id)

        missing_ids = sorted(list(set(range_ids_list) - set(series_sort_ids)))
        for missing_id in missing_ids:
            msg = parent.tr(f"Pas de série pour l'id {missing_id}. Est-ce normal ?")
            messages.append(msg)

        # TODO: Séries vides
        # TODO: Séries avec le meme identifiant

    for serie in series:
        # Vérification du chemin
        if serie.path and not os.path.isdir(serie.path):
            msg = parent.tr(f"Le chemin pour la série {serie.name} n'existe pas")
            messages.append(msg)

    return messages


def set_cursor_on_center(qwidget) -> None:
    QCursor().setPos(qwidget.mapToGlobal(qwidget.rect().center()))


def tutorial(parent_widget) -> None:
    msg = """Bienvenue dans ce tutoriel !
Ce tutoriel va brièvement présenter les différents écrans de l'application.
"""

    QMessageBox.information(None, "Tutoriel", msg, QMessageBox.StandardButton.Ok)

    tabs = ((1, "Voici l'écran dans lequel vous aller définir les séries à voir"),
            2, "Ecran des outils")
    for tab in tabs:
        # Message de bienvenue
        parent_widget.tabWidget.setCurrentIndex(tab[0])  # Onglet de la liste des animé
        parent_widget.tabWidget.setToolTip(tab[1])
        set_cursor_on_center(parent_widget.tabWidget)
        # btn = parent_widget.tab2
        # btn.setStyleSheet("border: 0.5em solid red;")


def anime_titles_autocomplete(object) -> None:
    # Chargement des complétions automatiques depuis le fichier json
    json_filepath = os.path.join(core.APPLICATION_DATA_PATH, "anime-offline-database-minified.json")
    if not os.path.isfile(json_filepath):
        return

    with open(json_filepath, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    # Animés
    animes_titles = [anime["title"] for anime in data["data"]]

    # Application des complétions automatique
    completer = QCompleter(animes_titles)
    del animes_titles  # Permet de limiter l'usage de RAM pour l'autocompete
    completer.setFilterMode(Qt.MatchFlag.MatchStartsWith)
    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    object.setCompleter(completer)

def get_season_age(season) -> str:
    year = str(season.year) if season.year and str(season.year) != "None" else ""

    # Calcul de l'age
    if year and len(year) == 4:
        # Différence entre deux dates
        release_year_datetime_object = datetime.strptime(year, "%Y")
        age_diff = datetime.now().year - release_year_datetime_object.year
        age = f"{age_diff} ans"
    else:
        age = ""

    return age
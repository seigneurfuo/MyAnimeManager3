import os
import urllib.request
import json
import webbrowser

from datetime import datetime

from PyQt6.QtWidgets import QMessageBox

from core import app_version, APPLICATION_DATA_PATH, release_url, anime_offline_database_release_url, anime_offline_database_json_url
from utils import load_animes_json_data

def _request_data(url):
    req = urllib.request.urlopen(url, timeout=5)
    if not req:
        return None

    return req.read()
def _download_file(url, filepath) -> bool:
    data = _request_data(url)
    if not data:
        return None

    if os.path.isfile(filepath):
        os.remove(filepath)

    with open(filepath, "wb") as json_file:
        json_file.write(data)
        return True

def _request_json(url):
    data = _request_data(url)
    if not data:
        return None

    json_data = json.loads(data.decode("utf-8"))

    return json_data

def check_for_appliction_update() -> bool:
    print("Recherche de mises à jour ...")
    try:
        json_data = _request_json(release_url)
        if not json_data:
            return False

        req = urllib.request.urlopen(release_url, timeout=5)

        remote_version = json_data["tag_name"]
        release_page_url = json_data["html_url"]
        zipball_url = json_data["zipball_url"]

        if app_version < remote_version:
            choice = QMessageBox.information(None, "Nouvelle version disponible",
                                             f"Une nouvelle version est disponible: {remote_version}.\nSouhaitez-vous télécharger la mise à jour sur la page du projet ?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if choice == QMessageBox.StandardButton.Yes:
                webbrowser.open(release_page_url, 2)

            return choice

        return False

    except:
        return False

def check_for_autocomplete_data_update() -> bool:
    print("Recherche de mises à jour pour les complétions automatiques ...")

    json_data = load_animes_json_data()
    if json_data:
        # Récupération de la version locale
        local_file_update_date = datetime.strptime(json_data["lastUpdate"], "%Y-%m-%d")
        local_version = local_file_update_date.strftime("%Y-%V")

        # Récupération de la version en ligne
        json_data = _request_json(anime_offline_database_release_url)
        req = urllib.request.urlopen(release_url, timeout=5)

        remote_version = json_data["tag_name"]

    # Si on n'a pas le fichier ou bien qu'on à une MAJ
    if not json_data or local_version < remote_version:
        print(f"   Locale: {local_version}, Distante: {remote_version}")
        print("   Mise à jour du fichier trouvée ! Récupération de la nouvelle version ...")

        json_filepath = os.path.join(APPLICATION_DATA_PATH, "anime-offline-database-minified.json")
        _download_file(anime_offline_database_json_url, json_filepath)
        return True

    return False


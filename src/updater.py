from ntpath import isfile
import os
import urllib.request
import json
import webbrowser

from datetime import datetime

from PyQt6.QtWidgets import QMessageBox

from core import app_version, APPLICATION_DATA_PATH, release_url, anime_offline_database_releases_url, anime_offline_database_json_url
from utils import anime_json_data_version

from ui.download_dialog import DownloadDialog

def _request_data(url):
    req = urllib.request.urlopen(url, timeout=5)
    if not req:
        return None

    return req.read()

def _request_json(url):
    data = _request_data(url)
    if not data:
        return None

    json_data = json.loads(data.decode("utf-8"))
    return json_data

def check_for_application_update() -> bool:
    print("Recherche de mises à jour de l'application ...")
    try:
        json_data = _request_json(release_url)
        if not json_data:
            return False

        req = urllib.request.urlopen(release_url, timeout=5)

        remote_version = json_data["tag_name"]
        release_page_url = json_data["html_url"]
        zipball_url = json_data["zipball_url"]

        if app_version < remote_version:
            dialog = QMessageBox.information(None, "Nouvelle version disponible",
                                             f"Une nouvelle version est disponible: {remote_version}.\nSouhaitez-vous télécharger la mise à jour sur la page du projet ?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            choice = dialog is QMessageBox.StandardButton.Yes
            if choice:
                webbrowser.open(release_page_url, 2)

            return choice

        return False

    except:
        return False

def check_for_autocomplete_data_update() -> bool:
    print("Recherche de mises à jour pour les complétions automatiques ...")
    try:
        # Récupération de la version en ligne
        json_data = _request_json(anime_offline_database_releases_url)
        remote_version = json_data["tag_name"]
   
        anime_data_version = anime_json_data_version()
        if anime_data_version:
            # Récupération de la version locale
            local_file_update_date = datetime.strptime(anime_data_version, "%Y-%m-%d")
            local_version = local_file_update_date.strftime("%Y-%V")

        # Si on n'a pas le fichier ou bien qu'on à une MAJ
        if not anime_data_version or local_version < remote_version:
            print("   Mise à jour du fichier trouvée ! Récupération de la nouvelle version ...")

            json_filepath = os.path.join(APPLICATION_DATA_PATH, "anime-offline-database-minified.json")
            json_url = anime_offline_database_json_url.format(version=remote_version)
            
            print("Url:", json_url)

            window = DownloadDialog(json_url, json_filepath)
            window.exec()

            return True

        return False

    except Exception as e:
        print(e)
        return False


def already_checked() -> bool:
    current_day_int = datetime.now().strftime("%Y%m%d")

    last_update_date = None
    last_update_filepath = os.path.join(APPLICATION_DATA_PATH, ".last-update-date")
   
    if os.path.isfile(last_update_filepath):
        with open(last_update_filepath, "r") as last_update_file:
            last_update_date = last_update_file.read().strip()

    # Ecriture de la date du jour
    with open(last_update_filepath, "w") as last_update_file:
        last_update_file.write(current_day_int)

    already_checked = last_update_date and last_update_date >= current_day_int
    print("Besoin de rechercher des mises à jour:", not already_checked)

    return already_checked
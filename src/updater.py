import urllib.request
import json
import webbrowser

from PyQt6.QtWidgets import QMessageBox

from core import app_version, release_url

def check_for_update():
    try:
        req = urllib.request.urlopen(release_url, timeout=5)
        if not req:
            return

        data = req.read()
        encoding = req.info().get_content_charset('utf-8')
        json_data = json.loads(data.decode(encoding))

        remote_version = json_data["tag_name"]
        release_page_url = json_data["html_url"]
        zipball_url = json_data["zipball_url"]

        if app_version < remote_version:
            choice = QMessageBox.information(None, "Nouvelle version disponible",
                "Une nouvelle version est disponible: {}.\nSouhaitez-vous télécharger la mise à jour sur la page du projet ?".format(remote_version),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if choice == QMessageBox.StandardButton.Yes:
                webbrowser.open(release_page_url, 2)

    except:
        pass

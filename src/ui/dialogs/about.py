import os
from platform import python_version

from PyQt6.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

from peewee import __version__ as peewee_version

from core import app_name, app_version, IS_PORTABLE
from utils import anime_json_data_version


class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.parent = parent

        self.logo_clicks = 0
        self.icons_path = os.path.join(os.path.dirname(__file__), "../../resources/icons")
        self.logo_data = [
            icon for icon in os.listdir(self.icons_path)
            if os.path.isfile(os.path.join(self.icons_path, icon))
            and icon.endswith(".png")
        ]

        self.init_ui()
        self.init_events()

    def init_ui(self) -> None:
        loadUi(os.path.join(os.path.dirname(__file__), "about.ui"), self)
        self.setWindowTitle(self.tr("A propos"))

        self.tabWidget.setCurrentIndex(0)

        self.fill_data()

    def init_events(self) -> None:
        self.logo.mousePressEvent = self.when_logo_clicked

    def fill_data(self) -> None:
        anime_offline_database_version = self.tr("Inutilisé")
        
        if self.parent.parent.settings["anime_titles_autocomplete"]:
            anime_offline_database_version = anime_json_data_version() if anime_json_data_version() else self.tr("Impossible de récupérer le numéro de version")

        is_portable = self.tr("Oui") if IS_PORTABLE else self.tr("Non")

        fields = [(self.application_name, app_name),
                  (self.application_version, app_version),
                  (self.python_version, python_version()),
                  (self.qt_version, QT_VERSION_STR),
                  (self.pyqt_version, PYQT_VERSION_STR),
                  (self.peewee_version, peewee_version),
                  (self.anime_offline_database_version, anime_offline_database_version),
                  (self.profile_path, self.parent.parent.profile.path),
                  (self.portable, is_portable),
              ]

        for field, value in fields:
            field.setText(value)

    def when_logo_clicked(self, event) -> None:
        pixmap = os.path.join(os.path.dirname(__file__), self.icons_path, self.logo_data[self.logo_clicks])
        self.logo.setPixmap(QPixmap(pixmap).scaled(128, 128))

        if self.logo_clicks == len(self.logo_data) - 1:
            self.logo_clicks = 0
        else:
            self.logo_clicks += 1

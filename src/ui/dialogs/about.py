import os
from platform import python_version

from PyQt6.QtCore import QT_VERSION_STR, PYQT_VERSION_STR, pyqtSlot, QRunnable, QThreadPool
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
        self.icons_path = os.path.join(os.path.dirname(__file__), "../../resources/frames")
        self.logo_data = ["003.png", "002.png", "001.png", "002.png"]

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
        # Version de l'autocomplétion        
        if self.parent.parent.settings["anime_titles_autocomplete"]:
            self.anime_offline_database_version.setText(self.tr("Chargement..."))

            worker = Worker(self.async_fill_anime_offline_database_version)
            self.threadpool = QThreadPool()
            self.threadpool.start(worker)
        else:
            self.anime_offline_database_version.setText(self.tr("Inutilisé"))

        is_portable = self.tr("Oui") if IS_PORTABLE else self.tr("Non")

        fields = [(self.application_name, app_name),
                  (self.application_version, app_version),
                  (self.python_version, python_version()),
                  (self.qt_version, QT_VERSION_STR),
                  (self.pyqt_version, PYQT_VERSION_STR),
                  (self.peewee_version, peewee_version),
                  (self.profile_path, self.parent.parent.profile.path),
                  (self.portable, is_portable),
              ]

        for field, value in fields:
            field.setText(value)

    def async_fill_anime_offline_database_version(self):
        anime_offline_database_version = anime_json_data_version() if anime_json_data_version() else self.tr("Impossible de récupérer le numéro de version")
        self.anime_offline_database_version.setText(anime_offline_database_version)

    def when_logo_clicked(self, event) -> None:
        pixmap = os.path.join(os.path.dirname(__file__), self.icons_path, self.logo_data[self.logo_clicks])
        self.logo.setPixmap(QPixmap(pixmap).scaled(128, 128))

        if self.logo_clicks == len(self.logo_data) - 1:
            self.logo_clicks = 0
        else:
            self.logo_clicks += 1

class Worker(QRunnable):
    """Worker thread."""

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)

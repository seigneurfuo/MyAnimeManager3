#!/bin/env python3

import sys
import os

from pathlib import Path
from PyQt5.QtWidgets import QApplication

import default_settings

from ui.main_window import MainWindow
from database_manager import load_or_create_database
from common import app_name, app_version, app_description, app_name_and_version


class Application(QApplication):
    def __init__(self, args):
        super().__init__(args)

        self.app_dir = os.path.abspath(os.path.dirname(__file__))

        self.setApplicationName(app_name)
        self.setApplicationDisplayName(app_name_and_version)
        self.setApplicationVersion(app_version)

        self.default_settings = default_settings.DEFAULT_SETTINGS
        self.profile_path = None
        self.database_path = None

        self.load_profile()
        self.load_database()

        self.mainwindow = MainWindow(self)
        self.mainwindow.show()

    def load_profile(self):
        # Creation du profil
        self.profile_path = os.path.join(Path.home(), ".myanimemanager3")

        if not os.path.exists(self.profile_path):
            # Création du dossier ./profile/covers qui créer en meme temps le dossier parent ./profile
            os.makedirs(self.profile_path)

    def load_database(self):
        self.database_path = load_or_create_database(self.profile_path)


if __name__ == "__main__":
    DEBUG = 1
    if DEBUG == 1:
        import cgitb
        cgitb.enable(format='text')

    application = Application(sys.argv)
    application.exec_()

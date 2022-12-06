#!/bin/env python3

import sys
import os

from pathlib import Path
from PyQt5.QtWidgets import QApplication

import default_settings

from ui.dialogs.profiles_manage import ProfilesManageDialog

from ui.main_window import MainWindow
from database_manager import load_or_create_database
from profiles import Profiles
import core
from ui.themes import get_themes_list


class Application(QApplication):
    def __init__(self, args):
        super().__init__(args)

        self.app_dir = os.path.abspath(os.path.dirname(__file__))

        self.setApplicationName(core.app_name)
        self.setApplicationDisplayName(core.app_name_and_version)
        self.setApplicationVersion(core.app_version)

        self.default_settings = default_settings.DEFAULT_SETTINGS
        self.profile = None
        self.database_path = None

        self.profile = self.load_profile()
        self.database_path =  self.load_database()

        display_name = self.tr("{} - Profil: {}").format(core.app_name_and_version, self.profile.name)
        self.setApplicationDisplayName(display_name)

        mainwindow = MainWindow(self)
        mainwindow.move(self.desktop().screen().rect().center() - mainwindow.rect().center())
        mainwindow.show()

    def load_profile(self):
        # Creation des dossiers de l'applications
        if not os.path.isdir(core.APPLICATION_DATA_PATH):
            os.makedirs(core.APPLICATION_DATA_PATH)
            os.makedirs(core.PROFILES_PATH)

        profiles_list = Profiles.get_profiles_list()

        # Si pas de profil ou bien plusieurs, on ouvre l'assistant
        if len(profiles_list) != 1:
            profiles_manage = ProfilesManageDialog(ProfilesManageDialog.roles.choose, None)
            profiles_manage.exec()

            if profiles_manage.selected_profile == None:
                exit(0)
            else:
                profile = profiles_manage.selected_profile

        else:
            # Creation du profil
            profile = profiles_list[0]

        return profile

    def load_database(self):
        return load_or_create_database(self.profile)


if __name__ == "__main__":
    DEBUG = 1
    if DEBUG == 1:
        import cgitb

        cgitb.enable(format='text')

    application = Application(sys.argv)
    application.exec()

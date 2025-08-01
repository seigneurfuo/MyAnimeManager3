#!/usr/bin/python3
import argparse
import sys
import os
import platform
import logging

from PyQt6.QtCore import QLibraryInfo, QTranslator, QLocale
from PyQt6.QtWidgets import QApplication
import core
import updater
from ui.dialogs.profiles_manage import ProfilesManageDialog

from ui.main_window import MainWindow
from database_manager import load_or_create_database
from profiles import Profiles

from common import load_settings


# from ui.themes import set_theme


class Application(QApplication):
    def __init__(self, argv, args):
        super().__init__(argv)

        self.app_dir = os.path.abspath(os.path.dirname(__file__))

        self.setApplicationName(core.app_name)
        self.setApplicationDisplayName(core.app_name_and_version)
        self.setApplicationVersion(core.app_version)

        # Patch pour avoir l'icone de la barre des tâches sous Windows
        # https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
        if platform.system() == "Windows":
            import ctypes
            app_id = f'{core.app_name}.{core.app_version}'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        self.settings = load_settings()

        # Définition du mode sombre (j'ai décidé pour le moment de ne plus supporter les thêmes tiers
        if self.settings["fusion_theme"]:
            self.setStyle("fusion")
        # set_theme(self, self.settings["application_stylesheet"])

        # Recherche de mise à jour quotidiennes
        update_already_checked = updater.already_checked()

        # Recherche de MAJ
        if not update_already_checked and not args.offline and (core.app_version != "DEV" and self.settings["updates_check"]):
            if updater.check_for_application_update():
                self.exit()

        # Recherche de MAj pour l'autocomplete
        if self.settings["anime_titles_autocomplete"] and not update_already_checked and not args.offline :
            updater.check_for_autocomplete_data_update()

        self.profile = self.load_profile(args.profile_name)
        self.database_path = self.load_database()

        display_name = self.tr(f"{core.app_name_and_version} - Profil: {self.profile.name}")
        self.setApplicationDisplayName(display_name)

        self.mainwindow = MainWindow(self)
        self.mainwindow.center()
        self.mainwindow.showMaximized()

    def load_profile(self, profile_name=None) -> Profiles:
        # Creation des dossiers de l'applications
        if not os.path.isdir(core.PROFILES_PATH):
            os.makedirs(core.PROFILES_PATH)

        profiles_list = Profiles.get_profiles_list()
        profiles_names = [profile.name for profile in profiles_list]

        if profile_name and profile_name in profiles_names:
            profile = Profiles(profile_name)

        # Si pas de profil ou bien plusieurs, on ouvre l'assistant
        elif len(profiles_list) != 1:
            profiles_manage = ProfilesManageDialog(None, ProfilesManageDialog.roles.choose, None)
            profiles_manage.exec()

            if profiles_manage.selected_profile == None:
                sys.exit(0)
            else:
                profile = profiles_manage.selected_profile

        else:
            # Creation du profil
            profile = profiles_list[0]

        return profile

    def load_database(self) -> str:
        return load_or_create_database(self.profile)


def main():
    # Logging
    APPLICATION_DATA_PATH, _, _ = core.get_paths()
    log_filepath = os.path.join(APPLICATION_DATA_PATH, "log.txt")
    logging.basicConfig(filename=log_filepath, level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

    # Arguments
    argument_parser = argparse.ArgumentParser()
    
    argument_parser.add_argument("--profile-name", required=False, help="Charger directement un profil via son nom")
    argument_parser.add_argument("--offline", required=False, action="store_true", help="Mode en hors ligne: désactive la recherche de mise à jour de l'application et des complétions automatiques")
    
    args = argument_parser.parse_args()

    application = Application(sys.argv, args)

    # Correction des boutons dans les fenetres de dialogues qui n'étaient pas traduites
    # https://doc.qt.io/qtforpython-6/tutorials/basictutorial/translations.html
    path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    translator = QTranslator(application)
    if translator.load(QLocale.system(), "qtbase", "_", path):
        application.installTranslator(translator)

    sys.exit(application.exec())


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(e)
        logging.error("An error occurred during application execution: %s", e)
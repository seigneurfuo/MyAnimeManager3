import os

from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi

from ui.themes import get_themes_list

import core
from common import save_settings

class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = self.parent.parent.settings

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "settings.ui"), self)

        self.setWindowTitle(self.tr("Options"))

        self.fill_data()

    def init_events(self):
        pass

    def fill_data(self):
        # Liste des thêmes
        themes = get_themes_list()

        for theme in themes:
            self.comboBox.addItem(theme.name, userData=theme.path)

        # Choix du thême sélectionné
        current_theme = self.settings["application_stylesheet"]
        print("Theme:", current_theme)
        index = self.comboBox.findData(current_theme)
        self.comboBox.setCurrentIndex(index)



    def save_settings_to_file(self):
        self.settings["application_stylesheet"] = self.comboBox.currentData()
        self.parent.parent.settings = self.settings
        save_settings(core.PROFILES_PATH, self.settings)

    def accept(self):
        self.save_settings_to_file()
        super().accept()

    def reject(self):
        super().reject()

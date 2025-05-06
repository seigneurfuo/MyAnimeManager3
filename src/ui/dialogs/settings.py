import os

from PyQt6.QtWidgets import QDialog, QStyleFactory
from PyQt6.uic import loadUi

# from ui.themes import get_themes_list

from common import save_settings


class SettingsDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.parent = parent
        self.settings = self.parent.parent.settings

        self.init_ui()
        self.init_events()

    def init_ui(self) -> None:
        loadUi(os.path.join(os.path.dirname(__file__), "settings.ui"), self)

        self.setWindowTitle(self.tr("Options"))

        # Masquage de l'option pour changer de thême si on est pas sous Windows
        if "Fusion" not in QStyleFactory.keys():
            self.label.setEnabled(False)
            self.checkBox_3.setEnabled(False)

        self.fill_data()

    def init_events(self) -> None:
        pass

    def fill_data(self) -> None:
        # Liste des thêmes
        # themes = get_themes_list()

        # for theme in themes:
        #     self.comboBox.addItem(theme.name, userData=theme.path)
        #
        # # Choix du thême sélectionné
        # current_theme = self.settings["application_stylesheet"]
        # print("Theme:", current_theme)
        # index = self.comboBox.findData(current_theme)
        # self.comboBox.setCurrentIndex(index)

        # Thême sombre pour Windows
        self.checkBox_3.setChecked(self.settings["fusion_theme"])

        # Conservation des sauvegardes
        self.spinBox.setValue(self.settings["backups_limit"])
        self.checkBox.setChecked(self.settings["updates_check"])

        # Gestion de visionnages avec amis
        self.checkBox_2.setChecked(self.settings["friends_enabled"])

        # Gestion des champs supplémentaires
        self.checkBox_4.setChecked(self.settings["custom_data_enabled"])

        # Gestion de la complétion automatique
        self.checkBox_5.setChecked(self.settings["anime_titles_autocomplete"])

        # Affichage alternatif dans la liste des épisodes à voir (tri par épisodes dernièrement vus)
        self.checkBox_6.setChecked(self.settings["planning_to_watched_alternative_order"])

    def save_settings_to_file(self) -> None:
        # self.settings["application_stylesheet"] = self.comboBox.currentData()
        self.settings["fusion_theme"] = self.checkBox_3.isChecked()
        self.settings["backups_limit"] = self.spinBox.value()
        self.settings["updates_check"] = self.checkBox.isChecked()
        self.settings["friends_enabled"] = self.checkBox_2.isChecked()
        self.settings["custom_data_enabled"] = self.checkBox_4.isChecked()
        self.settings["anime_titles_autocomplete"] = self.checkBox_5.isChecked()
        self.settings["planning_to_watched_alternative_order"] = self.checkBox_6.isChecked()

        # Passage des paramètres à toute l'application
        self.parent.parent.settings = self.settings

        # Sauvegarde des paramètres
        save_settings(self.settings)

    def accept(self) -> None:
        self.save_settings_to_file()
        super().accept()

    def reject(self) -> None:
        super().reject()

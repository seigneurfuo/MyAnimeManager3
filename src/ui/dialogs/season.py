import datetime
import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class SeasonDialog(QDialog):
    def __init__(self, season, serie, seasons_types):
        super().__init__()

        self.season = season
        self.serie = serie
        self.seasons_types = seasons_types

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "season.ui"), self)

        # Remplissage des types
        for seasons_type in self.seasons_types:
            self.comboBox_2.addItem(seasons_type.name, userData=seasons_type.id)

        # # Année par défaut: année en cours
        # current_year = int(datetime.date.today().strftime("%Y"))
        # self.spinBox_5.setValue(current_year)

        # Si création
        if self.season.id:
            self.setWindowTitle(self.season.name)
            self.fill_data()

    def init_events(self):
        # TODO: Empècher de metre un nombre d'épisodes vus plus haut que le total
        pass

    def fill_data(self):
        self.spinBox.setValue(self.season.sort_id)
        self.lineEdit_2.setText(self.season.name)

        if self.season.year and str(self.season.year) != "None":
            self.spinBox_5.setValue(self.season.year)
        else:
            self.spinBox_5.clear()

        self.combobox_1.setCurrentIndex(self.season.state)
        self.spinBox_4.setValue(self.season.episodes)
        self.spinBox_3.setValue(self.season.watched_episodes)
        self.spinBox_2.setValue(self.season.view_count)
        self.checkBox.setChecked(self.season.favorite)
        self.checkBox_2.setChecked(self.season.airing)
        self.textEdit.setPlainText(self.season.description)

        # Changement de l'index
        index = self.comboBox_2.findData(self.season.type.id)
        self.comboBox_2.setCurrentIndex(index)


    def save_data(self):
        # Si création
        if not self.season.id:
            self.season.serie = self.serie

        self.season.sort_id = self.spinBox.value()
        self.season.name = self.lineEdit_2.text().strip()

        self.season.year = None if self.spinBox_5.value() == 0 else self.spinBox_5.value()

        self.season.state = self.combobox_1.currentIndex()
        self.season.episodes = self.spinBox_4.value()
        self.season.watched_episodes = self.spinBox_3.value()
        self.season.view_count = self.spinBox_2.value()
        self.season.favorite = self.checkBox.isChecked()
        self.season.airing = self.checkBox_2.isChecked()
        self.season.description = self.textEdit.toPlainText()
        self.season.type = self.comboBox_2.currentData()

        self.season.save()

    def accept(self):
        self.save_data()
        super().accept()

    def reject(self):
        super().reject()

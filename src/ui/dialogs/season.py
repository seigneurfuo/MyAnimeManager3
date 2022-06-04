import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class SeasonDialog(QDialog):
    def __init__(self, season, serie, seasons_types):
        super(SeasonDialog, self).__init__()

        self.season = season
        self.serie = serie
        self.seasons_types = seasons_types

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "season.ui"), self)

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
        self.combobox_1.setCurrentIndex(self.season.state)
        self.spinBox_4.setValue(self.season.episodes)
        self.spinBox_3.setValue(self.season.watched_episodes)
        self.spinBox_2.setValue(self.season.view_count)
        self.textEdit.setPlainText(self.season.description)

    def save_data(self):
        # Si création
        if not self.season.id:
            self.season.serie = self.serie

        self.season.sort_id = self.spinBox.value()
        self.season.name = self.lineEdit_2.text()
        self.season.state = self.combobox_1.currentIndex()
        self.season.type = self.seasons_types  # TODO pour le meoment toujours saison
        self.season.episodes = self.spinBox_4.value()
        self.season.watched_episodes = self.spinBox_3.value()
        self.season.view_count = self.spinBox_2.value()
        self.season.description = self.textEdit.toPlainText()

        self.season.save()

    def accept(self):
        self.save_data()
        super(SeasonDialog, self).accept()

    def reject(self):
        super(SeasonDialog, self).reject()

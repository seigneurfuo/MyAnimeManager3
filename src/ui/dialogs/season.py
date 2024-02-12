import json
import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt6.uic import loadUi

import core


class SeasonDialog(QDialog):
    def __init__(self, parent, season, serie, seasons_types):
        super().__init__(parent=parent)

        self.season = season
        self.serie = serie
        self.seasons_types = seasons_types

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "season.ui"), self)

        # On rempli par vide si il n'y à pas d'année définie
        if not self.season.id:
            self.spinBox_5.clear()

        # Remplissage de l'état des saisons
        for index, season_state in enumerate(core.SEASONS_STATES):
            state_icon = os.path.join(os.path.dirname(__file__), "../../resources/icons/", season_state["icon"])
            self.combobox_1.addItem(QIcon(state_icon), season_state["name"], userData=index)

        # Remplissage des types
        for seasons_type in self.seasons_types:
            self.comboBox_2.addItem(seasons_type.name, userData=seasons_type.id)

        # Remplissage de la note
        for rating_level in core.RATING_LEVELS:
            rating_icon = os.path.join(os.path.dirname(__file__), "../../resources/icons/", rating_level["icon"])
            self.comboBox.addItem(QIcon(rating_icon), rating_level["name"], userData=rating_level["value"])

        # Si modification
        if self.season.id:
            # Empèche de metre un nombre d'épisodes vus plus haut que le total d'épisode
            self.spinBox_3.setMaximum(self.season.episodes)

            self.setWindowTitle(self.season.name)
            self.fill_data()

    def init_events(self):
        self.pushButton.clicked.connect(self.add_row)

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

        if self.season.rating is not None:
            index = self.comboBox.findData(self.season.rating)
            self.comboBox.setCurrentIndex(index) # FIXME: Utiliser plutot DATA ?

        self.checkBox_2.setChecked(self.season.airing)
        self.textEdit.setPlainText(self.season.description)

        # Changement de l'index
        index = self.comboBox_2.findData(self.season.type.id)
        self.comboBox_2.setCurrentIndex(index) # FIXME: Utiliser plutot DATA ?

        # Chargement des champs supplémentaires + Affichage dans le tableau
        custom_data = json.loads(self.season.custom_data) if self.season.custom_data else []
        row_count = len(custom_data)
        self.tableWidget.setRowCount(row_count + 1)

        for row_index, key in enumerate(custom_data):

            columns = [key, custom_data[key]]
            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                #item.setData(Qt.ItemDataRole.UserRole, )
                self.tableWidget.setItem(row_index, col_index, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
                                                                 QHeaderView.ResizeMode.ResizeToContents)

    def add_row(self):
        self.tableWidget.insertRow(0)

    def remove_row(self):
        pass

    def save_data(self):
        # Si création
        if not self.season.id:
            self.season.serie = self.serie

        self.season.sort_id = self.spinBox.value()
        self.season.name = self.lineEdit_2.text().strip()

        self.season.year = None if self.spinBox_5.value() == 0 or len(str(self.spinBox_5.value())) != 4 else self.spinBox_5.value()

        self.season.state = self.combobox_1.currentData()
        self.season.episodes = self.spinBox_4.value()
        self.season.watched_episodes = self.spinBox_3.value()
        self.season.view_count = self.spinBox_2.value()
        self.season.rating = self.comboBox.currentData()
        self.season.airing = self.checkBox_2.isChecked()
        self.season.description = self.textEdit.toPlainText()
        self.season.type = self.comboBox_2.currentData()

        self.save_custom_data()

        self.season.save()

    def save_custom_data(self):
        data = {}

        for row_index in range(self.tableWidget.rowCount()):

            key_item = self.tableWidget.item(row_index, 0)
            key = key_item.text() if "text" in key_item.__dir__() else ""

            value_item = self.tableWidget.item(row_index, 1)
            value = value_item.text() if "text" in value_item.__dir__() else ""

            if not key:
                continue

            data[key] = value

        self.season.custom_data = json.dumps(data) if data else None

    def accept(self):
        self.save_data()
        super().accept()

    def reject(self):
        super().reject()

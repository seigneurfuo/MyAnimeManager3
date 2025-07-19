import json
import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QFileDialog
from PyQt6.uic import loadUi

import core
from ui.dialogs.autocomplete import AutocompleteDialog
from utils import save_cover, load_cover


class SeasonDialog(QDialog):
    def __init__(self, parent, season, serie, seasons_types) -> None:
        super().__init__(parent=parent)
        self.parent = parent

        self.season = season
        self.serie = serie
        self.seasons_types = seasons_types
        self.picture_filepath = None

        self.picture_url = None

        self.init_ui()
        self.init_events()

    def init_ui(self) -> None:
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

        if not self.parent.parent.parent.settings["custom_data_enabled"]:
            self.label_11.setVisible(False)
            self.tabWidget.setVisible(False)
            self.pushButton.setVisible(False)
            self.pushButton_2.setVisible(False)

    def init_events(self) -> None:
        self.pushButton_3.clicked.connect(self.open_autocomplete_dialog)
        self.pushButton.clicked.connect(self.add_row)
        self.pushButton_2.clicked.connect(self.remove_row)
        self.choose_picture_button.clicked.connect(self.choose_picture)
        self.pushButton_5.clicked.connect(self.delete_image)

    def fill_data(self) -> None:
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
            self.comboBox.setCurrentIndex(index)  # FIXME: Utiliser plutot DATA ?

        self.checkBox_2.setChecked(self.season.airing)
        self.textEdit.setPlainText(self.season.description)

        # Changement de l'index
        index = self.comboBox_2.findData(self.season.type.id)
        self.comboBox_2.setCurrentIndex(index)  # FIXME: Utiliser plutot DATA ?

        # Champs supplémentaires
        if self.parent.parent.parent.settings["custom_data_enabled"]:
            self.fill_custom_data()

    def open_autocomplete_dialog(self):
        dialog = AutocompleteDialog(self, self.season.name)
        dialog.exec()

        anime_data = dialog.anime_data
        del dialog

        if not anime_data:
            return
   
        # Valeurs par défaut si nouvelle série
        if not self.season.id:
            self.season.name = ""
            self.season.episodes = 0
            self.season.airing = False
            self.season.sort_id = 1
            self.season.watched_episodes = 0
            self.season.view_count = 0
            self.season.state = 0
            self.season.type = 1
            self.season.custom_data = []

        # Données
        if anime_data["save_type"] in (0, 1):
            self.season.name = anime_data["title"]
            self.season.year = anime_data["year"]
            self.season.episodes = anime_data["episodes"]
            self.season.airing = (anime_data["status"] == "ONGOING") 

        # Images
        if anime_data["save_type"] in(0, 2) and anime_data["picture_tmp_filepath"]:
            self.picture_filepath = anime_data["picture_tmp_filepath"]


        self.fill_data()

    def fill_custom_data(self) -> None:
        self.tableWidget.clearContents()

        # Chargement des champs supplémentaires + Affichage dans le tableau
        custom_data = self.season.custom_data
        row_count = len(custom_data)
        self.tableWidget.setRowCount(row_count + 1)

        for row_index, key in enumerate(custom_data):

            columns = [key, custom_data[key]]
            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                # item.setData(Qt.ItemDataRole.UserRole, )
                self.tableWidget.setItem(row_index, col_index, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
                                                                    QHeaderView.ResizeMode.ResizeToContents)

        # Onglet RAW
        pretty_json = json.dumps(self.season.custom_data, indent=4)
        self.plainTextEdit.setPlainText(pretty_json)

    def add_row(self) -> None:
        self.tableWidget.insertRow(0)

    def remove_row(self) -> None:
        current_row = self.tableWidget.currentRow()
        self.tableWidget.removeRow(current_row)

    def choose_picture(self) -> None:
        path = self.season.serie.path if self.season.serie.path and os.path.isdir(self.season.serie.path) else ""
        self.picture_filepath, filter = QFileDialog.getOpenFileName(self, self.tr("Choisir une image"), path,
                                                                    "Fichiers images (*.jpg *.jpeg *.png *.gif);;Tous les fichiers (*)")

    def delete_image(self) -> None:
        if self.picture_filepath:
            self.picture_filepath = ""

        filepath = load_cover(self.parent.parent.parent.profile.path, "season", self.season.id)
        if filepath:
            os.remove(filepath)

    def save_data(self) -> None:
        # Si création
        if not self.season.id:
            self.season.serie = self.serie

        self.season.sort_id = self.spinBox.value()
        self.season.name = self.lineEdit_2.text().strip()

        self.season.year = None if self.spinBox_5.value() == 0 or len(
            str(self.spinBox_5.value())) != 4 else self.spinBox_5.value()

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

    def save_custom_data(self) -> None:
        data = {}

        for row_index in range(self.tableWidget.rowCount()):

            key_item = self.tableWidget.item(row_index, 0)
            key = key_item.text() if "text" in key_item.__dir__() else ""

            value_item = self.tableWidget.item(row_index, 1)
            value = value_item.text() if "text" in value_item.__dir__() else ""

            if not key:
                continue

            data[key] = value

        self.season.custom_data = data

    def accept(self) -> None:
        self.save_data()

        if self.picture_filepath:
            save_cover(self.picture_filepath, self.parent.parent.parent.profile.path, "season", self.season.id)

        super().accept()

    def reject(self) -> None:
        super().reject()

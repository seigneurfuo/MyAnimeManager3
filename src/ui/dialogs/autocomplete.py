from typing import Any


import os

from utils import load_animes_json_data, save_cover, download_picture

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt6.uic import loadUi


class AutocompleteDialog(QDialog):
    def __init__(self, parent, season_name) -> None:
        super().__init__(parent=parent)

        self.anime_title = season_name

        self.anime_data = None
        self.animes_data = load_animes_json_data()
        self.picture_tmp_filepath = None

        self.init_ui()
        self.init_events()

    def init_ui(self) -> None:
        loadUi(os.path.join(os.path.dirname(__file__), "autocomplete.ui"), self)
        self.setWindowTitle(self.tr("Recherche des complétions automatiques"))

        self.lineEdit.setText(self.anime_title)

        self.fill_table_data()

    def init_events(self) -> None:
        self.lineEdit.textChanged.connect(self.when_search_text_changed)

        self.tableWidget.currentItemChanged.connect(self.when_current_index_changed)

    def when_search_text_changed(self):
        self.fill_table_data()

    def filter_animes_data(self): 
        text = self.lineEdit.text().lower()
        if not text:
            return []
        
        def filter_anime(anime_data):
            return anime_data["title"].lower().startswith(text)

        return list(filter(filter_anime, self.animes_data["data"]))

    def get_anime_data(self, anime_data, anime_index):
        if anime_index is not None:
            animes_data = self.filter_animes_data()
            anime_data = animes_data[anime_index]
            del animes_data

        # Modification des données avant renvoit
        anime_data["year"] = anime_data["animeSeason"]["year"] if "animeSeason" in anime_data and "year" in anime_data["animeSeason"] else ""
        #anime_data["synonyms"] = "" #str(" ".join(anime_data["synonyms"]))
        anime_data["sources"] = "" #str(" ".join(anime_data["sources"]))
        anime_data["picture"] = anime_data["picture"] if anime_data["picture"].lower().startswith("http") else None

        return anime_data

    def fill_table_data(self) -> None:
        self.tableWidget.clearContents()

        data = self.filter_animes_data()

        row_count = len(data)
        self.label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.tableWidget.setRowCount(row_count)

        for row_index, anime_data in enumerate(data):
            anime_data = self.get_anime_data(anime_data, None)
            columns = [anime_data["title"], str(anime_data["year"]), str(anime_data["episodes"]), "", ""]

            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                item.setData(Qt.ItemDataRole.UserRole, row_index)
                self.tableWidget.setItem(row_index, col_index, item)

        #self.tableWidget.resizeColumnsToContents()
        #self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
        #                                                            QHeaderView.ResizeMode.ResizeToContents)

    def when_current_index_changed(self):
        # TODO récupérer l'index
        current_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        
        if current_item:
            anime_index = current_item.data(Qt.ItemDataRole.UserRole)
            anime_data = self.get_anime_data(None, anime_index)
            self.anime_data = anime_data
            self.fill_anime_data(anime_data)

    def fill_anime_data(self, anime_data):
        synonyms_list = anime_data["synonyms"]
        synonyms_index = min(len(synonyms_list), 6)
        synonyms = ", \n".join(synonyms_list[:synonyms_index])

        fields = [
            (self.label_8, anime_data["title"]),
            (self.label_11, synonyms),
            (self.label_5, str(anime_data["episodes"])),
            (self.label_7, str(anime_data["year"]))
        ]

        for field, value in fields:
            field.setText(value)

        # Image de couverture
        pixmap_label = self.label_10
        picture_url = anime_data["picture"]

        # TODO: Thread en arrière plan pour gérer l'image (comme ça évite de tout bloquer si on n'a pas internet)
        pixmap = QPixmap()
        if picture_url:
            self.picture_tmp_filepath = download_picture(picture_url)
            if self.picture_tmp_filepath:  
                pixmap = QPixmap.fromImage(QImage(self.picture_tmp_filepath)).scaled(pixmap_label.width(), pixmap_label.height(), Qt.AspectRatioMode.KeepAspectRatio)

        pixmap_label.setPixmap(pixmap)

    def accept(self) -> None:
        del self.animes_data

        if self.anime_data:
            self.anime_data["picture_tmp_filepath"] = self.picture_tmp_filepath
            self.anime_data["save_type"] = self.comboBox.currentIndex()
        
        super().accept()

    def reject(self) -> None:
        self.anime_data = None
        del self.animes_data
        super().reject()

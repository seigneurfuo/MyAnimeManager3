#!/bin/env python3
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDir

import os

from database import Series, Seasons


class FullListTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self.init_ui()
        self.init_events()

        self.current_serie_id = None
        self.current_season_id = None

        self.fill_series_combobox()

    def init_ui(self):
        loadUi(os.path.join(QDir.currentPath(), 'ui/full_list_tab_tree.ui'), self)


    def init_events(self):
        self.comboBox.currentIndexChanged.connect(self.on_series_list_current_index_changed)
        # self.pushButton.clicked.connect(self._on_serie_edit)
        self.tableWidget.currentItemChanged.connect(self.on_seasons_list_current_index_changed)

        # region ----- Boutons -----
        self.delete_serie_button.clicked.connect(self.on_delete_serie_button_clicked)
        # endregion

        pass

    # region ----- Serie combobox -----
    def fill_series_combobox(self):
        self.comboBox.clear()
        for serie in Series.select().order_by(Series.sort_id):
            self.comboBox.addItem(serie.name)
    # endregion

    def on_series_list_current_index_changed(self, index):
        # ----- -----
        # FIXME: Changer de le mode détection de la série
        serie = Series.select().where(Series.name == self.comboBox.currentText()).get()
        self.current_serie_id = serie.id_
        self.fill_serie_data(serie)
        self.fill_season_list(serie)

    # region ----- Remplissage de la liste des informations sur la série -----
    def fill_serie_data(self, serie):
        fields = [(self.label_3, serie.name)]
        for field, value in fields:
            field.setText(value)

        self.plainTextEdit.setPlainText(serie.description)
    # endregion

    def on_delete_serie_button_clicked(self):
        # FIXME: Cascade SQL Delete

        # ----- Supression des saisons -----
        seasons = Seasons.select().where(Seasons.serie == self.current_serie_id).order_by(Seasons.sort_id)
        print([season.name for season in seasons])
        for season in seasons:
            Seasons.delete_by_id(season.id_)

        # ----- Supression de la série -----
        Series.delete_by_id(self.current_serie_id)

        self.fill_series_combobox()
        self.fill_serie_data()

    # region ----- Remplissage de la liste des saisons -----
    def fill_season_list(self, serie):
        self.tableWidget.setRowCount(0)

        seasons = Seasons.select().where(Seasons.serie == serie.id_).order_by(Seasons.sort_id)
        self.label_2.setText(str(len(seasons)))

        self.tableWidget.setRowCount(len(seasons))

        for row_id, season in enumerate(seasons):
            self.tableWidget.setItem(row_id, 0, QTableWidgetItem(season.seasons_type.name))
            self.tableWidget.setItem(row_id, 1, QTableWidgetItem(season.name))
    # endregion

    def fill_season_data(self, season):
        print(season.name)

    def on_seasons_list_current_index_changed(self):
        # TODO:
        #season = Series.select().where(Series.name == self.comboBox.currentText()).get()
        # self.current_season_id = season.id_

        pass

    # endregion

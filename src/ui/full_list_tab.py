#!/bin/env python3
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDir, Qt

import os
from pathlib import Path

from ui.dialogs.series import SeriesDialog
from ui.dialogs.deleted_elements import DeletedElements
from database import Series, Seasons, database
from common import show_view_history_dialog


class FullListTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.current_serie_id = None
        self.current_season_id = None

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), 'full_list_tab.ui'), self)

    def init_events(self):
        self.comboBox.currentIndexChanged.connect(self.on_series_list_current_index_changed_function)
        # self.pushButton.clicked.connect(self._on_serie_edit)
        self.tableWidget.currentItemChanged.connect(self.on_seasons_list_current_index_changed_function)

        # region ----- Boutons -----
        self.add_serie_button.clicked.connect(self.on_add_serie_button_clicked_function)
        self.edit_serie_button.clicked.connect(self.on_edit_serie_button_clicked_function)

        # FIXME:
        self.delete_serie_button.clicked.connect(self.on_delete_serie_button_clicked_function)

        self.delete_season_button.clicked.connect(self.on_delete_season_button_clicked_function)

        self.view_deleted_elements_button.clicked.connect(self.on_view_deleted_elements_button_clicked_function)
        # TODO: pushButton_2
        self.show_view_history_button.clicked.connect(self.when_show_view_history_button_is_clicked)
        # endregion

    def when_visible(self):
        self.fill_series_combobox()

        # TODO: à garder ou pas ?
        # On force l'affichage de l'informaton pour la première série au lancement
        self.on_series_list_current_index_changed_function()

    # region ----- Serie combobox -----
    def fill_series_combobox(self):
        self.comboBox.clear()

        series = Series.select().where(Series.is_deleted == 0).order_by(Series.sort_id)
        for serie in series:
            text = "{0} - {1}".format(serie.sort_id, serie.name)
            self.comboBox.addItem(text, userData=serie.id)

        self.current_serie_id = self.comboBox.currentData()

    # endregion

    def on_series_list_current_index_changed_function(self):
        # ----- -----

        self.current_serie_id = self.comboBox.currentData()

        if self.current_serie_id:
            serie = Series.get(Series.id == self.current_serie_id)

            self.fill_serie_data(serie)
            self.fill_season_list(serie)

    # region ----- Remplissage de la liste des informations sur la série -----
    def fill_serie_data(self, serie):
        fields = [(self.label_3, serie.name)]

        for field, value in fields:
            field.setText(value)

        # FIXME: Utiliser en fonction de la classe la bonne fonction ?
        self.plainTextEdit.setPlainText(serie.description)

    # endregion

    def on_add_serie_button_clicked_function(self):
        serie = Series()
        series_dialog = SeriesDialog(serie)

        if series_dialog.exec_():
            series_dialog.serie.save()
            self.fill_series_combobox()

    def on_edit_serie_button_clicked_function(self):
        if self.current_serie_id:
            serie = Series().get(self.current_serie_id)

            series_dialog = SeriesDialog(serie)
            if series_dialog.exec_():
                self.when_visible()

    def on_delete_serie_button_clicked_function(self):
        if self.current_serie_id:
            # ----- Supression des saisons -----
            serie = Series.get(self.current_serie_id)
            serie.is_deleted = 1
            serie.save()

            # self.on_series_list_current_index_changed()
            self.fill_series_combobox()

    def on_delete_season_button_clicked_function(self):
        if self.current_season_id:
            season = Seasons.get(self.current_season_id)
            season.is_deleted = 1
            season.save()

            #self.on_series_list_current_index_changed_function()

    def on_view_deleted_elements_button_clicked_function(self):
        deleted_series = Series.select().where(Series.is_deleted == 1).order_by(Series.sort_id)
        deleted_seasons = Seasons.select().where(Seasons.is_deleted == 1).order_by(Seasons.sort_id)
        print(deleted_seasons)
        dialog = DeletedElements(deleted_series, deleted_seasons)

        # TODO:
        if dialog.exec_():
            pass

    # region ----- Remplissage de la liste des saisons -----
    def fill_season_list(self, serie):
        self.tableWidget.setRowCount(0)

        seasons = Seasons.select().where(Seasons.serie == serie.id, Seasons.is_deleted == 0).order_by(Seasons.sort_id)
        seasons_count = len(seasons)

        self.label_2.setText(str(seasons_count))

        self.tableWidget.setRowCount(seasons_count)
        for row_index, season in enumerate(seasons):
            columns = [season.type.name, season.name]

            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, season.id)
                self.tableWidget.setItem(row_index, col_index, item)

        # Si on à au moiins une série, alors on affiche la première de la liste
        # if seasons:
        # self.tableWidget.setCurrentCell(0, 0)

        # endregion

    def fill_season_data(self, season):
        fields = [(self.label_8, season.name),
                  (self.label_10, season.date)]

        for field, value in fields:
            field.setText(value)


    def on_seasons_list_current_index_changed_function(self):
        # self.tableWidget.currentItem()
        current_row = self.tableWidget.currentRow()
        current_item = self.tableWidget.item(current_row, 0)

        # TODO: Click automatique sur le premier élement lors du changement si une saison existe ?
        if current_item:
            self.current_season_id = current_item.data(Qt.UserRole)
            print(self.current_season_id)

        season = Seasons.get(Seasons.id == self.current_season_id)
        self.fill_season_data(season)

    def when_show_view_history_button_is_clicked(self):
        if self.current_season_id:
            show_view_history_dialog(self.current_season_id)

    # endregion

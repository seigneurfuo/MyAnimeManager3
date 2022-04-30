#!/bin/env python3
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

import os

from ui.dialogs.serie import SerieDialog
from ui.dialogs.season import SeasonDialog
from ui.dialogs.deleted_elements import DeletedElements
from database import database, Series, Seasons, SeasonsTypes
from common import show_watch_history_dialog


class FullListTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.current_serie_id = None
        self.current_season_id = None

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "full_list_tab.ui"), self)

    def init_events(self):
        self.comboBox.currentIndexChanged.connect(self.when_series_list_current_index_changed)
        # self.pushButton.clicked.connect(self._on_serie_edit)
        self.tableWidget.currentItemChanged.connect(self.when_seasons_list_current_index_changed)

        # region ----- Boutons -----
        self.add_serie_button.clicked.connect(self.when_add_serie_button_clicked)
        self.edit_serie_button.clicked.connect(self.when_edit_serie_button_clicked)
        # FIXME:
        self.delete_serie_button.clicked.connect(self.when_delete_serie_button_clicked)

        self.add_season_button.clicked.connect(self.when_add_season_button_clicked)
        self.edit_season_button.clicked.connect(self.when_edit_season_button_clicked)
        self.delete_season_button.clicked.connect(self.when_delete_season_button_clicked)

        self.view_deleted_elements_button.clicked.connect(self.when_view_deleted_elements_button_clicked)
        # TODO: pushButton_2
        self.show_view_history_button.clicked.connect(self.when_show_view_history_button_is_clicked)

        self.search_box.textChanged.connect(self.when_search_box_content_changed)
        # endregion

    def when_visible(self):
        self.fill_series_combobox()

        # TODO: à garder ou pas ?
        # On force l'affichage de l'informaton pour la première série au lancement
        self.when_series_list_current_index_changed()

    # region ----- Serie combobox -----
    def fill_series_combobox(self, search_query=None):
        self.comboBox.clear()

        if search_query:
            series = Series().select().where(Series.is_deleted == 0, Series.name.contains(search_query)).order_by(Series.sort_id)
        else:
            series = Series().select().where(Series.is_deleted == 0).order_by(Series.sort_id)

        for serie in series:
            text = "{0} - {1}".format(serie.sort_id, serie.name)
            self.comboBox.addItem(text, userData=serie.id)

        self.current_serie_id = self.comboBox.currentData()

    # endregion

    def when_series_list_current_index_changed(self):
        # ----- -----

        self.current_serie_id = self.comboBox.currentData()

        if self.current_serie_id:
            serie = Series().get(Series.id == self.current_serie_id)

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

    def when_add_serie_button_clicked(self):
        serie = Series()
        series_dialog = SerieDialog(serie)

        if series_dialog.exec_():
            self.fill_series_combobox()

    def when_edit_serie_button_clicked(self):
        if self.current_serie_id:
            serie = Series().get(self.current_serie_id)

            series_dialog = SerieDialog(serie)
            if series_dialog.exec_():
                self.when_visible()

    def when_delete_serie_button_clicked(self):
        if self.current_serie_id:
            # ----- Supression des saisons -----
            serie = Series().get(self.current_serie_id)
            serie.is_deleted = 1
            serie.save()

            # self.on_series_list_current_index_changed()
            self.fill_series_combobox()

    def when_add_season_button_clicked(self):
        if self.current_serie_id:
            # ----- Supression des saisons -----
            season = Seasons()
            serie = Series().get(self.current_serie_id)
            seasons_types = SeasonsTypes().select(1) # FIXME
            season_dialog = SeasonDialog(season, serie, seasons_types)

            if season_dialog.exec_():
                self.when_visible()

    def when_edit_season_button_clicked(self):
        if self.current_season_id:
            season = Seasons().get(self.current_season_id)
            seasons_types = SeasonsTypes().select(1) # FIXME
            season_dialog = SeasonDialog(season, serie=None, seasons_types=seasons_types)
            if season_dialog.exec_():
                self.when_visible()

    def when_delete_season_button_clicked(self):
        if self.current_season_id:
            season = Seasons().get(self.current_season_id)
            serie = Series().get(Series.id == self.current_serie_id)

            season.is_deleted = 1
            season.save()

            self.fill_serie_data(serie)
            self.fill_season_list(serie)

    def when_view_deleted_elements_button_clicked(self):
        deleted_series = Series().select().where(Series.is_deleted == 1).order_by(Series.sort_id)
        deleted_seasons = Seasons().select().where(Seasons.is_deleted == 1).order_by(Seasons.sort_id)
        print(deleted_seasons)
        dialog = DeletedElements(deleted_series, deleted_seasons)

        # TODO:
        if dialog.exec_():
            pass

    # region ----- Remplissage de la liste des saisons -----
    def fill_season_list(self, serie):
        seasons = Seasons().select().where(Seasons.serie == serie.id, Seasons.is_deleted == 0).order_by(Seasons.sort_id)
        row_count = len(seasons)
        self.label_2.setText(str(row_count))
        self.tableWidget.setRowCount(row_count)
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


    def when_seasons_list_current_index_changed(self):
        # self.tableWidget.currentItem()
        current_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)

        # TODO: Click automatique sur le premier élement lors du changement si une saison existe ?
        if current_item:
            self.current_season_id = current_item.data(Qt.UserRole)
            print(self.current_season_id)

        season = Seasons().get(Seasons.id == self.current_season_id)
        self.fill_season_data(season)

    def when_show_view_history_button_is_clicked(self):
        if self.current_season_id:
            show_watch_history_dialog(self.current_season_id)


    def when_search_box_content_changed(self):
        search_query = self.search_box.text()
        self.fill_series_combobox(search_query)

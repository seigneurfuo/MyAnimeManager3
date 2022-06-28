#!/bin/env python3
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QUrl

import os

from ui.dialogs.serie import SerieDialog
from ui.dialogs.season import SeasonDialog
from ui.dialogs.deleted_elements import DeletedElements
from database import database, Series, Seasons, SeasonsTypes
from common import display_view_history_dialog


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
        self.tableWidget.currentItemChanged.connect(self.when_seasons_list_current_index_changed)

        # region ----- Boutons -----
        self.pushButton_5.clicked.connect(self.when_search_box_clear_button_clicked)

        self.add_serie_button.clicked.connect(self.when_add_serie_button_clicked)
        self.edit_serie_button.clicked.connect(self.when_edit_serie_button_clicked)
        self.delete_serie_button.clicked.connect(self.when_delete_serie_button_clicked)  # FIXME:

        self.add_season_button.clicked.connect(self.when_add_season_button_clicked)
        self.edit_season_button.clicked.connect(self.when_edit_season_button_clicked)
        self.delete_season_button.clicked.connect(self.when_delete_season_button_clicked)

        self.view_deleted_elements_button.clicked.connect(self.when_view_deleted_elements_button_clicked)
        self.pushButton.clicked.connect(self.when_view_history_button_clicked)
        # TODO: pushButton_2
        self.open_folder_button.clicked.connect(self.when_open_folder_button_clicked)
        self.show_view_history_button.clicked.connect(self.when_show_view_history_button_is_clicked)

        self.search_box.textChanged.connect(self.when_search_box_content_changed)
        self.search_box.returnPressed.connect(self.when_search_box_content_changed)
        # endregion

    def when_visible(self):
        self.refresh_data()

    def refresh_data(self):
        self.fill_series_combobox()

        # TODO: à garder ou pas ?
        # On force l'affichage de l'informaton pour la première série au lancement
        self.when_series_list_current_index_changed()

    def fill_series_combobox(self, search_query=None):
        self.comboBox.clear()

        if search_query:
            series = Series().select().where(Series.is_deleted == 0, Series.name.contains(search_query)).order_by(
                Series.sort_id)
        else:
            series = Series().select().where(Series.is_deleted == 0).order_by(Series.sort_id)

        for serie in series:
            text = "{0} - {1}".format(serie.sort_id, serie.name)
            self.comboBox.addItem(text, userData=serie.id)

        self.current_serie_id = self.comboBox.currentData()

    def set_series_combobox_current_selection(self, serie_id):
        index = self.comboBox.findData(serie_id)
        self.comboBox.setCurrentIndex(index)

    def when_series_list_current_index_changed(self):
        self.current_serie_id = self.comboBox.currentData()

        if self.current_serie_id:
            serie = Series().get(Series.id == self.current_serie_id)

            self.fill_serie_data(serie)
            self.fill_season_list(serie)

    def fill_serie_data(self, serie):
        fields = [(self.label_3, serie.name)]

        for field, value in fields:
            field.setText(value)

    def when_add_serie_button_clicked(self):
        serie = Series()
        series_dialog = SerieDialog(serie)

        if series_dialog.exec_():
            self.refresh_data()
            self.set_series_combobox_current_selection(serie.id)

    def when_edit_serie_button_clicked(self):
        if self.current_serie_id:
            serie = Series().get(self.current_serie_id)

            series_dialog = SerieDialog(serie)
            if series_dialog.exec_():
                self.refresh_data()
                self.set_series_combobox_current_selection(serie.id)

    def when_delete_serie_button_clicked(self):
        if self.current_serie_id:
            # ----- Supression des saisons -----
            serie = Series().get(self.current_serie_id)
            serie.is_deleted = 1
            serie.save()

            self.refresh_data()

    def when_add_season_button_clicked(self):
        if self.current_serie_id:
            # ----- Supression des saisons -----
            season = Seasons()
            serie = Series().get(self.current_serie_id)
            seasons_types = SeasonsTypes().select()
            season_dialog = SeasonDialog(season, serie, seasons_types)

            if season_dialog.exec_():
                self.refresh_data()

    def when_edit_season_button_clicked(self):
        if self.current_season_id:
            season = Seasons().get(self.current_season_id)
            seasons_types = SeasonsTypes().select()
            season_dialog = SeasonDialog(season, serie=None, seasons_types=seasons_types)
            if season_dialog.exec_():
                self.refresh_data()
                self.set_series_combobox_current_selection(season.serie.id)

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
        dialog = DeletedElements(deleted_series, deleted_seasons)

        # TODO:
        if dialog.exec_():
            pass

    def when_view_history_button_clicked(self):
        if self.current_season_id:
            display_view_history_dialog(self.current_season_id)

    def fill_season_list(self, serie):
        seasons = Seasons().select().where(Seasons.serie == serie.id, Seasons.is_deleted == 0).order_by(Seasons.sort_id)
        row_count = len(seasons)
        self.label_2.setText(str(row_count))
        self.tableWidget.setRowCount(row_count)

        for row_index, season in enumerate(seasons):
            columns = [str(season.sort_id), season.type.name, season.name]

            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                item.setData(Qt.UserRole, season.id)
                self.tableWidget.setItem(row_index, col_index, item)

        # Si on à au moins une série, alors on affiche la première de la liste
        if seasons:
            self.tableWidget.setCurrentCell(0, 0)
            self.when_seasons_list_current_index_changed()

    def fill_season_data(self, season):
        fields = [(self.label_12, str(season.sort_id)),
                  (self.label_8, season.name),
                  (self.label_10, str(season.year)),
                  (self.label_16, str(season.episodes)),
                  (self.label_17, str(season.watched_episodes)),
                  (self.label_19, str(season.view_count))]

        for field, value in fields:
            field.setText(value)


        self.label_4.setVisible(season.favorite)
        self.plainTextEdit.setPlainText(season.description)

        # On masque ou none le bouton pour parcourir le dossier
        self.open_folder_button.setEnabled(os.path.exists(season.serie.path))

    def clear_season_data(self):
        fields = [self.label_12,
                  self.label_8,
                  self.label_10,
                  self.label_16,
                  self.label_17,
                  self.label_19]

        for field in fields:
            field.clear()

        self.open_folder_button.setEnabled(False)

    def when_seasons_list_current_index_changed(self):
        current_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)

        if current_item:
            self.current_season_id = current_item.data(Qt.UserRole)

            season = Seasons().get(Seasons.id == self.current_season_id)
            self.fill_season_data(season)

        else:
            self.clear_season_data()

    def when_show_view_history_button_is_clicked(self):
        if self.current_season_id:
            display_view_history_dialog(self.current_season_id)

    def when_search_box_content_changed(self):
        search_query = self.search_box.text()
        self.fill_series_combobox(search_query)

    def when_search_box_clear_button_clicked(self):
        self.search_box.clear()

    def when_open_folder_button_clicked(self):
        if self.current_season_id:
            season = Seasons().get(Seasons.id == self.current_season_id)
            if os.path.exists(season.serie.path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(season.serie.path))

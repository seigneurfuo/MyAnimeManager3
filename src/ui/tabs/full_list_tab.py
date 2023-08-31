#!/bin/env python3
import io

from PyQt6.QtGui import QDesktopServices, QPixmap, QIcon, QImage
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QCompleter
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QUrl

import os

from core import SEASONS_STATES
from common import display_view_history_dialog
from database import Series, Seasons, SeasonsTypes, FriendsPlanning, Friends, Planning

from ui.dialogs.serie import SerieDialog
from ui.dialogs.season import SeasonDialog
from ui.dialogs.deleted_elements import DeletedElementsDialog

import core


class FullListTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.init_ui()
        self.init_events()

        self.clear_season_data()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "full_list_tab.ui"), self)

    def init_events(self):
        self.comboBox.currentIndexChanged.connect(self.when_series_list_current_index_changed)
        self.tableWidget.currentItemChanged.connect(self.when_seasons_list_current_index_changed)
        self.tableWidget.doubleClicked.connect(self.when_serie_double_clicked)

        # region ----- Boutons -----
        self.add_serie_button.clicked.connect(self.when_add_serie_button_clicked)
        self.edit_serie_button.clicked.connect(self.when_edit_serie_button_clicked)
        self.delete_serie_button.clicked.connect(self.when_delete_serie_button_clicked)  # FIXME:

        self.add_season_button.clicked.connect(self.when_add_season_button_clicked)
        self.edit_season_button.clicked.connect(self.when_edit_season_button_clicked)
        self.delete_season_button.clicked.connect(self.when_delete_season_button_clicked)

        self.view_deleted_elements_button.clicked.connect(self.when_view_deleted_elements_button_clicked)

        self.open_folder_button.clicked.connect(self.when_open_folder_button_clicked)
        self.show_view_history_button.clicked.connect(self.when_show_view_history_button_clicked)

        self.previous_serie_button.clicked.connect(self.when_previous_serie_button_clicked)
        self.next_serie_button.clicked.connect(self.when_next_serie_button_clicked)
        # endregion

    def when_visible(self):
        self.refresh_data()

    def refresh_data(self):
        self.fill_series_combobox()

    def get_current_serie_id(self):
        return self.comboBox.currentData()

    def get_current_season_id(self):
        current_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        return current_item.data(Qt.ItemDataRole.UserRole) if current_item else None

    def fill_series_combobox(self):
        self.comboBox.clear()
        completer_data = []
        series = Series().select().where(Series.is_deleted == 0).order_by(Series.sort_id)
        for index, serie in enumerate(series):
            text = "{:03d} - {}".format(serie.sort_id, serie.name)
            self.comboBox.addItem(text, userData=serie.id)

            # Autocomplétion
            completer_data.append(text)

        completer = QCompleter(completer_data)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.comboBox.setCompleter(completer)

    def set_series_combobox_current_selection(self, serie_id):
        index = self.comboBox.findData(serie_id)
        self.comboBox.setCurrentIndex(index)

    def when_series_list_current_index_changed(self):
        self.clear_serie_data()

        current_serie_id = self.get_current_serie_id()
        if current_serie_id:
            serie = Series().get(current_serie_id)

            self.fill_serie_data(serie)
            self.fill_season_list(serie)

        else:
            #self.current_season_id = 0 # FIXME
            self.tableWidget.setRowCount(0)

        self.clear_season_data()

    def fill_serie_data(self, serie):
        fields = [(self.label_3, serie.name)]

        for field, value in fields:
            field.setText(value)

        # Image de la série
        if serie.picture:
            with io.BytesIO(serie.picture) as picture_data:
                pixmap = QPixmap.fromImage(QImage.fromData(picture_data.read()))

            self.label_6.setScaledContents(True)
            self.label_6.setPixmap(pixmap)

        # On masque ou non le bouton pour parcourir le dossier de la série
        self.open_folder_button.setEnabled(os.path.exists(serie.path))

    def clear_serie_data(self):
        fields = [self.label_3, self.label_2, self.label_6]

        for field in fields:
            field.clear()

        # On masque pour parcourir le dossier de la série
        self.open_folder_button.setEnabled(False)

    def when_add_serie_button_clicked(self):
        serie = Series()
        series_dialog = SerieDialog(self, serie)

        if series_dialog.exec():
            self.refresh_data()
            self.set_series_combobox_current_selection(serie.id)

    def when_edit_serie_button_clicked(self):
        current_serie_id = self.get_current_serie_id()
        if current_serie_id:
            serie = Series().get(current_serie_id)

            series_dialog = SerieDialog(self, serie)
            if series_dialog.exec():
                self.refresh_data()
                self.set_series_combobox_current_selection(serie.id)

    def when_delete_serie_button_clicked(self):
        current_serie_id = self.get_current_serie_id()
        if current_serie_id:
            # ----- Supression des saisons -----
            serie = Series().get(current_serie_id)
            serie.is_deleted = 1
            serie.save()

            self.refresh_data()

    def when_add_season_button_clicked(self):
        current_serie_id = self.get_current_serie_id()
        if current_serie_id:
            # ----- Supression des saisons -----
            season = Seasons()
            serie = Series().get(current_serie_id)
            seasons_types = SeasonsTypes().select()
            season_dialog = SeasonDialog(self, season, serie, seasons_types)

            if season_dialog.exec():
                self.refresh_data()
                self.set_series_combobox_current_selection(serie.id)

    def edit_season(self):
        current_season_id = self.get_current_season_id()
        if current_season_id:
            season = Seasons().get(current_season_id)
            seasons_types = SeasonsTypes().select()
            season_dialog = SeasonDialog(self, season, serie=None, seasons_types=seasons_types)
            if season_dialog.exec():
                self.refresh_data()
                self.set_series_combobox_current_selection(season.serie.id)

    def when_edit_season_button_clicked(self):
        self.edit_season()

    def when_serie_double_clicked(self):
        self.edit_season()

    def when_delete_season_button_clicked(self):
        current_serie_id = self.get_current_serie_id()
        current_season_id = self.get_current_season_id()
        if current_season_id:
            serie = Series().get(current_serie_id)
            season = Seasons().get(current_season_id)

            season.is_deleted = 1
            season.save()

            self.fill_serie_data(serie)
            self.fill_season_list(serie)

    def when_view_deleted_elements_button_clicked(self):
        deleted_series = Series().select().where(Series.is_deleted == 1).order_by(Series.sort_id)
        deleted_seasons = Seasons().select().where(Seasons.is_deleted == 1).join(Series).order_by(Seasons.sort_id)
        dialog = DeletedElementsDialog(self, deleted_series, deleted_seasons)

        # FIXME: Ne veut pas changer la valeur ...
        if dialog.exec():
            if dialog.series_to_restore:
                for serie_id in dialog.series_to_restore:
                    serie = Seasons.get(serie_id)
                    serie.is_deleted = 0
                    serie.save()

            if dialog.seasons_to_restore:
                for season_id in dialog.seasons_to_restore:
                    season = Seasons.get(season_id)
                    season.is_deleted = 0
                    season.save()

            if dialog.series_to_restore or dialog.seasons_to_restore:
                self.refresh_data()


    def when_view_history_button_clicked(self):
        current_season_id = self.get_current_season_id()
        if current_season_id:
            display_view_history_dialog(self, current_season_id)

    def fill_season_list(self, serie):
        seasons = serie.seasons.where(Seasons.is_deleted == 0).order_by(Seasons.sort_id)
        row_count = len(seasons)
        self.label_2.setText(str(row_count))
        self.tableWidget.setRowCount(row_count)

        for row_index, season in enumerate(seasons):
            columns = [season.sort_id, season.name, season.type.name,
                       season.year if season.year and str(season.year) != "None" else "",
                       season.episodes, season.watched_episodes, season.view_count, SEASONS_STATES[season.state],
                       season.rating]

            # Si on à activé la gestion des amis:
            if self.parent.parent.settings["friends_enabled"]:
                friends = [friend.name for friend in
                           Friends.select(Friends.name).where(Seasons.id == season.id).join(FriendsPlanning)
                           .join(Planning).join(Seasons).group_by(Friends.name)]

                columns.append(", ".join(friends))

            # Sinon on masque la colonne:
            else:
                self.tableWidget.horizontalHeader().hideSection(len(columns))

            for col_index, value in enumerate(columns):
                if col_index == 7:
                    item = QTableWidgetItem(value["name"])
                    item.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "../../resources/icons/", value["icon"])))
                    item.setToolTip(item.text())

                elif col_index == 8:
                    rating = next(rating for rating in core.RATING_LEVELS if rating["value"] == season.rating)
                    icon_path = os.path.join(os.path.dirname(__file__), "../../resources/icons", rating["icon"])
                    item = QTableWidgetItem()
                    item.setIcon(QIcon(icon_path))

                else:
                    item = QTableWidgetItem(str(value))
                    item.setToolTip(item.text())
                    item.setData(Qt.ItemDataRole.UserRole, season.id)

                self.tableWidget.setItem(row_index, col_index, item)

        self.tableWidget.clearSelection()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
                                                                 QHeaderView.ResizeMode.ResizeToContents)

    def fill_season_data(self, season):
        # Note
        rating = next(rating for rating in core.RATING_LEVELS if rating["value"] == season.rating)
        pixmap_path = os.path.join(os.path.dirname(__file__), "../../resources/icons", rating["icon"])
        # TODO: Ratio à conserver
        self.label_4.setPixmap(QPixmap(pixmap_path))

        self.plainTextEdit.setPlainText(season.description)
        self.show_view_history_button.setEnabled(True)

    def clear_season_data(self):
        self.plainTextEdit.clear()
        self.show_view_history_button.setEnabled(False)
        self.label_4.setPixmap(QPixmap())
        self.plainTextEdit.clear()

    def when_seasons_list_current_index_changed(self):
        current_season_id = self.get_current_season_id()
        if current_season_id:
            season = Seasons().get(current_season_id)
            self.fill_season_data(season)

        else:
            self.clear_season_data()

    def when_show_view_history_button_clicked(self):
        current_season_id = self.get_current_season_id()
        if current_season_id:
            display_view_history_dialog(self, current_season_id)

    def when_open_folder_button_clicked(self):
        current_serie_id = self.get_current_serie_id()
        if current_serie_id:
            serie = Series().get(current_serie_id)
            if os.path.exists(serie.path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(serie.path))

    def when_previous_serie_button_clicked(self):
        if self.comboBox.currentIndex() > 0:
            self.comboBox.setCurrentIndex(self.comboBox.currentIndex() - 1)

    def when_next_serie_button_clicked(self):
        if self.comboBox.currentIndex() < self.comboBox.count() - 1:
            self.comboBox.setCurrentIndex(self.comboBox.currentIndex() + 1)

#!/usr/bin/python3

import os
from datetime import datetime

from PyQt6.QtGui import QIcon, QColor, QPixmap

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QCheckBox, QHeaderView, QMessageBox, QLabel
from PyQt6.uic import loadUi

import utils

from core import SEASONS_STATES, RATING_LEVELS
from common import display_view_history_dialog
from database import Series, Seasons, Friends, Planning, FriendsPlanning, SeasonsTypes

import core


class List2(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "list2_tab.ui"), self)

        # Remplissage de l'état des saisons
        for index, season_state in enumerate(core.SEASONS_STATES):
            state_icon = os.path.join(os.path.dirname(__file__), "../../resources/icons/", season_state["icon"])
            self.comboBox.addItem(QIcon(state_icon), season_state["name"], userData=index)

        # Remplissage des types
        for seasons_type in SeasonsTypes().select():
            self.comboBox_2.addItem(seasons_type.name, userData=seasons_type.id)

    def init_events(self):
        self.pushButton.clicked.connect(self.when_export_button_clicked)
        self.pushButton_2.clicked.connect(self.when_show_view_history_button_clicked)
        self.go_to_serie_data_button.clicked.connect(self.when_go_to_serie_data_button_clicked)
        self.tableWidget.currentCellChanged.connect(self.when_current_cell_changed)
        self.refresh_button.clicked.connect(self.refresh_data)

    def when_visible(self):
        self.refresh_data()

    def refresh_data(self):
        self.fill_data()

        self.pushButton_2.setEnabled(False)
        self.go_to_serie_data_button.setEnabled(False)

    def when_current_cell_changed(self):
        self.pushButton_2.setEnabled(True)
        self.go_to_serie_data_button.setEnabled(True)

    def when_show_view_history_button_clicked(self):
        current_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        current_season_id = current_item.data(Qt.ItemDataRole.UserRole) if current_item else None

        if current_season_id:
            display_view_history_dialog(self, current_season_id)

    def when_go_to_serie_data_button_clicked(self):
        current_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        current_season_id = current_item.data(Qt.ItemDataRole.UserRole) if current_item else None

        if current_season_id:
            season = Seasons().get(current_season_id)

            self.parent.tabWidget.setCurrentIndex(1)
            self.parent.full_list_tab.set_series_combobox_current_selection(season.serie.id)

    def get_request_with_filters(self):
        request = Seasons().select().where(Seasons.is_deleted == 0)

        start_year = self.start_year_spinbox.value()
        stop_year = self.stop_year_spinbox.value()
        season_state = self.comboBox.currentData()
        season_type = self.comboBox_2.currentData()

        # Filtrage: année de début
        if start_year != 0:
            request = request.where(Seasons.year >= start_year)

        # Filtrae: année de fin
        if stop_year != 0:
            request = request.where(Seasons.year <= stop_year)

        # Filtrage: En cours de diffusion
        if self.airing_checkbox.isChecked():
            request = request.where(Seasons.airing)

        # Filtrage par état
        if season_state:
            request = request.where(Seasons.state == season_state)

        # Filtrage par type
        if season_type:
            request = request.where(Seasons.type == season_type)

        request = request.join(Series) \
            .order_by(Seasons.serie.sort_id, Seasons.serie.name, Seasons.sort_id, Seasons.name)

        return request

    def fill_data(self):
        self.tableWidget.clearContents()

        data = self.get_request_with_filters()
        row_count = len(data)

        self.label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.tableWidget.setRowCount(row_count)

        for row_index, season in enumerate(data):
            ids = f"{season.serie.sort_id:03d} - {season.sort_id}"
            year = str(season.year) if season.year and str(season.year) != "None" else ""

            # Calcul de l'age
            age = utils.get_season_age(season)
            # Etat de la saison
            season_state = SEASONS_STATES[season.state]

            columns = [ids, season.serie.name, season.type.name, season.name, str(season.episodes), year,
                       age, season_state['name']]

            for col_index, value in enumerate(columns):
                if col_index == 7:
                    item = QTableWidgetItem(season_state["name"])
                    icon = QIcon(
                        os.path.join(os.path.dirname(__file__), "../../resources/icons/", season_state["icon"]))
                    item.setIcon(icon)

                else:
                    item = QTableWidgetItem(value)
                    item.setToolTip(item.text())

                item.setData(Qt.ItemDataRole.UserRole, season.id)

                # Bandeau orangé pour les series avec un numéro temporaire
                if col_index == 0 and season.serie.sort_id == 0:
                    item.setBackground(QColor("#FCC981"))

                self.tableWidget.setItem(row_index, col_index, item)

            # En diffusion
            airing = self.tr("Oui") if season.airing else self.tr("Non")
            item = QTableWidgetItem(airing)

            if season.airing:
                item.setForeground(QColor("#039d09"))

            item.setToolTip(item.text())
            self.tableWidget.setItem(row_index, len(columns), item)

            # Nombre de visionnages
            item = QTableWidgetItem(str(season.view_count))
            item.setToolTip(item.text())
            self.tableWidget.setItem(row_index, len(columns) + 1, item)

            # Note
            rating = next(rating for rating in core.RATING_LEVELS if rating["value"] == season.rating)
            pixmap_path = os.path.join(os.path.dirname(__file__), "../../resources/icons", rating["icon"])
            # TODO: Ratio à conserver
            rating = QLabel()
            rating.setPixmap(QPixmap(pixmap_path))
            self.tableWidget.setCellWidget(row_index, len(columns) + 2, rating)

            # Image présente ?
            picture_present_text = self.tr("Oui") if season.serie.picture else self.tr("Non")
            picture_present = QTableWidgetItem(picture_present_text)
            self.tableWidget.setItem(row_index, len(columns) + 3, picture_present)

            # Amis
            if self.parent.parent.settings["friends_enabled"]:
                friends = [friend.name for friend in
                           Friends.select(Friends.name).where(Seasons.id == season.id).join(FriendsPlanning)
                           .join(Planning).join(Seasons).group_by(Friends.name)]

                item = QTableWidgetItem(", ".join(friends))
                item.setToolTip(item.text())
                self.tableWidget.setItem(row_index, len(columns) + 4, item)

            # Sinon on masque la colonne:
            else:
                self.tableWidget.horizontalHeader().hideSection(len(columns) + 4)

        self.tableWidget.clearSelection()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
                                                                 QHeaderView.ResizeMode.ResizeToContents)

    def when_export_button_clicked(self):
        filepath = utils.export_qtablewidget(self.tableWidget, self.parent.parent.profile.path, "liste")
        # Bouton pour ouvrir le dossier ?
        QMessageBox.information(self, self.tr("Export terminé"),
                                self.tr("Le fichier a été généré ici:") + "\n    " + filepath,
                                QMessageBox.StandardButton.Ok)

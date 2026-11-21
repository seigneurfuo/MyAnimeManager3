#!/usr/bin/python3

import os
from datetime import datetime

from PyQt6.QtGui import QIcon, QColor, QPixmap

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QCheckBox, QHeaderView, QMessageBox, QLabel
from PyQt6.uic import loadUi
from peewee import JOIN

from core import SEASONS_STATES, RATING_LEVELS
from common import display_view_history_dialog
from database import Series, Seasons, Friends, Planning, FriendsPlanning, SeasonsTypes
from utils import load_cover, get_season_age, export_qtablewidget, order_by, pre_update_qtablewidget, post_update_qtablewidget


class List2(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.parent = parent

        self.init_ui()
        self.init_events()

    def init_ui(self) -> None:
        loadUi(os.path.join(os.path.dirname(__file__), "list2_tab.ui"), self)

        # Remplissage de l'état des saisons
        for index, season_state in enumerate(SEASONS_STATES):
            state_icon = os.path.join(os.path.dirname(__file__), "../../resources/icons/", season_state["icon"])
            self.comboBox.addItem(QIcon(state_icon), season_state["name"], userData=index)

        # Remplissage des types
        for seasons_type in SeasonsTypes().select():
            self.comboBox_2.addItem(seasons_type.name, userData=seasons_type.id)

    def init_events(self) -> None:
        self.pushButton.clicked.connect(self.when_export_button_clicked)
        self.pushButton_2.clicked.connect(self.when_show_view_history_button_clicked)
        self.go_to_serie_data_button.clicked.connect(self.when_go_to_serie_data_button_clicked)
        self.tableWidget.currentCellChanged.connect(self.when_current_cell_changed)
        self.refresh_button.clicked.connect(self.refresh_data)

    def when_visible(self) -> None:
        self.refresh_data()

    def refresh_data(self) -> None:
        self.fill_data()

        self.pushButton_2.setEnabled(False)
        self.go_to_serie_data_button.setEnabled(False)

    def when_current_cell_changed(self) -> None:
        self.pushButton_2.setEnabled(True)
        self.go_to_serie_data_button.setEnabled(True)

    def when_show_view_history_button_clicked(self) -> None:
        current_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        current_season_id = current_item.data(Qt.ItemDataRole.UserRole) if current_item else None

        if current_season_id:
            display_view_history_dialog(self, current_season_id)

    def when_go_to_serie_data_button_clicked(self) -> None:
        current_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        current_season_id = current_item.data(Qt.ItemDataRole.UserRole) if current_item else None

        if current_season_id:
            season = Seasons().get(current_season_id)

            self.parent.tabWidget.setCurrentIndex(1)
            self.parent.full_list_tab.set_series_combobox_current_selection(season.serie.id)

    def get_request_with_filters(self):
        # Sélection des séries et des types dans la même requête pour éviter une requête par ligne
        request = (Seasons.select(Seasons, Series, SeasonsTypes)
                   .join(Series).switch(Seasons)
                   .join(SeasonsTypes, JOIN.LEFT_OUTER)
                   .where(Seasons.is_deleted == 0).where(Series.is_deleted == 0))

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

        request = request.order_by(order_by(self.parent.parent.settings, Series), Seasons.sort_id)

        return request

    def fill_data(self) -> None:
        data = self.get_request_with_filters()
        row_count = len(data)

        self.label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        

        pre_update_qtablewidget(self.tableWidget, row_count)

        # Chargement des icônes une seule fois
        icons_dir = os.path.join(os.path.dirname(__file__), "../../resources/icons/")
        state_icons = [QIcon(os.path.join(icons_dir, season_state["icon"])) for season_state in SEASONS_STATES]
        rating_pixmaps = {rating["value"]: QPixmap(os.path.join(icons_dir, rating["icon"])) for rating in RATING_LEVELS}

        # Amis: une seule requête pour toutes les saisons
        friends_enabled = self.parent.parent.settings["friends_enabled"]
        friends_by_season = {}
        if friends_enabled:
            friends_request = (Friends.select(Seasons.id, Friends.name).join(FriendsPlanning).join(Planning)
                               .join(Seasons).group_by(Seasons.id, Friends.name).tuples())
            for season_id, friend_name in friends_request:
                friends_by_season.setdefault(season_id, []).append(friend_name)

        profile_path = self.parent.parent.profile.path

        for row_index, season in enumerate(data):
            serie = season.serie
            ids = f"{serie.sort_id:03d} - {season.sort_id}"
            year = str(season.year) if season.year and str(season.year) != "None" else ""

            # Calcul de l'age
            age = get_season_age(season)
            # Etat de la saison
            season_state = SEASONS_STATES[season.state]
            season_type = season.type.name if season.type else ""

            columns = [ids, serie.name, season_type, season.name, str(season.episodes), year,
                       age, season_state['name']]
            columns_count = len(columns)

            for col_index, value in enumerate(columns):
                if col_index == 7:
                    item = QTableWidgetItem(season_state["name"])
                    item.setIcon(state_icons[season.state])

                else:
                    item = QTableWidgetItem(value)
                    item.setToolTip(item.text())

                item.setData(Qt.ItemDataRole.UserRole, season.id)

                # Bandeau orangé pour les series avec un numéro temporaire
                if col_index == 0 and serie.sort_id == 0:
                    item.setBackground(QColor("#FCC981"))

                self.tableWidget.setItem(row_index, col_index, item)

            # En diffusion
            airing = self.tr("Oui") if season.airing else self.tr("Non")
            item = QTableWidgetItem(airing)

            if season.airing:
                item.setForeground(QColor("#039d09"))

            item.setToolTip(item.text())
            self.tableWidget.setItem(row_index, columns_count, item)

            # Nombre de visionnages
            item = QTableWidgetItem(str(season.view_count))
            item.setToolTip(item.text())
            self.tableWidget.setItem(row_index, columns_count + 1, item)

            # Note
            # TODO: Ratio à conserver
            rating = QLabel()
            rating.setPixmap(rating_pixmaps[season.rating])
            self.tableWidget.setCellWidget(row_index, columns_count + 2, rating)

            # Image présente ?
            cover_path = load_cover(profile_path, "season", season.id)
            picture_present_text = self.tr("Oui") if cover_path else self.tr("Non")
            picture_present = QTableWidgetItem(picture_present_text)
            self.tableWidget.setItem(row_index, columns_count + 3, picture_present)

            # Amis
            if friends_enabled:
                item = QTableWidgetItem(", ".join(friends_by_season.get(season.id, [])))
                item.setToolTip(item.text())
                self.tableWidget.setItem(row_index, columns_count + 4, item)

        # Colonne des amis masquée si désactivée
        friends_column = self.tableWidget.columnCount() - 1
        self.tableWidget.horizontalHeader().setSectionHidden(friends_column, not friends_enabled)

        post_update_qtablewidget(self.tableWidget)

    def when_export_button_clicked(self) -> None:
        filepath = export_qtablewidget(self.tableWidget, self.parent.parent.profile.path, "list")
        # Bouton pour ouvrir le dossier ?
        QMessageBox.information(self, self.tr("Export terminé"),
                                self.tr("Le fichier a été généré ici:") + "\n    " + filepath,
                                QMessageBox.StandardButton.Ok)

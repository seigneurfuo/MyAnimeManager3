#!/bin/env python3

import platform
import os

from PyQt5.QtCore import Qt, QDate, QUrl
from PyQt5.QtGui import QColor, QDesktopServices, QIcon
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QProgressBar, QMessageBox, QHeaderView
from PyQt5.uic import loadUi

from ui.widgets.custom_calendar import CustomCalendar
from database import Planning, Seasons
from common import display_view_history_dialog
from common import SEASONS_STATES


class PlanningTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.current_season_id = None
        self.planning_calendar = QWidget()

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "planning_tab.ui"), self)

        self.planning_calendar = CustomCalendar()
        self.planning_calendar.setCellsBackgroundColor(QColor(115, 210, 22, 50))
        self.verticalLayout.insertWidget(1, self.planning_calendar)

    def init_events(self):
        self.tableWidget_6.currentCellChanged.connect(self.when_current_cell_changed)
        self.tableWidget_6.cellDoubleClicked.connect(self.when_current_cell_double_clicked)

        self.today_button.clicked.connect(self.when_today_button_clicked)
        self.planning_calendar.selectionChanged.connect(self.when_planning_calender_date_changed)
        self.checkBox_4.clicked.connect(self.when_checkBox_4_clicked)
        self.add_to_watched_list_button.clicked.connect(self.when_add_to_watched_list_button_clicked)
        self.open_folder_button.clicked.connect(self.when_open_folder_button_clicked)
        self.show_view_history_button.clicked.connect(self.when_show_view_history_button_is_clicked)
        self.date_edit.dateChanged.connect(self.when_date_edit_date_changed)
        self.delete_button.clicked.connect(self.when_delete_button_clicked)

    def when_visible(self):
        self.update_date_on_widgets()
        self.fill_data()

    def fill_data(self):
        # Coloration des jours sur le calendrier
        self.planning_calendar.dates = [record.date for record in Planning().select().order_by(Planning.date)]

        self.fill_watched_table()
        self.fill_to_watch_table()

    def when_planning_calender_date_changed(self):
        # Change aussi la date sur le selecteur de date
        self.date_edit.setDate(self.planning_calendar.selectedDate())

        # Rempli le tableau
        self.fill_watched_table()

    def when_date_edit_date_changed(self):
        self.planning_calendar.setSelectedDate(self.date_edit.date())
        self.fill_watched_table()

    def fill_watched_table(self):
        """
        Fonction qui rempli la liste des ??pisodes vus
        :return:
        """

        # Nettoyage du nombre d'??pisodes vus pour cette date
        self.label_82.setText("")

        calendar_date = self.planning_calendar.selectedDate().toPyDate()

        planning_data_list = Planning().select().where(Planning.date == calendar_date).order_by(Planning.id)

        row_count = len(planning_data_list)
        self.label_82.setText(str(row_count))
        self.tableWidget_7.setRowCount(row_count)

        for row_index, planning_data in enumerate(planning_data_list):
            columns = ["{} - {}".format(planning_data.serie.sort_id, planning_data.season.sort_id),
                       planning_data.season.serie.name, planning_data.season.name, str(planning_data.episode)]

            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                item.setData(Qt.UserRole, planning_data.id)
                self.tableWidget_7.setItem(row_index, col_index, item)

        self.tableWidget_7.resizeColumnsToContents()
        self.tableWidget_7.horizontalHeader().setSectionResizeMode(self.tableWidget_7.columnCount() - 1, QHeaderView.ResizeToContents)


    def fill_to_watch_table(self):
        """
        Fonction qui rempli la liste des ??pisodes ?? voir
        :return:
        """

        states = [2] if self.checkBox_4.isChecked() else [1, 2]
        # https://docs.peewee-orm.com/en/latest/peewee/query_operators.html 1 or 2
        episodes_to_watch = Seasons.select()\
            .where(Seasons.state.in_(states), Seasons.watched_episodes < Seasons.episodes, Seasons.is_deleted == 0)\
            .order_by(Seasons.id)

        # Nettoyage de la liste
        row_count = len(episodes_to_watch)
        self.tableWidget_6.setRowCount(row_count)
        for col_index, row_data in enumerate(episodes_to_watch):
            ids = "{} - {}".format(row_data.serie.sort_id, row_data.sort_id)
            item = QTableWidgetItem(ids)
            item.setToolTip(item.text())
            item.setData(Qt.UserRole, row_data.id)
            self.tableWidget_6.setItem(col_index, 0, item)

            # S??rie
            item = QTableWidgetItem(row_data.serie.name)
            item.setToolTip(item.text())
            item.setData(Qt.UserRole, row_data.id)
            self.tableWidget_6.setItem(col_index, 1, item)

            # Saison
            item = QTableWidgetItem(row_data.name)
            item.setToolTip(item.text())
            self.tableWidget_6.setItem(col_index, 2, item)

            # Type
            item = QTableWidgetItem(row_data.type.name)
            item.setToolTip(item.text())
            self.tableWidget_6.setItem(col_index, 3, item)

            # Etat
            season_state = SEASONS_STATES[row_data.state]
            item = QTableWidgetItem(season_state["name"])
            item.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "../../resources/icons/", season_state["icon"])))
            item.setToolTip(item.text())
            self.tableWidget_6.setItem(col_index, 4, item)

            # Episode
            next_episode_index = int(row_data.watched_episodes) + 1
            next_episode_text = "{} / {}".format(next_episode_index, row_data.episodes)
            item = QTableWidgetItem(next_episode_text)
            item.setToolTip(item.text())
            self.tableWidget_6.setItem(col_index, 5, item)

            # Progression
            progress_bar = QProgressBar(self)
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(row_data.episodes)
            progress_bar.setValue(
                row_data.watched_episodes)  # Car si un film donc ??pisode 1 / 1 on ?? d??ja une barre ?? 100%

            # Style diff??rent si on est sous Windows
            if platform.system() == "Windows":
                progress_bar.setStyleSheet("QProgressBar::chunk ""{""background-color: #2B65EC;""}")
                progress_bar.setAlignment(Qt.AlignCenter)

            self.tableWidget_6.setCellWidget(col_index, 6, progress_bar)

        self.tableWidget_6.resizeColumnsToContents()
        self.tableWidget_6.horizontalHeader().setSectionResizeMode(self.tableWidget_6.columnCount() - 1, QHeaderView.ResizeToContents)

    def when_today_button_clicked(self):
        """Fonction qui ram??ne le calendrier ?? la date actuelle"""

        self.update_date_on_widgets()
        self.fill_watched_table()

    def update_date_on_widgets(self):
        current_date = QDate.currentDate()
        self.planning_calendar.setSelectedDate(current_date)
        self.date_edit.setDate(current_date)

    def add_to_watched_list(self):
        if self.current_season_id:
            self.add_episode_to_planning(self.current_season_id)
            self.fill_data()

    def when_add_to_watched_list_button_clicked(self):
        self.add_to_watched_list()

    def when_current_cell_double_clicked(self):
        self.add_to_watched_list()

    def add_episode_to_planning(self, season_id):
        calendar_date = self.planning_calendar.selectedDate().toPyDate()
        current_season = Seasons().get(Seasons.id == season_id)

        new_watched_episodes_value = current_season.watched_episodes + 1

        # Ajout dans le planning
        planning_entry = Planning()
        planning_entry.serie = current_season.serie.id
        planning_entry.season = current_season.id
        planning_entry.date = calendar_date
        planning_entry.episode = new_watched_episodes_value
        planning_entry.save()

        # Changement d'??tat de la saison + RAZ
        if new_watched_episodes_value == current_season.episodes:
            current_season.watched_episodes = 0
            current_season.view_count += 1
            current_season.state = 3  # Termin??
        else:
            current_season.watched_episodes = new_watched_episodes_value

        current_season.save()

    def when_checkBox_4_clicked(self):
        self.fill_to_watch_table()

    def when_current_cell_changed(self):
        self.update_current_season_id()

    def update_current_season_id(self):
        current_item = self.tableWidget_6.item(self.tableWidget_6.currentRow(), 0)
        self.current_season_id = current_item.data(Qt.UserRole) if current_item else None

        if self.current_season_id:
            # On active le bouton d'ajout aux ??pisodes vus
            self.add_to_watched_list_button.setEnabled(True)

            # On active le bouton d'historique
            self.show_view_history_button.setEnabled(True)

            # Active ou d??sactive le bouton d'ouverture du dossier de la s??rie
            season = Seasons().get(Seasons.id == self.current_season_id)
            self.open_folder_button.setEnabled(os.path.exists(season.serie.path))

        else:
            # On d??sactive les boutons qui ont une action avec une s??rie selectionn??e
            self.add_to_watched_list_button.setEnabled(False)
            self.show_view_history_button.setEnabled(False)
            self.open_folder_button.setEnabled(False)

    def when_open_folder_button_clicked(self):
        if self.current_season_id:
            season = Seasons().get(Seasons.id == self.current_season_id)
            if os.path.exists(season.serie.path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(season.serie.path))

    def when_show_view_history_button_is_clicked(self):
        if self.current_season_id:
            display_view_history_dialog(self.current_season_id)

    def when_delete_button_clicked(self):
        if self.current_season_id:
            self.show_delete_watched_episode_window()

    def show_delete_watched_episode_window(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.tr("Supression d'un ??pisode vu"))

        # TODO: Traduction
        msg_box.setText(self.tr("Vous aller supprimer le visionnagede l'??pisode {}"))
        yes_button = msg_box.addButton(self.tr("D??finir l'??pisode comme prochain ??pisode ?? voir et le supprimer"), QMessageBox.YesRole)
        no_button = msg_box.addButton(self.tr("Supprimer uniquement l'??pisode sans modifier le prochain ??pisode ?? voir"), QMessageBox.NoRole)
        msg_box.addButton(self.tr("Annuler"), QMessageBox.RejectRole)
        msg_box.exec_()

        if msg_box.clickedButton() == yes_button:
            return 0

        elif msg_box.clickedButton() == no_button:
            return 1
        else:
            return -1

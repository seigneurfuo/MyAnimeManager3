#!/bin/env python3

import platform
import os

from PyQt5.QtCore import Qt, QDate, QUrl
from PyQt5.QtGui import QColor, QDesktopServices
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QProgressBar, QMessageBox
from PyQt5.uic import loadUi

from ui.custom_calendar import CustomCalendar
from database import Planning, Seasons
from common import show_watch_history_dialog


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
        self.open_folder_button.clicked.connect(self.when_open_folder_button_is_clicked)
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
        Fonction qui rempli la liste des épisodes vus
        :return:
        """

        # Nettoyage du nombre d'épisodes vus pour cette date
        self.label_82.setText("")

        calendar_date = self.planning_calendar.selectedDate().toPyDate()

        planning_data_list = Planning().select().where(Planning.date == calendar_date).order_by(Planning.id)

        row_count = len(planning_data_list)
        self.label_82.setText(str(row_count))
        self.tableWidget_7.setRowCount(row_count)
        for col_index, row_data in enumerate(planning_data_list):
            col_data = QTableWidgetItem(row_data.season.serie.name)
            col_data.setToolTip(col_data.text())
            col_data.setData(Qt.UserRole, row_data.id)
            self.tableWidget_7.setItem(col_index, 0, col_data)

            col_data = QTableWidgetItem(row_data.season.name)
            col_data.setToolTip(col_data.text())
            self.tableWidget_7.setItem(col_index, 1, col_data)

            col_data = QTableWidgetItem(str(row_data.episode))
            col_data.setToolTip(col_data.text())
            self.tableWidget_7.setItem(col_index, 2, col_data)

        self.tableWidget_7.resizeColumnsToContents()

    def fill_to_watch_table(self):
        """
        Fonction qui rempli la liste des épisodes à voir
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
            # Série
            col_data = QTableWidgetItem(row_data.serie.name)
            col_data.setToolTip(col_data.text())
            col_data.setData(Qt.UserRole, row_data.id)
            self.tableWidget_6.setItem(col_index, 0, col_data)

            # Saison
            col_data = QTableWidgetItem(row_data.name)
            col_data.setToolTip(col_data.text())
            self.tableWidget_6.setItem(col_index, 1, col_data)

            # Etat FIXME: C'est pas très propre le self.parent.parent.season_states
            col_data = QTableWidgetItem(self.parent.parent.season_states[row_data.state])
            col_data.setToolTip(col_data.text())
            self.tableWidget_6.setItem(col_index, 2, col_data)

            # Episode
            next_episode_index = int(row_data.watched_episodes) + 1
            next_episode_text = "{} / {}".format(next_episode_index, row_data.episodes)
            col_data = QTableWidgetItem(next_episode_text)
            col_data.setToolTip(col_data.text())
            self.tableWidget_6.setItem(col_index, 3, col_data)

            # Progression
            progress_bar = QProgressBar(self)
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(row_data.episodes)
            progress_bar.setValue(
                row_data.watched_episodes)  # Car si un film donc épisode 1 / 1 on à déja une barre à 100%

            # Style différent si on est sous Windows
            if platform.system() == "Windows":
                progress_bar.setStyleSheet("QProgressBar::chunk ""{""background-color: #2B65EC;""}")
                progress_bar.setAlignment(Qt.AlignCenter)

            self.tableWidget_6.setCellWidget(col_index, 4, progress_bar)

        self.tableWidget_6.resizeColumnsToContents()

    def when_today_button_clicked(self):
        """Fonction qui ramène le calendrier à la date actuelle"""

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

        # Changement d'état de la saison + RAZ
        if new_watched_episodes_value == current_season.episodes:
            current_season.watched_episodes = 0
            current_season.state = 3  # Terminé
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
            # On active le bouton d'ajout aux épisodes vus
            self.add_to_watched_list_button.setEnabled(True)

            # On active le bouton d'historique
            self.show_view_history_button.setEnabled(True)

            # Active ou désactive le bouton d'ouverture du dossier de la série
            season = Seasons().get(Seasons.id == self.current_season_id)
            self.open_folder_button.setEnabled(os.path.exists(season.serie.path))

        else:
            # On désactive les boutons qui ont une action avec une série selectionnée
            self.add_to_watched_list_button.setEnabled(False)
            self.show_view_history_button.setEnabled(False)
            self.open_folder_button.setEnabled(False)

    def when_open_folder_button_is_clicked(self):
        if self.current_season_id:
            season = Seasons().get(Seasons.id == self.current_season_id)
            path = season.serie.path
            if os.path.exists(path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def when_show_view_history_button_is_clicked(self):
        if self.current_season_id:
            show_watch_history_dialog(self.current_season_id)

    def when_delete_button_clicked(self):
        if self.current_season_id:
            self.show_delete_watched_episode_window()

    def show_delete_watched_episode_window(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.tr("Supression d'un épisode vu"))

        # TODO: Traduction
        msg_box.setText(self.tr("Vous aller supprimer le visionnagede l'épisode {}"))
        yes_button = msg_box.addButton(self.tr("Définir l'épisode comme prochain épisode à voir et le supprimer"), QMessageBox.YesRole)
        no_button = msg_box.addButton(self.tr("Supprimer uniquement l'épisode sans modifier le prochain épisode à voir"), QMessageBox.NoRole)
        msg_box.addButton(self.tr("Annuler"), QMessageBox.RejectRole)
        msg_box.exec_()

        if msg_box.clickedButton() == yes_button:
            return 0

        elif msg_box.clickedButton() == no_button:
            return 1
        else:
            return -1

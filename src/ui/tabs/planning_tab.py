#!/bin/env python3

import platform
import os

from PyQt5.QtCore import Qt, QDate, QUrl
from PyQt5.QtGui import QColor, QDesktopServices, QIcon
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QProgressBar, QMessageBox, QHeaderView, QCalendarWidget
from PyQt5.uic import loadUi

from ui.dialogs.edit_date import EditDateDialog
from ui.widgets.custom_calendar import CustomCalendar
from database import Planning, Seasons, Friends, FriendsPlanning
from core import SEASONS_STATES
from common import display_view_history_dialog


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
        self.planning_calendar.setGridVisible(True)
        self.planning_calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
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
        self.show_view_history_button.clicked.connect(self.when_show_view_history_button_clicked)
        self.date_edit.dateChanged.connect(self.when_date_edit_date_changed)
        self.delete_button.clicked.connect(self.when_delete_button_clicked)
        self.change_date_button.clicked.connect(self.when_change_date_button_clicked)

    def when_visible(self):
        self.update_date_on_widgets()
        self.fill_data()

    def fill_data(self):
        self.fill_calendar_dates()
        self.fill_watched_table()
        self.fill_to_watch_table()

        self.update_current_season_id()

    def when_planning_calender_date_changed(self):
        # Change aussi la date sur le selecteur de date
        self.date_edit.setDate(self.planning_calendar.selectedDate())

        # Rempli le tableau
        self.fill_watched_table()

    def when_date_edit_date_changed(self):
        self.planning_calendar.setSelectedDate(self.date_edit.date())
        self.fill_watched_table()

    def fill_calendar_dates(self):
        # Coloration des jours sur le calendrier
        self.planning_calendar.dates = [record.date for record in Planning().select().group_by(Planning.date).order_by(Planning.date)]

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

        for row_index, planning_data in enumerate(planning_data_list):
            friends = [friend_planning.friend.name for friend_planning in planning_data.friends]
            columns = ["{} - {}".format(planning_data.serie.sort_id, planning_data.season.sort_id),
                       planning_data.season.serie.name, planning_data.season.name, str(planning_data.episode),
                       ", ".join(friends)]

            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                item.setData(Qt.UserRole, planning_data.id)
                self.tableWidget_7.setItem(row_index, col_index, item)

        self.tableWidget_7.resizeColumnsToContents()
        self.tableWidget_7.horizontalHeader().setSectionResizeMode(self.tableWidget_7.columnCount() - 1,
                                                                   QHeaderView.ResizeToContents)

    def fill_to_watch_table(self):
        """
        Fonction qui rempli la liste des épisodes à voir
        :return:
        """

        states = [2] if self.checkBox_4.isChecked() else [1, 2]
        # https://docs.peewee-orm.com/en/latest/peewee/query_operators.html 1 or 2
        episodes_to_watch = Seasons.select() \
            .where(Seasons.state.in_(states), Seasons.watched_episodes < Seasons.episodes, Seasons.is_deleted == 0) \
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

            # Série
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

            # En diffusion
            airing = self.tr("Oui") if row_data.airing else self.tr("Non")
            item = QTableWidgetItem(airing)

            if row_data.airing:
                item.setForeground(QColor("#039d09"))

            item.setToolTip(item.text())
            self.tableWidget_6.setItem(col_index, 5, item)

            # Episode
            next_episode_index = int(row_data.watched_episodes) + 1
            next_episode_text = "{} / {}".format(next_episode_index, row_data.episodes)
            item = QTableWidgetItem(next_episode_text)

            item.setToolTip(item.text())
            self.tableWidget_6.setItem(col_index, 6, item)

            # Progression
            progress_bar = QProgressBar(self)
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(row_data.episodes)
            progress_bar.setValue(row_data.watched_episodes)  # Car si un film donc épisode 1 / 1 on à déja une barre à 100%

            # Style différent si on est sous Windows
            if platform.system() == "Windows":
                progress_bar.setStyleSheet("QProgressBar::chunk ""{""background-color: #2B65EC;""}")
                progress_bar.setAlignment(Qt.AlignCenter)

            self.tableWidget_6.setCellWidget(col_index, 7, progress_bar)

        self.tableWidget_6.resizeColumnsToContents()
        self.tableWidget_6.horizontalHeader().setSectionResizeMode(self.tableWidget_6.columnCount() - 1,
                                                                   QHeaderView.ResizeToContents)

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
            current_season.view_count += 1
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

    # TODO: Update watched table buttons

    def when_open_folder_button_clicked(self):
        if self.current_season_id:
            season = Seasons().get(Seasons.id == self.current_season_id)
            if os.path.exists(season.serie.path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(season.serie.path))

    def when_show_view_history_button_clicked(self):
        if self.current_season_id:
            display_view_history_dialog(self.current_season_id)

    def when_delete_button_clicked(self):
        current_item = self.tableWidget_7.item(self.tableWidget_7.currentRow(), 0)
        planning_id = current_item.data(Qt.UserRole) if current_item else None

        if planning_id:
            planning_data = Planning.get(planning_id)
            planning_data.delete_instance()

            self.fill_calendar_dates()
            self.fill_watched_table()

            #self.show_delete_watched_episode_window(planning_data)

    def when_change_date_button_clicked(self):
        current_item = self.tableWidget_7.item(self.tableWidget_7.currentRow(), 0)
        planning_id = current_item.data(Qt.UserRole) if current_item else None

        if planning_id:
            planning_data = Planning.get(planning_id)
            full_friends_list = Friends.select()
            dialog = EditDateDialog(planning_data, full_friends_list)

            if dialog.exec():

                # Supression des amis
                for friend_id in dialog.friends_to_remove:
                    friend_planning = FriendsPlanning.get(FriendsPlanning.planning == planning_id, FriendsPlanning.friend == friend_id)
                    friend_planning.delete_instance()

                # Ajout des amis
                for friend_id in dialog.friends_to_add:
                    friend_planning_data = FriendsPlanning()
                    friend_planning_data.friend = friend_id
                    friend_planning_data.planning = planning_id
                    friend_planning_data.save()

                self.fill_calendar_dates()
                self.fill_watched_table()

    def show_delete_watched_episode_window(self, planning_data):
        episode_num = planning_data.episode
        previous_episode_num = episode_num - 1
        next_episode_num = episode_num + 1

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.tr("Supression d'un épisode vu"))

        # TODO: Traduction
        msg_box.setText(self.tr("Vous aller supprimer le visionnage de l'épisode: {}.".format(episode_num)))

        remove_and_decrement_episode = msg_box.addButton(self.tr(
            "Supprimer l'épisode {0}. Prochain épisode suggéré: {0}".format(episode_num)), QMessageBox.YesRole)

        remove_and_keep_episode_num = msg_box.addButton(self.tr(
            "Supprimer l'épisode {0}. Prochain épisode suggéré: {1}".format(episode_num, next_episode_num)),
                                       QMessageBox.NoRole)

        msg_box.addButton(self.tr("Annuler"), QMessageBox.RejectRole)
        msg_box.exec()

        if msg_box.clickedButton() == remove_and_decrement_episode:

            # FIXME: Marche pas
            season = Seasons.get(planning_data.season)
            season.watched_episodes = previous_episode_num
            season.save()

            Planning.get(planning_data.id).delete_instance()
            self.fill_data()

        elif msg_box.clickedButton() == remove_and_keep_episode_num:
            Planning.get(planning_data.id).delete_instance()
            self.fill_data()

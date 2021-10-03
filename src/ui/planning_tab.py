#!/bin/env python3
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.uic import loadUi

import os

from ui.custom_calendar import CustomCalendar
from database import Planning

class PlanningTab(QWidget):
    def __init__(self, parent, app_dir):
        super().__init__(parent)

        self.parent = parent
        self.app_dir = app_dir

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(self.app_dir, 'ui/planning_tab.ui'), self)

        self.planning_calendar = CustomCalendar()
        self.planning_calendar.setCellsBackgroundColor(QColor(115, 210, 22, 50))
        self.horizontalLayout_42.insertWidget(0, self.planning_calendar, )

    def init_events(self):
        self.today_button.clicked.connect(self.when_today_button_clicked)
        self.planning_calendar.clicked.connect(self.fill_watched_table)

    def when_visible(self):
        # Coloration des jours sur le calendrier
        self.planning_calendar.dates = [record.date for record in Planning().select().order_by(Planning.date)]

        self.fill_watched_table()

    def fill_watched_table(self):
        """
        Fonction qui rempli la liste des épisodes vus
        :return:
        """

        # Nettoyage de la liste
        self.tableWidget_7.setRowCount(0)

        # Nettoyage du nombre d'épisodes vus pour cette date
        self.label_82.setText("")

        calendar_date = self.planning_calendar.selectedDate().toPyDate()

        planning_data_list = Planning().select().where(Planning.date == calendar_date).order_by(Planning.id)
        row_count = len(planning_data_list)
        self.label_82.setText(str(row_count))
        self.tableWidget_7.setRowCount(row_count)

        for col_index, planning_data in enumerate(planning_data_list):
            column0 = QTableWidgetItem(planning_data.season.serie.name)
            self.tableWidget_7.setItem(col_index, 0, column0)

            column1 = QTableWidgetItem(planning_data.season.name)
            self.tableWidget_7.setItem(col_index, 1, column1)

            column2 = QTableWidgetItem(str(planning_data.episode))
            self.tableWidget_7.setItem(col_index, 2, column2)

    def fill_to_watch_table(self):
        """
        Fonction qui rempli la liste des épisodes à voir
        :return:
        """

        # Nettoyage de la liste
        self.tableWidget_6.setRowCount(0)

        # Nettoyage du nombre d'épisodes vus pour cette date

        calendar_date = self.planning_calendar.selectedDate().toPyDate()

        planning_data_list = Planning().select().where(Planning.date == calendar_date).order_by(Planning.id)
        row_count = len(planning_data_list)
        self.label_82.setText(str(row_count))
        self.tableWidget_7.setRowCount(row_count)

        for col_index, planning_data in enumerate(planning_data_list):
            column0 = QTableWidgetItem(planning_data.season.serie.name)
            self.tableWidget_7.setItem(col_index, 0, column0)

            column1 = QTableWidgetItem(planning_data.season.name)
            self.tableWidget_7.setItem(col_index, 1, column1)

            column2 = QTableWidgetItem(str(planning_data.episode))
            self.tableWidget_7.setItem(col_index, 2, column2)



    def when_today_button_clicked(self):
        """Fonction qui ramène le calendrier à la date actuelle"""

        self.planning_calendar.setSelectedDate(QDate.currentDate())
        self.fill_watched_table()



"""
id: entrée unique dans le planning
date: 
serie_id: 
season_id: 
episode_id: 
"""

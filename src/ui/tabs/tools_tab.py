#!/bin/env python3
import random

from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTime

import os

from database import Seasons
from utils import get_duration_list


class ToolsTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "tools_tab.ui"), self)

    def init_events(self):
        self.go_button.clicked.connect(self.when_duration_calculation_button_click)
        self.get_current_time_button.clicked.connect(self.when_get_current_time_button_click)

        # Si n'importe quelle valeur de la spinbox est changée, alors on met à jour en temps réel
        # self.timeEdit.timeChanged.connect(self.when_spinboxes_values_changed)
        # self.spinBox.valueChanged.connect(self.when_spinboxes_values_changed)
        # self.spinBox_2.valueChanged.connect(self.when_spinboxes_values_changed)
        # self.spinBox_3.valueChanged.connect(self.when_spinboxes_values_changed)
        # self.spinBox_4.valueChanged.connect(self.when_spinboxes_values_changed)

        self.select_random_season_button.clicked.connect(self.when_select_random_season_button_clicked)

    def when_visible(self):
        self.set_current_time()

    def duration_calculation(self):
        episodes_count = self.episodes_count_spinbox.value()
        episodes_duration = self.episodes_duration_spinbox.value()

        pause_every = self.pauses_every_spinbox.value()
        pause_duration = self.pauses_duration_spinbox.value()

        start_time_string = str(self.timeEdit.dateTime().toString("hh:mm"))

        rows = get_duration_list(episodes_count, episodes_duration, pause_every, pause_duration, start_time_string)

        row_count = len(rows)
        self.tableWidget_2.setRowCount(row_count)

        # TODO: Tablewidget Type: Episode / Pause, Heure début, Heure fin
        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setToolTip(item.text())
                self.tableWidget_2.setItem(row_index, col_index, item)

        self.tableWidget_2.clearSelection()
        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
                                                                 QHeaderView.ResizeToContents)

    # def when_spinboxes_values_changed(self):
    #     self.duration_calculation()

    def when_duration_calculation_button_click(self):
        self.duration_calculation()

    def set_current_time(self):
        self.timeEdit.setTime(QTime.currentTime())

    def when_get_current_time_button_click(self):
        self.set_current_time()

    def when_select_random_season_button_clicked(self):
        states = [0, 1, 2] if self.checkBox.isChecked() else [0, 1]
        seasons = Seasons.select().where(Seasons.state.in_(states), Seasons.is_deleted == 0).order_by(Seasons.id)

        MAX_ELEMENTS = 10
        random_seasons_indexes = [random.randint(0, len(seasons) - 1) for x in range(MAX_ELEMENTS)]

        self.tableWidget.setRowCount(MAX_ELEMENTS)

        for row_index, random_season_index in enumerate(random_seasons_indexes):
            random_season = seasons[random_season_index]

            columns = [random_season.serie.name, random_season.name, random_season.type.name]
            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                #item.setToolTip(item.text())
                self.tableWidget.setItem(row_index, col_index, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1, QHeaderView.ResizeToContents)
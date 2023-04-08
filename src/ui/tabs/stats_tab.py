#!/bin/env python3
import random

from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTime

import os

import peewee
from database import Series, Seasons

class StatsTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.request = []

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "stats.ui"), self)

        requests_list = [self.tr("Nombre de saisons par année"), self.tr("Saisons les plus revisionnées"),
                         self.tr("Saison avec le plus d'épisodes")]
        for index, name in enumerate(requests_list):
            self.comboBox.addItem(name, userData=index)

    def init_events(self):
        self.comboBox.currentIndexChanged.connect(self.when_stats_list_current_index_changed)

    def when_visible(self):
        self.fill_stats_table_data()

    def when_stats_list_current_index_changed(self):
        self.fill_stats_table_data()

    def fill_stats_table_data(self):
        headers, request = self.execute_request()

        row_count = len(request)
        self.label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.stats_table.setRowCount(row_count)
        self.stats_table.setColumnCount(len(headers))

       # Headers
        self.stats_table.setHorizontalHeaderLabels(headers)

        for row_index, row in enumerate(request):
            for col_index, value in enumerate(row.values()):
                item = QTableWidgetItem(str(value))
                item.setToolTip(item.text())
                self.stats_table.setItem(row_index, col_index, item)

        self.stats_table.resizeColumnsToContents()
        # self.stats_table.horizontalHeader().setSectionResizeMode(self.stats_table.columnCount() - 1,
        #                                                          QHeaderView.ResizeToContents)

    def execute_request(self):
        request_index = self.comboBox.currentData()

        # Nombre de saisons par année
        if request_index == 0:
            headers = ["Année", "Nombre"]
            request = Seasons.select(Seasons.year, peewee.fn.COUNT(Seasons.id)).where(Seasons.is_deleted == 0)\
                .group_by(Seasons.year).order_by(Seasons.year).dicts()

        # Saisons les plus revisionnées
        if request_index == 1:
            headers = ["Série", "Saison", "Nombre"]
            request = Seasons.select(Series.name.alias("serie_name"), Seasons.name, Seasons.view_count).join(Series)\
                .where(Seasons.is_deleted == 0)\
                .order_by(Seasons.view_count.desc()).dicts()

        if request_index == 2:
            headers = ["Série", "Saison", "Nombre"]
            request = Seasons.select(Series.name.alias("serie_name"), Seasons.name, Seasons.episodes).join(Series)\
                .where(Seasons.is_deleted == 0)\
                .order_by(Seasons.episodes.desc()).dicts()

        return headers, request
#!/bin/env python3

import os
from datetime import datetime

import utils

from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.uic import loadUi

from database import database, Series, Seasons

class List2(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "list2_tab.ui"), self)

    def init_events(self):
        self.pushButton.clicked.connect(self.when_export_button_clicked)

    def when_visible(self):
        self.fill_data()

    def fill_data(self):
        today_date_object = datetime.now()

        data = Seasons().select().where(Seasons.is_deleted == 0).order_by(Seasons.sort_id)
        row_count = len(data)

        self.label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.tableWidget.setRowCount(row_count)
        for row_index, season in enumerate(data):
            ids = "{} - {}".format(season.serie.sort_id, season.sort_id)
            year = str(season.year) if season.year and str(season.year) != "None" else ""

            # Calcul de l'age
            if year:
                # Différence entre deux dates
                release_year_datetime_object = datetime.strptime(str(season.year), "%Y")
                age_diff = today_date_object.year - release_year_datetime_object.year
                age = "{} ans".format(age_diff)
            else:
                age = ""

            state = self.parent.parent.season_states[season.state]

            columns = [ids, season.serie.name, season.type.name, season.name, str(season.episodes), year,
                       age, state, str(season.view_count)]

            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                item.setData(Qt.UserRole, season.id)
                self.tableWidget.setItem(row_index, col_index, item)

    def when_export_button_clicked(self):
        utils.export_qtablewidget(self.tableWidget)
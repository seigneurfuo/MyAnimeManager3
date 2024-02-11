#!/usr/bin/python3

from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi

import os

import peewee
from database import Series, Seasons, Planning

import utils


class StatsTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "stats_tab.ui"), self)

        # Remplissage la liste des extractions
        queries_list = [self.tr("Nombre de saisons par année de sortie"), self.tr("Saisons les plus revisionnées"),
                        self.tr("Saisons avec le plus d'épisodes"), self.tr("Séries avec le plus d'épisodes"),
                        self.tr("Nombre d'épisodes vus par année"), self.tr("Jounal de visionnage détaillé"),
                        self.tr("Liste des séries pour lequelles il reste des saisons à voir")]

        for index, name in enumerate(queries_list):
            self.comboBox.addItem(name, userData=index)

    def init_events(self):
        self.comboBox.currentIndexChanged.connect(self.when_stats_list_current_index_changed)
        self.export_button.clicked.connect(self.when_export_button_clicked)

    def when_visible(self):
        self.fill_data()

    def when_stats_list_current_index_changed(self):
        self.fill_data()

    def fill_data(self):
        headers, data = self.execute_query()
        self.fill_stats_table(headers, data)

    def fill_stats_table(self, headers, data):
        row_count = len(data)
        self.label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.stats_table.setRowCount(row_count)
        self.stats_table.setColumnCount(len(headers))

       # Headers
        self.stats_table.setHorizontalHeaderLabels(headers)

        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row.values()):
                item = QTableWidgetItem(str(value))
                item.setToolTip(item.text())
                self.stats_table.setItem(row_index, col_index, item)

        self.stats_table.resizeColumnsToContents()
        # self.stats_table.horizontalHeader().setSectionResizeMode(self.stats_table.columnCount() - 1,
        #                                                          QHeaderView.ResizeMode.ResizeToContents)


    def when_export_button_clicked(self):
        query_name = self.comboBox.currentText()

        filepath = utils.export_qtablewidget(self.stats_table, self.parent.parent.profile.path, query_name)
        # TODO: Bouton pour ouvrir le dossier ?
        QMessageBox.information(self, self.tr("Export terminé"),
                                self.tr("Le fichier a été généré ici:") + "\n    " + filepath,
                                QMessageBox.StandardButton.Ok)

    def execute_query(self):
        query_index = self.comboBox.currentData()

        # Nombre de saisons par année
        if query_index == 0:
            headers = ["Année", "Nombre"]
            query = Seasons.select(Seasons.year, peewee.fn.COUNT(Seasons.id)).where(Seasons.is_deleted == 0)\
                .group_by(Seasons.year).order_by(Seasons.year).dicts()

        # Saisons les plus revisionnées
        elif query_index == 1:
            headers = ["Série", "Saison", "Nombre"]
            query = Seasons.select(Series.name.alias("serie_name"), Seasons.name, Seasons.view_count).join(Series)\
                .where(Seasons.is_deleted == 0).order_by(Seasons.view_count.desc()).dicts()

        # Saison avec le plus d'épisodes
        elif query_index == 2:
            headers = ["Série", "Saison", "Nombre"]
            query = Seasons.select(Series.name.alias("serie_name"), Seasons.name, Seasons.episodes).join(Series)\
                .where(Seasons.is_deleted == 0).order_by(Seasons.episodes.desc()).dicts()

        # Séries avec le plus d'épisodes
        elif query_index == 3:
            headers = ["Série", "Nombre saisons", "Nombre épisodes"]
            query = Seasons.select(Series.name.alias("serie_name"), peewee.fn.COUNT(Seasons.id),
                                     peewee.fn.SUM(Seasons.episodes)).join(Series)\
                .where(Seasons.is_deleted == 0).group_by(Series.id)\
                .order_by(peewee.fn.SUM(Seasons.episodes).desc()).dicts()

        # Nombre d'épisodes vus par année
        elif query_index == 4:
            headers = ["Année", "Nombre"]
            query = Planning.select(Planning.date.year, peewee.fn.COUNT(Planning.id))\
                .group_by(Planning.date.year).order_by(Planning.date.year).dicts()

        elif query_index == 5:
            headers = ["Date", "Ids", "Série", "Saison", "Episode"]
            query = Planning.select(Planning.date, Series.sort_id.concat(" - ").concat(Seasons.sort_id),
                                    Series.name.alias("serie_name"), Seasons.name, Planning.episode) \
                .join(Series).switch(Planning).join(Seasons).order_by(Planning.date.desc(), Planning.id.desc()).dicts()

        elif query_index == 6:
            headers = ["Ids", "Série", "Saison", "Episodes vus"]
            query = Seasons.select(Series.sort_id.concat(" - ").concat(Seasons.sort_id), Series.name.alias("serie_name"),
                                   Seasons.name, Seasons.watched_episodes.concat("/").concat(Seasons.episodes))\
                .join(Series).where(Seasons.is_deleted == 0).where(Seasons.state.in_([0, 1, 2, 5]))\
                .order_by(Series.name.asc(), Seasons.name.asc()).dicts()

        return headers, query
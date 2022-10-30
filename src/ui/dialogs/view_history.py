import os

from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi

from database import Planning, Friends, Seasons, FriendsPlanning, Series


class ViewHistory(QDialog):
    def __init__(self, season, serie_episodes, season_episodes):
        super(ViewHistory, self).__init__()

        self.season = season
        self.serie_episodes = serie_episodes
        self.season_episodes = season_episodes

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "view_history.ui"), self)

        self.tabWidget.setCurrentIndex(0)

        self.setWindowTitle(self.tr("Historique de visionnage") + ": " + self.season.serie.name)

        self.fill_data()

    def init_events(self):
        pass

    def fill_data(self):
        self.fill_season_history()
        self.fill_serie_history()

    def fill_serie_history(self):
        row_count = len(self.serie_episodes)
        self.serie_label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.serie_table.setRowCount(row_count)

        for row_index, row in enumerate(self.serie_episodes):
            # Pas très propre mais fonctionnel
            friends = [friend.name for friend in
                       Friends.select(Friends.name).where(Seasons.id == row.season.id).where(Planning.date == row.date) \
                           .join(FriendsPlanning).join(Planning).join(Seasons).group_by(Friends.name)]

            columns = [row.date.strftime("%d/%m/%Y"), row.season.name, self.season.type.name, row.episodes,
                       ", ".join(friends)]

            # FIXME: Ne fonctionne pas quand il y à plusieurs épisodes
            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                self.serie_table.setItem(row_index, col_index, item)

        self.serie_table.resizeColumnsToContents()
        self.serie_table.horizontalHeader().setSectionResizeMode(self.serie_table.columnCount() - 1,
                                                                 QHeaderView.ResizeToContents)

    def fill_season_history(self):
        row_count = len(self.season_episodes)
        self.season_label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.season_table.setRowCount(row_count)

        for row_index, row in enumerate(self.season_episodes):
            friends = [friend.name for friend in
                       Friends.select(Friends.name).where(Seasons.id == row.season.id).where(Planning.date == row.date) \
                           .join(FriendsPlanning).join(Planning).join(Seasons).group_by(Friends.name)]

            columns = [row.date.strftime("%d/%m/%Y"), row.season.name, self.season.type.name, row.episodes, ", ".join(friends)]

            # FIXME: Ne fonctionne pas quand il y à plusieurs épisodes
            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                self.season_table.setItem(row_index, col_index, item)

        self.season_table.resizeColumnsToContents()
        self.season_table.horizontalHeader().setSectionResizeMode(self.season_table.columnCount() - 1,
                                                                 QHeaderView.ResizeToContents)

    def reject(self):
        super(ViewHistory, self).reject()

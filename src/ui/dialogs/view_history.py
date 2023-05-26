import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi

from database import Planning, Friends, Seasons, FriendsPlanning


class ViewHistoryDialog(QDialog):
    def __init__(self, parent, season, serie_episodes, season_episodes):
        super().__init__()

        self.parent = parent
        self.season = season
        self.serie_episodes = serie_episodes
        self.season_episodes = season_episodes

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "view_history.ui"), self)

        self.setWindowTitle(self.tr("Historique de visionnage") + ": " + self.season.serie.name)
        self.tabWidget.setCurrentIndex(0)

        self.fill_data()

    def init_events(self):
        self.pushButton.clicked.connect(self.when_go_to_planning_date)

    def fill_data(self):
        self.fill_seasons_history()
        self.fill_series_history()

    def fill_series_history(self):
        row_count = len(self.serie_episodes)
        self.serie_label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.serie_table.setRowCount(row_count)

        for row_index, row in enumerate(self.serie_episodes):
            # Pas très propre mais fonctionnel
            friends = [friend.name for friend in
                       Friends.select(Friends.name).where(Seasons.id == row.season.id).where(Planning.date == row.date) \
                           .join(FriendsPlanning).join(Planning).join(Seasons).group_by(Friends.name)]

            columns = [row.date.strftime("%d/%m/%Y"), "{} - {}".format(row.season.sort_id, row.season.name), self.season.type.name, row.episodes,
                       ", ".join(friends)]

            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                item.setData(Qt.UserRole, row.date) # On ajoute la date en paramètre afin de pouvoir la récupérer sur la ligne
                self.serie_table.setItem(row_index, col_index, item)

        self.serie_table.resizeColumnsToContents()
        self.serie_table.horizontalHeader().setSectionResizeMode(self.serie_table.columnCount() - 1,
                                                                 QHeaderView.ResizeToContents)

    def fill_seasons_history(self):
        row_count = len(self.season_episodes)
        self.season_label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.season_table.setRowCount(row_count)

        for row_index, row in enumerate(self.season_episodes):
            friends = [friend.name for friend in
                       Friends.select(Friends.name).where(Seasons.id == row.season.id).where(Planning.date == row.date) \
                           .join(FriendsPlanning).join(Planning).join(Seasons).group_by(Friends.name)]

            columns = [row.date.strftime("%d/%m/%Y"), "{} - {}".format(row.season.sort_id, row.season.name), self.season.type.name, row.episodes,
                       ", ".join(friends)]

            # FIXME: Ne fonctionne pas quand il y à plusieurs épisodes
            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                item.setData(Qt.UserRole, row.date) # On ajoute la date en paramètre afin de pouvoir la récupérer sur la ligne
                self.season_table.setItem(row_index, col_index, item)

        self.season_table.resizeColumnsToContents()
        self.season_table.horizontalHeader().setSectionResizeMode(self.season_table.columnCount() - 1,
                                                                  QHeaderView.ResizeToContents)

    def when_go_to_planning_date(self):
        # Série et saison
        # TODO:

        table = self.season_table if self.tabWidget.currentIndex() == 0 else self.serie_table
        current_item = table.item(table.currentRow(), 0)
        print(current_item)
        if current_item:
            selected_date = current_item.data(Qt.UserRole)

            self.parent.parent.tabWidget.setCurrentIndex(0) # Onglet "Planning"
            self.parent.parent.planning_tab.set_planning_date(selected_date)
            self.close()

    def reject(self):
        super().reject()

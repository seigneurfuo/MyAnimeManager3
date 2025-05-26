import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt6.uic import loadUi

from database import Planning, Friends, Seasons, FriendsPlanning


class ViewHistoryDialog(QDialog):
    def __init__(self, parent, season, serie_episodes, season_episodes) -> None:
        super().__init__(parent=parent)

        self.parent = parent
        self.season = season
        self.serie_episodes = serie_episodes
        self.season_episodes = season_episodes

        self.init_ui()
        self.init_events()

    def init_ui(self) -> None:
        loadUi(os.path.join(os.path.dirname(__file__), "view_history.ui"), self)

        self.setWindowTitle(self.tr("Historique de visionnage") + ": " + self.season.serie.name)
        self.tabWidget.setCurrentIndex(0)

        self.fill_data()

    def init_events(self) -> None:
        self.pushButton.clicked.connect(self.when_go_to_planning_date)
        self.season_table.currentCellChanged.connect(self.when_table_current_cell_changed)
        self.serie_table.currentCellChanged.connect(self.when_table_current_cell_changed)

    def when_table_current_cell_changed(self) -> None:
        self.pushButton.setEnabled(True)

    def fill_data(self) -> None:
        self.fill_seasons_history()
        self.fill_series_history()

    def fill_series_history(self) -> None:
        self.serie_table.clearContents()

        # On masque la colonne si les amis sont désactivés
        if not self.parent.parent.parent.settings["friends_enabled"]:
            self.serie_table.hideColumn(self.serie_table.columnCount() - 1)

        row_count = len(self.serie_episodes)
        self.serie_label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.serie_table.setRowCount(row_count)

        for row_index, row in enumerate(self.serie_episodes):
            columns = [row.date.strftime("%d/%m/%Y"), str(row.season.sort_id), row.season.name, row.season.type.name,
                       row.episodes]

            # Si on à activé la gestion des amis:
            if self.parent.parent.parent.settings["friends_enabled"]:
                friends = [friend.name for friend in
                           Friends.select(Friends.name).where(Seasons.id == row.season.id).where(
                               Planning.date == row.date) \
                               .join(FriendsPlanning).join(Planning).join(Seasons).group_by(Friends.name)]

                columns.append(", ".join(friends))

            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                item.setData(Qt.ItemDataRole.UserRole,
                             row.date)  # On ajoute la date en paramètre afin de pouvoir la récupérer sur la ligne
                self.serie_table.setItem(row_index, col_index, item)

        self.serie_table.resizeColumnsToContents()
        self.serie_table.horizontalHeader().setSectionResizeMode(self.serie_table.columnCount() - 1,
                                                                 QHeaderView.ResizeMode.ResizeToContents)

    def fill_seasons_history(self) -> None:
        self.season_table.clearContents()

        row_count = len(self.season_episodes)
        self.season_label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.season_table.setRowCount(row_count)

        for row_index, row in enumerate(self.season_episodes):
            columns = [row.date.strftime("%d/%m/%Y"), str(row.season.sort_id), row.season.name, row.season.type.name,
                       row.episodes]

            # Si on à activé la gestion des amis:
            if self.parent.parent.parent.settings["friends_enabled"]:
                friends = [friend.name for friend in
                           Friends.select(Friends.name).where(Seasons.id == row.season.id).where(
                               Planning.date == row.date) \
                               .join(FriendsPlanning).join(Planning).join(Seasons).group_by(Friends.name)]

                columns.append(", ".join(friends))

            # Sinon on masque la colonne:
            else:
                self.season_table.horizontalHeader().hideSection(len(columns))

            # FIXME: Ne fonctionne pas quand il y à plusieurs épisodes
            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                item.setData(Qt.ItemDataRole.UserRole, row.date)  # On ajoute la date en paramètre afin de pouvoir la récupérer sur la ligne
                self.season_table.setItem(row_index, col_index, item)

        self.season_table.resizeColumnsToContents()
        self.season_table.horizontalHeader().setSectionResizeMode(self.season_table.columnCount() - 1,
                                                                  QHeaderView.ResizeMode.ResizeToContents)

    def when_go_to_planning_date(self) -> None:
        # Série et saison
        # TODO:

        table = self.season_table if self.tabWidget.currentIndex() == 0 else self.serie_table
        current_item = table.item(table.currentRow(), 0)

        if current_item:
            selected_date = current_item.data(Qt.ItemDataRole.UserRole)

            self.parent.parent.tabWidget.setCurrentIndex(0)  # Onglet "Planning"
            self.parent.parent.planning_tab.set_planning_date(selected_date)
            self.close()

    def reject(self) -> None:
        super().reject()

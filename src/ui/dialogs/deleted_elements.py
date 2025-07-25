import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QCheckBox
from PyQt6.uic import loadUi

from database import Seasons, Series


class DeletedElementsDialog(QDialog):
    def __init__(self, parent, deleted_series, deleted_seasons) -> None:
        super().__init__(parent=parent)

        self.deleted_seasons = deleted_seasons
        self.deleted_series = deleted_series

        self.series_to_restore = []
        self.seasons_to_restore = []

        self.init_ui()
        self.init_events()

    def init_ui(self) -> None:
        loadUi(os.path.join(os.path.dirname(__file__), "deleted_elements.ui"), self)

        self.setWindowTitle(self.tr("Eléments supprimés"))
        self.tabWidget.setCurrentIndex(0)

        self.fill_data()

    def init_events(self) -> None:
        pass

    def fill_data(self) -> None:
        self.fill_seasons_table()
        self.fill_series_table()

    def fill_seasons_table(self) -> None:
        self.tableWidget_2.clearContents()

        row_count = len(self.deleted_seasons)
        self.label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.tableWidget_2.setRowCount(row_count)

        for row_index, season in enumerate(self.deleted_seasons):
            # Case à cocher
            restore_checkbox = QCheckBox()
            self.tableWidget_2.setCellWidget(row_index, 0, restore_checkbox)

            # TODO: Ajouter les colonnes supplémentaires

            columns = [str(season.serie.sort_id), season.serie.name, str(season.sort_id), season.name, season.type.name, season.state]
            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                item.setData(Qt.ItemDataRole.UserRole, season.id)
                self.tableWidget_2.setItem(row_index, col_index + 1, item)

        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(self.tableWidget_2.columnCount() - 1,
                                                                 QHeaderView.ResizeMode.ResizeToContents)

    def fill_series_table(self) -> None:
        self.tableWidget_1.clearContents()

        row_count = len(self.deleted_series)
        self.label_3.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.tableWidget_1.setRowCount(row_count)

        for row_index, serie in enumerate(self.deleted_series):
            # Case à cocher
            restore_checkbox = QCheckBox()
            self.tableWidget_1.setCellWidget(row_index, 0, restore_checkbox)

            # TODO: Ajouter les colonnes supplémentaires

            columns = [str(serie.sort_id), serie.name] # TODO: Nombre de saisons
            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                item.setData(Qt.ItemDataRole.UserRole, serie.id)
                self.tableWidget_1.setItem(row_index, col_index + 1, item)

        self.tableWidget_1.resizeColumnsToContents()
        self.tableWidget_1.horizontalHeader().setSectionResizeMode(self.tableWidget_1.columnCount() - 1,
                                                                 QHeaderView.ResizeMode.ResizeToContents)


    def get_checked_for_restoration(self) -> None:
        # Séries
        for row_index in range(self.tableWidget_1.rowCount()):
            if self.tableWidget_1.cellWidget(row_index, 0).isChecked():
                serie_id = self.tableWidget_1.item(row_index, 1).data(Qt.ItemDataRole.UserRole)
                self.series_to_restore.append(serie_id)

        # Saisons
        for row_index in range(self.tableWidget_2.rowCount()):
            if self.tableWidget_2.cellWidget(row_index, 0).isChecked():
                season_id = self.tableWidget_2.item(row_index, 1).data(Qt.ItemDataRole.UserRole)
                self.seasons_to_restore.append(season_id)

    def restore_elements(self):
        # Séries
        for serie_id in self.series_to_restore:
            serie = Series.get(serie_id)
            serie.is_deleted = 0
            serie.save()

        # Saisons
        for season_id in self.seasons_to_restore:
            season = Seasons.get(season_id)
            season.is_deleted = 0
            season.save()

    def accept(self) -> None:
        self.get_checked_for_restoration()
        self.restore_elements()

        super().accept()

    def reject(self) -> None:
        super().reject()

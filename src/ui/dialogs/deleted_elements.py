import os

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout, QWidget
from PyQt5.uic import loadUi


class DeletedElements(QDialog):
    def __init__(self, deleted_series, deleted_seasons):
        super(DeletedElements, self).__init__()

        self.deleted_series = deleted_series
        self.deleted_seasons = deleted_seasons
        self.seasons_to_restore = []

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "deleted_elements.ui"), self)
        self.fill_data()

    def init_events(self):
        pass

    def fill_data(self):
        row_count = len(self.deleted_seasons)
        self.label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.tableWidget.setRowCount(row_count)

        for row_index, season in enumerate(self.deleted_seasons):
            # Case à cocher
            # restore_checkbox_widget = QWidget()
            # restore_checkbox_h_box = QHBoxLayout()
            restore_checkbox = QCheckBox()
            # restore_checkbox_h_box.addWidget(restore_checkbox)
            # favorite_checkbox.setEnabled(False)
            # favorite_checkbox.setChecked(season.favorite)
            # restore_checkbox_widget.setLayout(restore_checkbox_h_box)
            self.tableWidget.setCellWidget(row_index, 0, restore_checkbox)

            # TODO: Ajouter les colonnes supplémentaires

            columns = [season.serie.name, season.name, season.type.name, season.state]
            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                item.setData(Qt.UserRole, season.id)
                self.tableWidget.setItem(row_index, col_index+1, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
                                                                 QHeaderView.ResizeToContents)


    def get_checked_for_restoration(self):
        # Saisons
        for row_index in range(self.tableWidget.rowCount()):
            if self.tableWidget.cellWidget(row_index, 0).isChecked():
                season_id = self.tableWidget.item(row_index, 1).data(Qt.UserRole)
                self.seasons_to_restore.append(season_id)

    def accept(self):
        self.get_checked_for_restoration()
        super(DeletedElements, self).accept()

    def reject(self):
        super(DeletedElements, self).reject()

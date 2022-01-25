import os

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.uic import loadUi


class DeletedElements(QDialog):
    def __init__(self, deleted_series, deleted_seasons):
        super(DeletedElements, self).__init__()

        self.deleted_series = deleted_series
        self.deleted_seasons = deleted_seasons

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), 'deleted_elements.ui'), self)
        self.setWindowTitle(self.serie.name)

        self.fill_data()

    def init_events(self):
        pass

    def fill_data(self):
        row_count = len(self.deleted_seasons)
        self.label.setText("Nombre d'éléments: " + str(row_count))
        self.tableWidget.setRowCount(row_count)
        for row_index, season in enumerate(self.deleted_seasons):
            # TODO: Ajouter les colonnes supplémentaires
            columns = [season.serie.name, season.name, season.type.name, season.state]
            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, season.id)
                self.tableWidget.setItem(row_index, col_index, item)

    def accept(self):
        super(DeletedElements, self).accept()

    def reject(self):
        super(DeletedElements, self).reject()

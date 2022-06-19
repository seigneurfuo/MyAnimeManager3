import os

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi


class ViewHistory(QDialog):
    def __init__(self, season_id, rows):
        super(ViewHistory, self).__init__()

        self.season_id = season_id
        self.rows = rows

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "view_history.ui"), self)
        # TODO: Title
        self.setWindowTitle(self.tr("Historique de visionnage"))

        self.fill_data()

    def init_events(self):
        pass

    def fill_data(self):
        row_count = len(self.rows)
        self.label.setText("Nombre d'éléments: " + str(row_count))
        self.tableWidget.setRowCount(row_count)

        for row_index, row in enumerate(self.rows):
            columns = [row.date.strftime("%d/%m/%Y"), row.season.name, str(row.episodes)]
            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setToolTip(item.text())
                self.tableWidget.setItem(row_index, col_index, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1, QHeaderView.ResizeToContents)

    def accept(self):
        super(ViewHistory, self).accept()

    def reject(self):
        super(ViewHistory, self).reject()

import os

from PyQt6.QtWidgets import QDialog, QTableWidgetItem
from PyQt6.uic import loadUi


class CollectionProblemsDialog(QDialog):
    def __init__(self, parent, messages):
        super().__init__(parent=parent)

        self.messages = messages

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "collection_problems.ui"), self)
        self.setWindowTitle(self.tr("Vérification des données"))

        self.fill_data()

    def init_events(self):
        pass

    def fill_data(self):
        row_count = len(self.messages)
        self.label.setText(self.tr("Nombre d'éléments: ") + str(row_count))
        self.tableWidget.setRowCount(row_count)

        for row_index, message in enumerate(self.messages):
            item = QTableWidgetItem(message)
            item.setToolTip(item.text())
            self.tableWidget.setItem(row_index, 0, item)

    def accept(self):
        super().accept()

    def reject(self):
        super().reject()

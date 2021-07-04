import os

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.uic import loadUi


class DeletedElementsDialog(QDialog):
    def __init__(self, deleted_seasons):
        super(DeletedElementsDialog, self).__init__()

        #self.parent = parent
        self.deleted_seasons = deleted_seasons

        self.init_ui()
        self.init_events()


    def init_ui(self):
        loadUi(os.path.join(QDir.currentPath(), 'ui/dialogs/deleted_elements_dialog.ui'), self)

        self.fill_table()


    def init_events(self):
        pass


    def fill_table(self):
        self.tableWidget.setRowCount(0)

        deleted_seasons_count = len(self.deleted_seasons)

        self.label.setText("Nombre d'éléments: " + str(deleted_seasons_count))

        self.tableWidget.setRowCount(deleted_seasons_count)
        for row_index, season in enumerate(self.deleted_seasons):
            # TODO: Ajouter les colonnes supplémentaires
            columns = [season.serie.name, season.name, season.seasons_type.name]

            print(columns)

            for col_index, value in enumerate(columns):
                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, season.id_)
                self.tableWidget.setItem(row_index, col_index, item)


    def accept(self):
        super(DeletedElementsDialog, self).accept()


    def reject(self):
        super(DeletedElementsDialog, self).reject()
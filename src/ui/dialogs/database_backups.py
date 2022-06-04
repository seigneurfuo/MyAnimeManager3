import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.uic import loadUi

from db_backups_manager import DBBackupsManager


class DatabaseHistory(QDialog):
    def __init__(self, parent):
        super(DatabaseHistory, self).__init__()
        self.parent = parent

        self.db_backups = []
        self.selected_backup = None

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "database_backups.ui"), self)
        # self.setWindowTitle(self.serie.name)

        self.fill_data()

    def init_events(self):
        self.pushButton.clicked.connect(self.when_restore_button_clicked)
        self.pushButton_2.clicked.connect(self.when_create_button_clicked)

    def when_restore_button_clicked(self):
        selected_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        selected_backup = selected_item.data(Qt.UserRole) if selected_item else None

        # FIXME: Ce qu'il y à au dessus ne fonctione pas (le filtrage de la sélection

        if selected_backup:
            self.selected_backup = selected_backup

        self.close()

    def when_create_button_clicked(self):
        db_backups_manager = DBBackupsManager(self.parent)
        db_backups_manager.backup_current_database(automatic=False)

        self.fill_data()

    def fill_data(self):
        db_backups_manager = DBBackupsManager(self.parent)
        db_backups = db_backups_manager.get_dbs_list()

        row_count = len(db_backups)
        self.tableWidget.setRowCount(row_count)

        for row_index, filepath in enumerate(db_backups):
            short_filename = os.path.basename(filepath)

            if "-manual-" in short_filename or "-auto-" in short_filename:
                item = QTableWidgetItem(short_filename)
                item.setToolTip(filepath)
                item.setData(Qt.UserRole, filepath)
                self.tableWidget.setItem(row_index, 0, item)

                state = self.tr("Manuelle") if "-manual-" in short_filename else self.tr("Automatique")

                item = QTableWidgetItem(state)
                item.setToolTip(state)
                self.tableWidget.setItem(row_index, 1, item)

        self.tableWidget.resizeColumnsToContents()

    def reject(self):
        super(DatabaseHistory, self).reject()

import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi

from db_backups_manager import DBBackupsManager


class DatabaseHistory(QDialog):
    def __init__(self, parent):
        super(DatabaseHistory, self).__init__()
        self.parent = parent

        self.db_backups = []
        self.selected_backup = None
        self.folderpath = os.path.join(os.path.dirname(__file__))

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(self.folderpath, "database_backups.ui"), self)
        # self.setWindowTitle(self.serie.name)

        self.fill_data()

    def init_events(self):
        self.pushButton.clicked.connect(self.when_restore_button_clicked)
        self.pushButton_2.clicked.connect(self.when_create_button_clicked)
        self.pushButton_3.clicked.connect(self.when_remove_button_clicked)

    def when_restore_button_clicked(self):
        # FIXME: Crash
        selected_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if selected_item:
            selected_backup = selected_item.data(Qt.UserRole) if selected_item else None

            db_backups_manager = DBBackupsManager(self.parent)
            db_backups_manager.restore_database_backup(selected_backup)

            self.selected_backup = selected_backup
            self.close()

    def when_create_button_clicked(self):
        db_backups_manager = DBBackupsManager(self.parent)
        db_backups_manager.backup_current_database(automatic=False)

        self.fill_data()

    def when_remove_button_clicked(self):
        current_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if current_item:
            database_backup_filename = current_item.data(Qt.UserRole)
            print(database_backup_filename)

            db_backups_manager = DBBackupsManager(self.parent)
            db_backups_manager.remove_database_backup(database_backup_filename)

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
                item.setIcon(QIcon(os.path.join(self.folderpath, "resources/icons/blue-document-clock.png")))
                item.setToolTip(filepath)
                item.setData(Qt.UserRole, filepath)
                self.tableWidget.setItem(row_index, 0, item)

                if "-manual-" in short_filename:
                    state = self.tr("Sauvegarde manuelle")
                    state_icon = os.path.join(self.folderpath, "../../resources/icons/user.png")
                else:
                    state = self.tr("Sauvegarde automatique")
                    state_icon = os.path.join(self.folderpath, "../../resources/icons/database.png")

                item = QTableWidgetItem(state)
                item.setIcon(QIcon(state_icon))
                item.setToolTip(state)
                self.tableWidget.setItem(row_index, 1, item)


        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1, QHeaderView.ResizeToContents)


    def reject(self):
        super(DatabaseHistory, self).reject()

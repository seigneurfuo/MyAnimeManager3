import datetime
import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt6.uic import loadUi

from db_backups_manager import DBBackupsManager


class DatabaseHistoryDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent

        self.db_backups = []
        self.selected_backup = None
        self.folderpath = os.path.join(os.path.dirname(__file__))

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(self.folderpath, "database_history.ui"), self)
        self.setWindowTitle("Sauvegardes")
        self.label_2.setText("Nombre de sauvegardes automatiques à conserver: {}".format(self.parent.parent.settings["backups_limit"]))

        self.fill_data()

    def init_events(self):
        self.pushButton.clicked.connect(self.when_restore_button_clicked)
        self.pushButton_2.clicked.connect(self.when_create_button_clicked)
        self.pushButton_3.clicked.connect(self.when_remove_button_clicked)

    def when_restore_button_clicked(self):
        selected_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if selected_item:
            selected_backup = selected_item.data(Qt.ItemDataRole.UserRole) if selected_item else None

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
            database_backup_filename = current_item.data(Qt.ItemDataRole.UserRole)
            print(database_backup_filename)

            db_backups_manager = DBBackupsManager(self.parent)
            db_backups_manager.remove_database_backup(database_backup_filename)

            self.fill_data()

    def fill_data(self):
        db_backups_manager = DBBackupsManager(self.parent)
        db_backups = db_backups_manager.get_dbs_list()

        self.tableWidget.clearContents()

        row_count = len(db_backups)
        self.tableWidget.setRowCount(row_count)

        for row_index, filepath in enumerate(db_backups):

            # Nom
            filename = os.path.basename(filepath)
            date_elements = filename.split("-")
            short_filename = f"{date_elements[2]}/{date_elements[1]}/{date_elements[0]} à {date_elements[3]}h{date_elements[4]}m{date_elements[5]}s"

            item = QTableWidgetItem(short_filename)
            item.setIcon(QIcon(os.path.join(self.folderpath, "resources/icons/blue-document-clock.png")))
            item.setToolTip(filepath)
            item.setData(Qt.ItemDataRole.UserRole, filepath)
            self.tableWidget.setItem(row_index, 0, item)

            # Icone
            if "-manual-" in filename:
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
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
                                                                 QHeaderView.ResizeMode.ResizeToContents)

    def reject(self):
        super().reject()

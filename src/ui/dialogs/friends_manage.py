import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QCalendarWidget, QTableWidgetItem, QHeaderView
from PyQt6.uic import loadUi

from database import Friends


class FriendManageDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)

        self.friends_list = []
        self.edited_friend_id = None

        self.init_ui()
        self.init_events()
        self.fill_data()

    def init_ui(self) -> None:
        loadUi(os.path.join(os.path.dirname(__file__), "friends_manage.ui"), self)

    def init_events(self) -> None:
        self.pushButton.clicked.connect(self.when_new_friend_button_clicked)
        self.pushButton_3.clicked.connect(self.when_save_friend_button_clicked)
        self.tableWidget.currentCellChanged.connect(self.when_friends_table_current_cell_changed)

    def fill_data(self) -> None:
        self.reload_friends_list()
        self.fill_friends_table()

    def fill_friends_table(self) -> None:
        self.tableWidget.clearContents()

        row_count = len(self.friends_list)
        # self.label_82.setText(str(row_count))
        self.tableWidget.setRowCount(row_count)

        for row_index, friend in enumerate(self.friends_list):
            item = QTableWidgetItem(friend.name)
            item.setToolTip(item.text())
            item.setData(Qt.ItemDataRole.UserRole, friend.id)
            self.tableWidget.setItem(row_index, 0, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1, QHeaderView.ResizeMode.ResizeToContents)

    def reload_friends_list(self) -> None:
        self.friends_list = Friends.select()

    def when_new_friend_button_clicked(self) -> None:
        self.edited_friend_id = None
        self.lineEdit.clear()

    def when_save_friend_button_clicked(self) -> None:
        if self.edited_friend_id:
            friend = Friends.get(self.edited_friend_id)
        else:
            friend = Friends()

        friend.name = self.lineEdit.text().strip()
        friend.save()

        self.reload_friends_list()
        self.fill_friends_table()

    def when_friends_table_current_cell_changed(self) -> None:
        selected_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if selected_item:
            selected_friend_id = selected_item.data(Qt.ItemDataRole.UserRole)
            self.edited_friend_id = selected_friend_id
            friend = Friends.get(self.edited_friend_id)

            self.lineEdit.setText(friend.name)

    def save_data(self) -> None:
        pass

    def accept(self) -> None:
        self.save_data()
        super().accept()

    def reject(self) -> None:
        super().reject()

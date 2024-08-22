import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QCalendarWidget, QTableWidgetItem, QHeaderView
from PyQt6.uic import loadUi

from ui.dialogs.friends_manage import FriendManageDialog


class EditDateDialog(QDialog):
    def __init__(self, parent, planning_data, full_friends_list) -> None:
        super().__init__(parent=parent)

        self.parent = parent

        self.planning_data = planning_data
        self.full_friends_list = full_friends_list
        self.friends = [friend_planning.friend for friend_planning in planning_data.friends]

        self.friends_to_add = []
        self.friends_to_remove = []

        self.init_ui()
        self.init_events()
        self.fill_data()

    def init_ui(self) -> None:
        loadUi(os.path.join(os.path.dirname(__file__), "edit_date.ui"), self)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar.setSelectedDate(self.planning_data.date)

        self.verticalLayout_2.insertWidget(0, self.calendar)

        # Si on n'a pas activé la gestion des amis, on masque divers éléments
        if not self.parent.parent.parent.settings["friends_enabled"]:
            self.tableWidget.hide()
            self.comboBox.hide()
            self.pushButton.hide()
            self.pushButton_2.hide()
            self.pushButton_3.hide()


    def init_events(self) -> None:
        self.calendar.selectionChanged.connect(self.update_date_label)
        self.pushButton.clicked.connect(self.when_add_friend_button_clicked)
        self.pushButton_2.clicked.connect(self.when_remove_friend_button_clicked)
        self.pushButton_3.clicked.connect(self.open_friends_list)

    def fill_data(self) -> None:
        self.update_friends_combobox()

        original_date = self.planning_data.date.strftime("%d/%m/%Y")
        self.old_date_label.setText(original_date)
        self.new_date_label.setText(original_date)

        self.update_date_label()
        self.fill_friends_table()
        self.update_friends_combobox()

    def when_add_friend_button_clicked(self) -> None:
        friend = self.comboBox.currentData()
        if friend and friend not in self.friends:
            self.friends.append(friend)

            self.fill_friends_table()
            self.update_friends_combobox()

    # FIXME: Marche pas
    def when_remove_friend_button_clicked(self) -> None:
        selected_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if selected_item:
            selected_friend_id = selected_item.data(Qt.ItemDataRole.UserRole)

            # Suppression de l'id de l'ami selectionné
            for index, friend in enumerate(self.friends):
                if friend.id == selected_friend_id:
                    self.friends.pop(index)
                    break

            self.fill_friends_table()
            self.update_friends_combobox()

    def fill_friends_table(self) -> None:
        self.tableWidget.clearContents()

        row_count = len(self.friends)
        # self.label_82.setText(str(row_count))
        self.tableWidget.setRowCount(row_count)

        for row_index, friend in enumerate(self.friends):
            item = QTableWidgetItem(friend.name)
            item.setToolTip(item.text())
            item.setData(Qt.ItemDataRole.UserRole, friend.id)
            self.tableWidget.setItem(row_index, 0, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
                                                                 QHeaderView.ResizeMode.ResizeToContents)

    def update_friends_combobox(self) -> None:
        self.comboBox.clear()
        for friend in self.full_friends_list:
            if friend not in self.friends:
                self.comboBox.addItem(friend.name, userData=friend)

    def update_date_label(self) -> None:
        date = self.calendar.selectedDate()
        date_string = date.toString("dd/MM/yyyy")
        self.new_date_label.setText(date_string)

    def open_friends_list(self) -> None:
        dialog = FriendManageDialog(self)
        if dialog.exec():
            self.full_friends_list = dialog.friends_list
            self.update_friends_combobox()

    def save_data(self) -> None:
        new_date = self.calendar.selectedDate().toPyDate()
        if new_date and new_date != self.planning_data.date:
            self.planning_data.date = new_date
            self.planning_data.save()

        # TODO: Save
        old_friends_ids = [friend_planning.friend.id for friend_planning in self.planning_data.friends]
        friends_ids = [friend.id for friend in self.friends]

        self.friends_to_remove = [item for item in old_friends_ids if item not in friends_ids]
        self.friends_to_add = [item for item in friends_ids if item not in old_friends_ids]

    def accept(self) -> None:
        self.save_data()
        super().accept()

    def reject(self) -> None:
        super().reject()

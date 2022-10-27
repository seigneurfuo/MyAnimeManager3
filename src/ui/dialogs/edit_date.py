import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QCalendarWidget, QComboBox, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi

class EditDateDialog(QDialog):
    def __init__(self, planning_data, full_friends_list):
        super(EditDateDialog, self).__init__()

        self.planning_data = planning_data
        self.full_friends_list = full_friends_list
        self.friends = [friend_planning.friend for friend_planning in planning_data.friends]

        loadUi(os.path.join(os.path.dirname(__file__), "edit_date.ui"), self)

        self.init_ui()
        self.init_events()
        self.fill_data()

    def init_ui(self):
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setSelectedDate(self.planning_data.date)

        self.verticalLayout_2.addWidget(self.calendar)

    def init_events(self):
        self.calendar.selectionChanged.connect(self.update_date_label)
        self.pushButton.clicked.connect(self.when_add_friend_button_clicked)
        self.pushButton_2.clicked.connect(self.when_remove_friend_button_clicked)

    def fill_data(self):
        self.update_friends_combobox()

        original_date = self.planning_data.date.strftime("%d/%m/%Y")
        self.old_date_label.setText(original_date)
        self.new_date_label.setText(original_date)

        self.update_date_label()
        self.fill_friends_table()
        self.update_friends_combobox()

    def when_add_friend_button_clicked(self):
        friend = self.comboBox.currentData()
        if friend and friend not in self.friends:
            self.friends.append(friend)

            self.fill_friends_table()
            self.update_friends_combobox()

    # FIXME: Marche pas
    def when_remove_friend_button_clicked(self):
        selected_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if selected_item:
            friend = selected_item.data(Qt.UserRole)
            self.friends.remove(friend)

            self.fill_friends_table()
            self.update_friends_combobox()

    def fill_friends_table(self):
        row_count = len(self.friends)
        # self.label_82.setText(str(row_count))
        self.tableWidget.setRowCount(row_count)

        for row_index, friend in enumerate(self.friends):
            item = QTableWidgetItem(friend.name)
            item.setToolTip(item.text())
            item.setData(Qt.UserRole, friend.id)
            self.tableWidget.setItem(row_index, 0, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
                                                                   QHeaderView.ResizeToContents)

    def update_friends_combobox(self):
        self.comboBox.clear()
        for friend in self.full_friends_list:
            if friend not in self.friends:
                self.comboBox.addItem(friend.name, userData=friend)

    def update_date_label(self):
        date = self.calendar.selectedDate()
        date_string = date.toString("dd/MM/yyyy")
        self.new_date_label.setText(date_string)

    def save_data(self):
        new_date = self.calendar.selectedDate().toPyDate()
        if new_date and new_date != self.planning_data.date:
            self.planning_data.date = new_date
            self.planning_data.save()

        # TODO: Save

    def accept(self):
        self.save_data()
        super(EditDateDialog, self).accept()

    def reject(self):
        super(EditDateDialog, self).reject()

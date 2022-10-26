import os

from PyQt5.QtWidgets import QDialog, QCalendarWidget
from PyQt5.uic import loadUi


class EditDateDialog(QDialog):
    def __init__(self, planning_data):
        super(EditDateDialog, self).__init__()

        self.planning_data = planning_data
        self.full_friends_list = []
        self.friends = []

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

    def fill_data(self):
        original_date = self.planning_data.date.strftime("%d/%m/%Y")
        self.old_date_label.setText(original_date)
        self.new_date_label.setText(original_date)

        self.update_date_label()

    def update_date_label(self):
        date = self.calendar.selectedDate()
        date_string = date.toString("dd/MM/yyyy")
        self.new_date_label.setText(date_string)

    def save_data(self):
        new_date = self.calendar.selectedDate().toPyDate()
        if new_date and new_date != self.planning_data.date:
            self.planning_data.date = new_date
            self.planning_data.save()

    def accept(self):
        self.save_data()
        super(EditDateDialog, self).accept()

    def reject(self):
        super(EditDateDialog, self).reject()

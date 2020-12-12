#!/bin/env python3
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDir, QTime

import os

from utils import duration_calculation


class ToolsTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent_mainwindow = parent
        self.init_ui()
        self.init_events()


    def init_ui(self):
        loadUi(os.path.join(QDir.currentPath(), 'ui/tools_tab_content.ui'), self)


    def init_events(self):
        self.go_button.clicked.connect(self.on_duration_calculation_button_click)
        self.get_current_time_button.clicked.connect(self.on_get_current_time_button_click)


    def on_duration_calculation_button_click(self):
        self.listWidget.clear()

        episodes_number = self.spinBox.value()
        episodes_lenght = self.spinBox_2.value()
        start_time_string = str(self.timeEdit.dateTime().toString("hh:mm"))

        rows = duration_calculation(episodes_number, episodes_lenght, start_time_string)

        for row in rows:
            self.listWidget.addItem(QListWidgetItem(row))


    def on_get_current_time_button_click(self):
        self.timeEdit.setTime(QTime.currentTime())
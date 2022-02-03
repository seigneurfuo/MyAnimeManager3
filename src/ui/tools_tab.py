#!/bin/env python3
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDir, QTime

import os

from utils import duration_calculation


class ToolsTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.init_ui()
        self.init_events()


    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "tools_tab.ui"), self)

    def init_events(self):
        self.go_button.clicked.connect(self.on_duration_calculation_button_click)
        self.get_current_time_button.clicked.connect(self.on_get_current_time_button_click)

        # Si n'importe quelle valeur de la spinbox est changée, alors on met à jour en temps réel
        self.timeEdit.timeChanged.connect(self.when_spinboxes_values_changed)
        self.spinBox.valueChanged.connect(self.when_spinboxes_values_changed)
        self.spinBox_2.valueChanged.connect(self.when_spinboxes_values_changed)
        self.spinBox_3.valueChanged.connect(self.when_spinboxes_values_changed)
        self.spinBox_4.valueChanged.connect(self.when_spinboxes_values_changed)

    def when_visible(self):
        self.set_current_time()

    def duration_calculation(self):
        self.listWidget.clear()

        episodes_count = self.spinBox.value()
        episodes_duration = self.spinBox_2.value()

        pause_every = self.spinBox_4.value()
        pause_duration = self.spinBox_3.value()

        start_time_string = str(self.timeEdit.dateTime().toString("hh:mm"))

        rows = duration_calculation(episodes_count, episodes_duration, pause_every, pause_duration, start_time_string)

        # TODO: Tablewidget Type: Episode / Pause, Heure début, Heure fin
        for row in rows:
            self.listWidget.addItem(QListWidgetItem(row))

    def when_spinboxes_values_changed(self):
        self.duration_calculation()

    def on_duration_calculation_button_click(self):
        self.duration_calculation()

    def set_current_time(self):
        self.timeEdit.setTime(QTime.currentTime())

    def on_get_current_time_button_click(self):
        self.set_current_time()
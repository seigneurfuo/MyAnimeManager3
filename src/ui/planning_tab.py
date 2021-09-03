#!/bin/env python3
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.uic import loadUi

import os


class PlanningTab(QWidget):
    def __init__(self, parent, app_dir):
        super().__init__(parent)

        self.parent_mainwindow = parent
        self.app_dir = app_dir

        self.init_ui()
        self.init_events()


    def init_ui(self):
        loadUi(os.path.join(self.app_dir, 'ui/planning_tab.ui'), self)


    def init_events(self):
        pass
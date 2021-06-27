from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

import os


class AboutWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent_qmainwindow = parent
        self.init_ui()

    def init_ui(self):
        loadUi(os.path.join(QDir.currentPath(), 'ui/about_window.ui'), self)

        self.name_label.setText(self._parent_qmainwindow.parent_qapplication.name)
        self.version_label.setText(self._parent_qmainwindow.parent_qapplication.version)
        self.description_label.setText(self._parent_qmainwindow.parent_qapplication.description)

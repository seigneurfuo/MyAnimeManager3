import os
from platform import python_version

from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from peewee import __version__ as peewee_version

import common


class About(QDialog):
    def __init__(self, parent):
        super(About, self).__init__()
        self.parent = parent

        self.logo_clicks = 0
        self.logo_data = ["heart.png", "user.png"]

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "about.ui"), self)
        self.setWindowTitle(self.tr("A propos"))

        self.fill_data()

    def init_events(self):
        self.logo.mousePressEvent = self.when_logo_clicked

    def fill_data(self):
        fields = [(self.application_version, common.app_version),
                  (self.python_version, python_version()),
                  (self.qt_version, QT_VERSION_STR),
                  (self.pyqt_version, PYQT_VERSION_STR),
                  (self.peewee_version, peewee_version)]

        for field, value in fields:
            field.setText(value)

    def when_logo_clicked(self, event):

        pixmap = os.path.join(os.path.dirname(__file__), "../../resources/icons/", self.logo_data[self.logo_clicks])
        self.logo.setPixmap(QPixmap(pixmap))

        if self.logo_clicks == 1:
            self.logo_clicks = 0
        else:
            self.logo_clicks += 1


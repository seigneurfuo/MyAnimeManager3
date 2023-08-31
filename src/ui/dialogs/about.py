import os
from platform import python_version

from PyQt6.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

from peewee import __version__ as peewee_version

from core import app_name, app_version


class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.parent = parent

        self.logo_clicks = 0
        self.icons_path = os.path.join(os.path.dirname(__file__), "../../resources/icons")
        self.logo_data = [icon for icon in os.listdir(self.icons_path)
                          if os.path.isfile(os.path.join(self.icons_path, icon))
                          and icon.endswith(".png")]

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "about.ui"), self)
        self.setWindowTitle(self.tr("A propos"))

        self.fill_data()

    def init_events(self):
        self.logo.mousePressEvent = self.when_logo_clicked

    def fill_data(self):
        fields = [(self.application_name, app_name),
                  (self.application_version, app_version),
                  (self.python_version, python_version()),
                  (self.qt_version, QT_VERSION_STR),
                  (self.pyqt_version, PYQT_VERSION_STR),
                  (self.peewee_version, peewee_version)]

        for field, value in fields:
            field.setText(value)

    def when_logo_clicked(self, event):
        pixmap = os.path.join(os.path.dirname(__file__), self.icons_path, self.logo_data[self.logo_clicks])
        self.logo.setPixmap(QPixmap(pixmap))

        if self.logo_clicks == len(self.logo_data) - 1:
            self.logo_clicks = 0
        else:
            self.logo_clicks += 1

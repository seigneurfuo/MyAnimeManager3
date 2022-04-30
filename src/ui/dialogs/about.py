import os
from platform import python_version

from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from peewee import __version__ as peewee_version


class About(QDialog):
    def __init__(self):
        super(About, self).__init__()

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "about.ui"), self)
        self.setWindowTitle(self.tr("A propos"))

        self.fill_data()

    def init_events(self):
        pass

    def fill_data(self):
        fields = [(self.application_version, ""),
                  (self.python_version, python_version()),
                  (self.qt_version, QT_VERSION_STR),
                  (self.pyqt_version, PYQT_VERSION_STR),
                  (self.peewee_version, peewee_version)]

        for field, value in fields:
            field.setText(value)

        # TODO:
        # self.name_label.setText(self._parent_qmainwindow.parent_qapplication.name)
        # self.version_label.setText(self._parent_qmainwindow.parent_qapplication.version)
        # self.description_label.setText(self._parent_qmainwindow.parent_qapplication.description)

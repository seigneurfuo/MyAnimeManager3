from PyQt5.QtWidgets import QApplication

import default_settings
from ui.mainwindow import MainWindow


class Application(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.name = "MyAnimeManager 3"
        self.version = "0.0.1"
        self.description = self.tr("Un gestionnaire de séries multiplateforme écrit en Python3 et Qt5")

        self.setApplicationName(self.name)
        self.setApplicationDisplayName(self.name)
        self.setApplicationVersion(self.version)

        self._DEFAULT_SETTINGS = default_settings.DEFAULT_SETTINGS

        self._launch_mainwindow()


    def _launch_mainwindow(self):
        self._mainwindow = MainWindow(self)
        self._mainwindow.show()

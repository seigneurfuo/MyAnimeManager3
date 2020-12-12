from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

import os

from ui.full_list_tab import FullListTab
from ui.tools_tab import ToolsTab

class MainWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent=None)
        self.parent = parent
        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(QDir.currentPath(), 'ui/mainwindow.ui'), self)

        # Onglet 2
        self.full_list_tab = FullListTab(self)
        self.full_list_tab_layout.addWidget(self.full_list_tab)

        # Onglet 3
        self.tools_tab = ToolsTab(self)
        self.tools_tab_layout.addWidget(self.tools_tab)


    def init_events(self):
        pass

    #print(self.parent_qapplication.profile.get_series())


    def closeEvent(self, a0):
        super().close()
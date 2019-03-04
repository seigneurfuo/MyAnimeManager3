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
        self._init_ui()
        self._init_events()

    def _init_ui(self):
        loadUi(os.path.join(QDir.currentPath(), 'ui/mainwindow.ui'), self)

        # Onglet 2
        self.full_list_tab = FullListTab(self)
        self.full_list_tab_layout.addWidget(self.full_list_tab)

        # Onglet 3
        self.tools_tab = ToolsTab(self)
        self.tools_tab_layout.addWidget(self.tools_tab)


    def _init_events(self):
        pass

    #print(self.parent_qapplication.profile.get_series())

    def _on_current_serie_changed(self, index):
        pass

    def _fill_serie_details(self, index):
        pass

    def _clear_serie_details(self):
        self.label.clear()

    def closeEvent(self, a0):
        self.parent_qapplication.profile.save()
        super().close()
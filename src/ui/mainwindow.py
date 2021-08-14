from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

import os

from utils import open_folder
from ui.full_list_tab import FullListTab
from ui.tools_tab import ToolsTab

class MainWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent=None)
        self.parent = parent
        self.app_dir = parent.app_dir

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(self.app_dir, 'ui/mainwindow.ui'), self)

        # Onglet 2
        self.full_list_tab = FullListTab(self, self.app_dir)
        self.full_list_tab_layout.addWidget(self.full_list_tab)

        # Onglet 3
        self.tools_tab = ToolsTab(self, self.app_dir)
        self.tools_tab_layout.addWidget(self.tools_tab)

    def init_events(self):
        # FIXME: Ouvrir plutot le dossier utilisateur !
        self.open_profile_action.triggered.connect(self.on_menu_action_open_profile_clicked_function)

    #print(self.parent_qapplication.profile.get_series())

    def on_menu_action_open_profile_clicked_function(self):
        open_folder(self.app_dir)

    def closeEvent(self, a0):
        super().close()
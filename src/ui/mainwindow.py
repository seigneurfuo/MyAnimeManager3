from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

import os

from utils import open_folder
from ui.planning_tab import PlanningTab
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

        # Onglet 1 - Planning
        planning_tab = PlanningTab(self, self.app_dir)
        self.planning_tab_layout.addWidget(planning_tab)

        # Onglet 2 - Liste des animés
        full_list_tab = FullListTab(self, self.app_dir)
        self.full_list_tab_layout.addWidget(full_list_tab)

        # Onglet 3 - Outils
        tools_tab = ToolsTab(self, self.app_dir)
        self.tools_tab_layout.addWidget(tools_tab)

    def init_events(self):
        # FIXME: Ouvrir plutot le dossier utilisateur !
        self.open_profile_action.triggered.connect(self.on_menu_action_open_profile_clicked_function)

    # TODO: evenement lors du click sur un onglet

    #print(self.parent_qapplication.profile.get_series())

    def on_menu_action_open_profile_clicked_function(self):
        open_folder(self.app_dir)


    def closeEvent(self, a0):
        super().close()
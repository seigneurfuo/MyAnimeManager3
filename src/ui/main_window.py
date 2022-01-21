from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

import os

from utils import open_folder
from ui.planning_tab import PlanningTab
from ui.full_list_tab import FullListTab
from ui.tools_tab import ToolsTab
from ui.dialogs.about import About


class MainWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent=None)
        self.parent = parent
        self.app_dir = parent.app_dir

        self.tabs = tuple()

        self.init_ui()
        self.init_events()

        # On met à jour les informations sur l'onglet charger en premier
        self.update_tab_content(self.tabWidget.currentIndex())

    def init_ui(self):
        loadUi(os.path.join(self.app_dir, 'ui/main_window.ui'), self)

        # Onglet 1 - Planning
        self.planning_tab = PlanningTab(self, self.app_dir)
        self.planning_tab_layout.addWidget(self.planning_tab)

        # Onglet 2 - Liste des animés
        self.full_list_tab = FullListTab(self, self.app_dir)
        self.full_list_tab_layout.addWidget(self.full_list_tab)

        # Onglet 4 - Outils
        self.tools_tab = ToolsTab(self, self.app_dir)
        self.tools_tab_layout.addWidget(self.tools_tab)

        # Remplissage de la liste des onglets
        self.tabs = (self.planning_tab, self.full_list_tab, None, self.tools_tab)

    def init_events(self):
        # FIXME: Ouvrir plutot le dossier utilisateur !
        self.open_profile_action.triggered.connect(self.on_menu_action_open_profile_clicked_function)

        self.planning_export_action.triggered.connect(self.on_menu_action_planning_export_clicked_function)
        self.about_action.triggered.connect(self.on_about_action_clicked_function)


        # Clic sur les onglets
        self.tabWidget.currentChanged.connect(self.on_current_tab_changed)

        # Affichage de l'emplacement des données de l'utilisateur
        #self.statusbar.showMessage(self.tr("Données utilisateur: {}".format(self.app_dir)))

    # TODO: evenement lors du click sur un onglet

    #print(self.parent_qapplication.profile.get_series())

    def update_tab_content(self, tab_index):
        if tab_index != -1 and tab_index < len(self.tabs) and self.tabs[tab_index] is not None:
            self.tabs[tab_index].when_visible()

    def on_current_tab_changed(self, tab_index):
        """
        Fonction qui est appelée lorsqu'un onglet est cliqué
        Il permet de lancer la fonction when_visible qui déclanche divers actions (MAJ de l'affichage, ...)
        dans l'onglet concerné

        :param tab_index: Index de l'onglet cliqué 0 à x
        :return: None
        """

        self.update_tab_content(tab_index)

    def on_menu_action_open_profile_clicked_function(self):
        open_folder(self.app_dir)


    def on_menu_action_planning_export_clicked_function(self):
        pass

    def on_about_action_clicked_function(self):
        dialog = About()
        dialog.exec_()


    def closeEvent(self, a0):
        super().close()

import os

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

import database
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
        self.profile_path = parent.profile_path

        self.tabs = tuple()

        self.init_ui()
        self.init_events()

        # On met à jour les informations sur l'onglet charger en premier
        self.update_tab_content(self.tabWidget.currentIndex())

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), 'main_window.ui'), self)

        # Onglet 1 - Planning
        planning_tab = PlanningTab(self)
        self.planning_tab_layout.addWidget(planning_tab)

        # Onglet 2 - Liste des animés
        full_list_tab = FullListTab(self)
        self.full_list_tab_layout.addWidget(full_list_tab)

        # Onglet 4 - Outils
        tools_tab = ToolsTab(self)
        self.tools_tab_layout.addWidget(tools_tab)

        # Remplissage de la liste des onglets
        self.tabs = (planning_tab, full_list_tab, None, tools_tab)

    def init_events(self):
        # FIXME: Ouvrir plutot le dossier utilisateur !
        self.open_profile_action.triggered.connect(self.when_menu_action_open_profile_clicked)

        self.planning_export_action.triggered.connect(self.when_menu_action_planning_export_clicked)
        self.about_action.triggered.connect(self.when_about_action_clicked)

        # Clic sur les onglets
        self.tabWidget.currentChanged.connect(self.when_current_tab_changed)

        # Affichage de l'emplacement des données de l'utilisateur
        # self.statusbar.showMessage(self.tr("Données utilisateur: {}".format(self.app_dir)))

    # TODO: evenement lors du click sur un onglet

    # print(self.parent_qapplication.profile.get_series())

    def update_tab_content(self, tab_index):
        if tab_index != -1 and tab_index < len(self.tabs) and self.tabs[tab_index] is not None:
            self.tabs[tab_index].when_visible()

    def when_current_tab_changed(self, tab_index):
        """
        Fonction qui est appelée lorsqu'un onglet est cliqué
        Il permet de lancer la fonction when_visible qui déclanche divers actions (MAJ de l'affichage, ...)
        dans l'onglet concerné

        :param tab_index: Index de l'onglet cliqué 0 à x
        :return: None
        """

        self.update_tab_content(tab_index)

    def when_menu_action_open_profile_clicked(self):
        open_folder(self.profile_path)

    def when_menu_action_planning_export_clicked(self):
        pass

    def when_about_action_clicked(self):
        dialog = About()
        dialog.exec_()

    # TODO: Désactiver la sauvegarde automatique
    def closeEvent(self, a0):
        super().close()


    #         # Si il y a eu des modifications
    #         if True: #TODO: Si il y à des chnagements
    #
    #             # Affiche la fenetre de dialogue d'enregistrement
    #             save_question = QMessageBox.question(self, 'Enregistrer les changements',
    #                                                  "Enregistrer les modifications ?",
    #                                                  QMessageBox.Yes, QMessageBox.No)
    #
    #             # Si on clique sur Oui (Sauvegarder)
    #             if save_question == QMessageBox.Yes:
    #                 # Enregistre les modifications dans la bdd
    #                 database.database.commit()
    #
    #             # Si on clique sur Quitter sans sauvegarder
    #             elif save_question == QMessageBox.No:
    #
    #                 # Annule tout les changements depuis le dernier enregistrement
    #                 database.database.rollback()
    #
    #         super().close()

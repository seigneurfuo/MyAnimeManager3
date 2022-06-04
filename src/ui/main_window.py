import os
import shutil
from datetime import datetime

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

import database
from ui.planning_tab import PlanningTab
from ui.full_list_tab import FullListTab
from ui.list2_tab import List2
from ui.tools_tab import ToolsTab

from ui.dialogs.about import About
from ui.dialogs.collection_problems import CollectionProblems
from ui.dialogs.database_backups import DatabaseHistory

from db_backups_manager import DBBackupsManager


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
        loadUi(os.path.join(os.path.dirname(__file__), "main_window.ui"), self)

        # Onglet 1 - Planning
        self.planning_tab = PlanningTab(self)
        self.planning_tab_layout.addWidget(self.planning_tab)

        # Onglet 2 - Liste des animés
        self.full_list_tab = FullListTab(self)
        self.full_list_tab_layout.addWidget(self.full_list_tab)

        # Onglet 3 - Liste des animés 2
        self.list2_tab = List2(self)
        self.list2_tab_layout.addWidget(self.list2_tab)

        # Onglet 4 - Outils
        self.tools_tab = ToolsTab(self)
        self.tools_tab_layout.addWidget(self.tools_tab)

        # Remplissage de la liste des onglets
        self.tabs = (self.planning_tab, self.full_list_tab, self.list2_tab, self.tools_tab)

        # Onglet par défaut
        self.tabWidget.setCurrentIndex(0)  # TODO: Configuration

    def init_events(self):
        # FIXME: Ouvrir plutot le dossier utilisateur !
        # Menus
        self.open_profile_action.triggered.connect(self.when_menu_action_open_profile_clicked)

        self.planning_export_action.triggered.connect(self.when_menu_action_planning_export_clicked)
        self.about_action.triggered.connect(self.when_menu__action_about_clicked)
        self.check_problems_action.triggered.connect(self.when_menu_action_check_collection_clicked)
        self.open_database_backups_action.triggered.connect(self.when_menu_action_open_database_history)

        # ----- Clic sur les onglets -----
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
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.profile_path))

    def when_menu_action_planning_export_clicked(self):
        pass

    # TODO: Changer l'emplacement et metre ça ailleurs dans un autre fichier
    def get_collection_problems(self):
        seasons_passed = []
        messages = []

        seasons = database.Seasons().select().join(database.Series).where(database.Seasons.is_deleted == 0).order_by(
            database.Seasons.sort_id)

        for season in seasons:
            if season.serie.id not in seasons_passed and season.state != 4:

                if season.serie.sort_id == 0 and (season.view_count > 0 or season.watched_episodes > 0):
                    seasons_passed.append(season.serie.id)
                    msg = "Série: {}. L'identifiant est toujours \"{}\" alors que des épisodes on déja étés vus.".format(
                        season.serie.name, season.serie.sort_id)
                    messages.append(msg)

                elif season.episodes == 0:
                    msg = "Série: {}. La saison \"{}\" n'a aucun nombre d'épisodes définis.".format(season.sort_id,
                                                                                                    season.name)
                    messages.append(msg)

                # On supprime tout les espaces. S'il ne reste rien, alors c'est que le tire de la saison est vide.
                elif season.name.replace(" ", "") == "":
                    msg = "Série: {}. La saison \"{}\" à un nom vide. ".format(season.serie.name, season.sort_id)
                    messages.append(msg)

        return messages

    def when_menu_action_check_collection_clicked(self):
        messages = self.get_collection_problems()
        dialog = CollectionProblems(messages)
        dialog.exec_()

    def when_menu__action_about_clicked(self):
        dialog = About()
        dialog.exec_()
        # tutorial(self)

    def when_menu_action_open_database_history(self):
        dialog = DatabaseHistory(self)
        dialog.exec_()
        selected_backup = dialog.selected_backup

        if selected_backup:
            db_backups_manager = DBBackupsManager(self)
            db_backups_manager.restore_database_backup(selected_backup)

            QMessageBox.information(None, "Base de données restaurée", \
                                    "Le logiciel va se fermer. Veuillez le relancer pour que les modifications soient prises en compte", QMessageBox.Ok)
            self.close()


    def backup_database_before_quit(self):
        db_backups_manager = DBBackupsManager(self)
        db_backups_manager.backup_current_database()

    # TODO: Désactiver la sauvegarde automatique
    def closeEvent(self, a0):
        database.database.commit()
        self.backup_database_before_quit()

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

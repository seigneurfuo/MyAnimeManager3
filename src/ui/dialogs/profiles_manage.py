import os

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QToolButton, QMessageBox
from PyQt5.uic import loadUi

from profiles import Profiles
from ui.dialogs.profile_edit import ProfileEditDialog


class ProfilesManageDialog(QDialog):
    class roles:
        manage = 0
        choose = 1

    def __init__(self, role, current_profile):
        super().__init__()

        self.role = role
        self.current_profile = current_profile
        self.profiles_list = None
        self.selected_profile = None

        self.max_btn_on_row = 3

        self.update_profiles_list()

        self.init_ui()
        self.fill_data()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "profiles_manage.ui"), self)

        if self.profiles_list:
            self.no_profile_found_label.hide()

        # Si on est en mode selection de profil, on désactive le bouton de supression et le bouton d'édition
        if self.role == ProfilesManageDialog.roles.choose:
            self.label.hide()
            self.pushButton_2.hide()
            self.pushButton_3.hide()

            title = self.tr("Choix d'un profil")

        else:
            title = self.tr("Gestion des profils")

        self.setWindowTitle(title)

    def init_events(self):
        self.pushButton.clicked.connect(self.when_create_profile_button_clicked)
        self.pushButton_2.clicked.connect(self.when_delete_profile_button_clicked)
        self.pushButton_3.clicked.connect(self.when_edit_profile_button_clicked)

    def update_profiles_list(self):
        self.selected_profile = None
        self.profiles_list = Profiles.get_profiles_list()

    def remove_buttons_from_grid(self):
        # Pour le refresh
        # https://stackoverflow.com/a/13103617
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)

    def fill_data(self):
        row_index = 0
        col_index = 0

        # Reset bouton
        if self.role == ProfilesManageDialog.roles.manage:
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)

        for index, profile in enumerate(self.profiles_list):
            btn = QToolButton()
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setText(profile.name)
            btn.setFixedSize(128, 128)
            btn.setIcon(QIcon(profile.get_picture()))
            btn.setIconSize(QSize(int(btn.height() - 32), int(btn.width() - 32)))
            btn.clicked.connect(lambda lamdba, profile=profile: self.set_profile(profile))

            # Si le profil actuel correpond au bouton en cours
            if self.current_profile and profile.path == self.current_profile.path:
                name = self.tr("{} (Profil actuel)").format(profile.name)
                btn.setText(name)

            # Ligne suivante si maximal attends
            if index != 0 and index % self.max_btn_on_row == 0:
                col_index = 0
                row_index += 1

            self.gridLayout.addWidget(btn, row_index, col_index)
            col_index += 1

    def update_all(self):
        self.selected_profile = None

        self.update_profiles_list()
        self.remove_buttons_from_grid()
        self.fill_data()

    def set_profile(self, profile):
        # Si le profil à été supprimé
        if not profile.exists():
            self.update_profiles_list()
            self.remove_buttons_from_grid()
            self.fill_data()
            return None

        self.selected_profile = profile

        if self.role == ProfilesManageDialog.roles.choose:
            self.close()

        msg = self.tr("Profil selectionné: {}").format(self.selected_profile.name)
        if self.current_profile and profile.path == self.current_profile.path:
            msg = "{} {}".format(msg, self.tr("(profil actuel)"))

        self.label.setText(msg)

        # Empèche de supprimer le profil en cours
        if self.current_profile and profile.path == self.current_profile.path:
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
        else:
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)

    def when_create_profile_button_clicked(self):
        profile_edit_dialog = ProfileEditDialog()

        if profile_edit_dialog.exec():
            new_profile_name = profile_edit_dialog.profile_name
            new_profile_picture = profile_edit_dialog.picture_filepath

            # FIXME: Pas plutot déplacer sans directement dans la création
            if new_profile_name and new_profile_name not in self.profiles_list:
                profile = Profiles(name=new_profile_name)
                profile.create()
                profile.set_picture(new_profile_picture)

                self.update_all()

    def when_edit_profile_button_clicked(self):
        profile = self.selected_profile

        profile_edit_dialog = ProfileEditDialog(self.selected_profile)

        if profile_edit_dialog.exec():
            new_profile_name = profile_edit_dialog.profile_name
            new_profile_picture = profile_edit_dialog.picture_filepath
            picture_edited = profile_edit_dialog.profile_picture_edited

            # FIXME: Pas plutot déplacer sans directement dans la rename
            if new_profile_name and new_profile_name not in self.profiles_list:
                if picture_edited:
                    profile.set_picture(new_profile_picture)

                # On ne renome qui si c'est néssésaire
                if new_profile_name != profile.name:
                    profile.rename(new_profile_name)

                self.update_all()

    def when_delete_profile_button_clicked(self):
        choice = QMessageBox.information(None, self.tr("Supression d'un profil"),
                                         self.tr("Etes vous sûr de vouloir supprimer le profil: {} ?".format(
                                             self.selected_profile.name)),
                                         QMessageBox.Yes | QMessageBox.Cancel)

        if choice == QMessageBox.Yes:
            self.selected_profile.delete()
            self.update_all()

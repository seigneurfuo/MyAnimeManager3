import os

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QToolButton, QLabel, QInputDialog, QLineEdit, QGridLayout
from PyQt5.uic import loadUi

from profiles import Profiles


class ProfilesManage(QDialog):
    class roles:
        manage = 0
        choose = 1

    def __init__(self, role, current_profile):
        super(ProfilesManage, self).__init__()

        self.role = role
        self.current_profile = current_profile
        self.profiles_list = None
        self.selected_profile = None

        self.update_profiles_list()

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "profiles_manage.ui"), self)

        if self.profiles_list:
            self.no_profile_found_label.hide()

        if self.role == ProfilesManage.roles.choose:
            self.label.hide()
            self.pushButton_2.hide()

            title = self.tr("Choix d'un profil")

        else:
            title = self.tr("Gestion des profils")

        self.setWindowTitle(title)

        self.fill_data()

    def init_events(self):
        self.pushButton.clicked.connect(self.on_create_profile_button_clicked)
        self.pushButton_2.clicked.connect(self.on_delete_profile_button_clicked)

    def update_profiles_list(self):
        self.selected_profile = None
        self.profiles_list = Profiles.get_profiles_list()

    def clear_data(self):
        # Pour le refresh
        # https://stackoverflow.com/a/13103617
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)

    def fill_data(self):
        # Reset bouton
        if self.role == ProfilesManage.roles.manage:
            self.pushButton_2.setEnabled(False)

        max_btn_on_row = 3
        row_index = 0
        col_index = 0


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
            if index != 0 and index % max_btn_on_row == 0:
                col_index = 0
                row_index += 1

            self.gridLayout.addWidget(btn, row_index, col_index)
            col_index += 1


    def set_profile(self, profile):
        self.selected_profile = profile

        if self.role == ProfilesManage.roles.choose:
            self.close()

        msg = self.tr("Profil selectionné: {}").format(self.selected_profile.name)
        if self.current_profile and profile.path == self.current_profile.path:
            msg = "{} {}".format(msg, self.tr("(profil actuel)"))

        self.label.setText(msg)

        # Empèche de supprimer le profil en cours
        if self.current_profile and profile.path == self.current_profile.path:
            self.pushButton_2.setEnabled(False)
        else:
            self.pushButton_2.setEnabled(True)

    def on_create_profile_button_clicked(self):
        profile_name = QInputDialog.getText(QLineEdit.Normal)

        exit()

        if profile_name: # TODO; Verifier existance profil pour éviter d'avoir deux fois le meme nom
            profile = Profiles()
            profile.create()

            self.update_profiles_list()
            self.clear_data()
            self.fill_data()

    def on_delete_profile_button_clicked(self):
        self.selected_profile.delete()

        self.update_profiles_list()
        self.clear_data()
        self.fill_data()
import os

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QToolButton, QLabel
from PyQt5.uic import loadUi

import profiles_manager


class ProfilesManage(QDialog):
    class roles:
        manage = 0
        choose = 1

    def __init__(self, profiles_list, role):
        super(ProfilesManage, self).__init__()

        self.profiles_list = profiles_list
        self.role = role
        self.selected_profile = None

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "profiles_manage.ui"), self)

        if self.role == ProfilesManage.roles.choose:
            title = self.tr("Choix d'un profil")

        else:
            title = self.tr("Gestion des profils")

        self.setWindowTitle(title)

        self.fill_data()

    def init_events(self):
        self.pushButton_2.clicked.connect(self.on_delete_profile_button_clicked)

    def fill_data(self):

        if self.profiles_list:
            self.no_profile_found_label.hide()

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

            # Ligne suivante si maximal attends
            if index != 0 and index % max_btn_on_row == 0:
                col_index = 0
                row_index += 1

            self.gridLayout.addWidget(btn, row_index, col_index)
            col_index += 1


    def set_profile(self, profile_path):
        self.selected_profile = profile_path

        self.pushButton_2.setEnabled(True)

        if self.role == ProfilesManage.roles.choose:
            self.close()

    def on_delete_profile_button_clicked(self):
        pass
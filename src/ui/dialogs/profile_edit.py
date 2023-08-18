import os

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialogButtonBox, QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog, QDialog


class ProfileEditDialog(QDialog):
    def __init__(self, profile=None):
        super().__init__()

        self.profile = profile
        self.profile_name = None
        self.picture_filepath = None
        self.profile_picture_edited = False

        self.init_ui()
        self.init_events()

        if self.profile:
            self.fill_data()

    def init_ui(self):
        if self.profile:
            title = self.tr("Modification d'un profil")
        else:
            title = self.tr("Création d'un nouveau profil")

        self.setWindowTitle(title)

        layout = QGridLayout()

        self.profile_picture = QLabel()
        self.profile_picture.setFixedSize(QSize(128, 128))
        self.profile_picture.setAlignment(Qt.AlignCenter)
        self.profile_picture.setStyleSheet("border: 1px solid black;")
        pixmap = os.path.join(os.path.dirname(__file__), "../../resources/icons", "user.png")
        self.profile_picture.setPixmap(QPixmap(pixmap))

        self.profile_name_label = QLabel(self.tr("Nom du profil:"))
        self.profile_name_entry = QLineEdit()
        self.profile_picture_browse_button = QPushButton("Choisir une image pour le profil")

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout.addWidget(self.profile_picture, 0, 0)
        layout.addWidget(self.profile_name_label, 0, 1)
        layout.addWidget(self.profile_name_entry, 0, 2)
        layout.addWidget(self.profile_picture_browse_button, 1, 0)
        layout.addWidget(self.button_box, 2, 2)

        self.setLayout(layout)

    def init_events(self):
        self.profile_picture_browse_button.clicked.connect(self.when_profile_picture_browse_clicked)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def fill_data(self):
        self.profile_name_entry.setText(self.profile.name)
        self.picture_filepath = self.profile.get_picture()
        self.update_profile_picture()

    def when_profile_picture_browse_clicked(self):
        picture_file = QFileDialog.getOpenFileName(self, self.tr("Choisir une image pour la photo de profil..."), "",
                                                   "Images (*.png *.jpg)")  # FIXME: Dossier du user

        if picture_file:
            self.picture_filepath = picture_file[0]
            self.profile_picture_edited = True
            self.update_profile_picture()

    def update_profile_picture(self):
        pixmap = QPixmap(self.picture_filepath)
        resized_pixmap = pixmap.scaled(self.profile_picture.height(), self.profile_picture.width())
        self.profile_picture.setPixmap(resized_pixmap)

    def accept(self):
        super().accept()

        profile_name = self.profile_name_entry.text().strip()

        # TODO: Améliorer ça ?
        characters = (".", "/", "\\")
        for character in characters:
            profile_name = profile_name.replace(character, "")

        self.profile_name = profile_name

    def reject(self):
        super().reject()

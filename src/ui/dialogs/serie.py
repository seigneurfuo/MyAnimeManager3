import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QFileDialog, QCompleter
from PyQt6.uic import loadUi

from common import file_to_blob
from utils import anime_titles_autocomplete


class SerieDialog(QDialog):
    def __init__(self, parent, serie) -> None:
        super().__init__(parent=parent)

        self.parent = parent
        self.serie = serie
        self.picture_filepath = None

        self.autocomplete_loaded = False

        self.init_ui()
        self.init_events()

    def init_ui(self) -> None:
        loadUi(os.path.join(os.path.dirname(__file__), "serie.ui"), self)

        # Si création
        if self.serie.id:
            self.setWindowTitle(self.serie.name)
            self.fill_data()

    def init_events(self) -> None:
        self.choose_path_button.clicked.connect(self.choose_path)
        self.choose_picture_button.clicked.connect(self.choose_picture)

        if (self.parent.parent.parent.settings["anime_titles_autocomplete"]):
            self.lineEdit_2.cursorPositionChanged.connect(self.fill_autocomplete)

    def fill_data(self) -> None:
        self.spinBox.setValue(self.serie.sort_id)
        self.lineEdit_2.setText(self.serie.name)
        self.lineEdit_3.setText(self.serie.path)

    def fill_autocomplete(self) -> None:
        # Complétion automatique
        if self.autocomplete_loaded:
            return

        anime_titles_autocomplete(self.lineEdit_2)
        self.autocomplete_loaded = True

    def choose_path(self) -> None:
        """Fonction qui permet à l'utilisateur de choisir le dossier de la série"""
        path = self.serie.path if self.serie.path and os.path.isdir(self.serie.path) else ""
        folder_name = QFileDialog.getExistingDirectory(self, self.tr("Choisir le dossier de la série"), path)

        # Si un dossier à été sélectionné
        if folder_name:
            # Application du texte sur le widget line edit
            self.lineEdit_3.setText(folder_name)

    def choose_picture(self) -> None:
        path = self.serie.path if self.serie.path and os.path.isdir(self.serie.path) else ""
        self.picture_filepath, filter = QFileDialog.getOpenFileName(self, self.tr("Choisir une image"), path,
                                                                    "Fichiers images (*.jpg *.jpeg *.png *.gif);;Tous les fichiers (*)")

    def save_data(self) -> None:
        self.serie.sort_id = self.spinBox.value()
        self.serie.name = self.lineEdit_2.text().strip()
        self.serie.path = self.lineEdit_3.text()

        if self.picture_filepath:
            self.serie.picture = file_to_blob(self.picture_filepath)

        self.serie.save()

    def accept(self) -> None:
        self.save_data()
        super().accept()

    def reject(self) -> None:
        super().reject()

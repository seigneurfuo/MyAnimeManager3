import os

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.uic import loadUi


class SeriesDialog(QDialog):
    def __init__(self, serie):
        super(SeriesDialog, self).__init__()

        self.serie = serie

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), 'series.ui'), self)

        if self.serie.id:
            self.fill_data()

    def init_events(self):
        self.choose_path_button.clicked.connect(self.choose_path)

    def fill_data(self):
        self.setWindowTitle(self.serie.name)  # Titre
        self.spinBox.setValue(self.serie.sort_id)
        self.lineEdit_2.setText(self.serie.name)  #
        self.lineEdit_3.setText(self.serie.path) # Chemin

    def choose_path(self):
        """Fonction qui permet à l'utilisateur de choisir le dossier de la série"""

        folder_name = QFileDialog.getExistingDirectory(self, "Choisir le dossier de la série")

        # Si un dossier à été sélectionné
        if folder_name:
            # Application du texte sur le widget line edit
            self.lineEdit_3.setText(folder_name)


    def accept(self):
        self.serie.name = self.lineEdit_2.text()
        self.serie.sort_id = self.spinBox.value()
        # TODO: Chemin de la série
        self.serie.path = self.lineEdit_3.text()
        self.serie.save()

        super(SeriesDialog, self).accept()

    def reject(self):
        super(SeriesDialog, self).reject()

import os

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.uic import loadUi


class SerieDialog(QDialog):
    def __init__(self, serie):
        super(SerieDialog, self).__init__()

        self.serie = serie

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "serie.ui"), self)

        # Si création
        if self.serie.id:
            self.setWindowTitle(self.serie.name)
            self.fill_data()

    def init_events(self):
        self.choose_path_button.clicked.connect(self.choose_path)

    def fill_data(self):
        self.spinBox.setValue(self.serie.sort_id)
        self.lineEdit_2.setText(self.serie.name)
        self.lineEdit_3.setText(self.serie.path)

    def choose_path(self):
        """Fonction qui permet à l'utilisateur de choisir le dossier de la série"""

        folder_name = QFileDialog.getExistingDirectory(self, self.tr("Choisir le dossier de la série"))

        # Si un dossier à été sélectionné
        if folder_name:
            # Application du texte sur le widget line edit
            self.lineEdit_3.setText(folder_name)

    def save_data(self):
        self.serie.sort_id = self.spinBox.value()
        self.serie.name = self.lineEdit_2.text()
        self.serie.path = self.lineEdit_3.text()

        self.serie.save()

    def accept(self):
        self.save_data()
        super(SerieDialog, self).accept()

    def reject(self):
        super(SerieDialog, self).reject()

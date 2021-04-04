import os

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.uic import loadUi


class SeriesDialog(QDialog):
    def __init__(self, serie):
        super(SeriesDialog, self).__init__()

        #self.parent = parent
        self.serie = serie

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(QDir.currentPath(), 'ui/dialogs/series.ui'), self)

        #if self.serie:
            #self.seriemodal.setWindowTitle(self.serie.name)

        # Rends la fenetre principale inacessible tant que celle-ci est ouverte
        self.setWindowModality(Qt.ApplicationModal)


    def init_events(self):
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.save)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.cancel)


    def save(self):
        self.serie.name = self.lineEdit_2.text()
        self.serie.sort_id = self.spinBox.value()

        print(self.serie)

    def cancel(self):
        print("bite")
        self.hide()

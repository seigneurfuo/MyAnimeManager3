import os

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.uic import loadUi


class SeriesDialog(QDialog):
    def __init__(self, serie, app_dir):
        super(SeriesDialog, self).__init__()

        self.serie = serie
        self.app_dir = app_dir

        self.init_ui()
        self.init_events()

        if self.serie.id:
            self.fill_data()

    def init_ui(self):
        loadUi(os.path.join(self.app_dir, 'ui/dialogs/series.ui'), self)

    def init_events(self):
        pass

    def fill_data(self):
        self.setWindowTitle(self.serie.name) # Titre
        self.spinBox.setValue(self.serie.sort_id)
        self.lineEdit_2.setText(self.serie.name) #
        #self.lineEdit_3.setText(self.serie.) # Chemin

    def accept(self):
        self.serie.name = self.lineEdit_2.text()
        self.serie.sort_id = self.spinBox.value()
        self.serie.save()

        super(SeriesDialog, self).accept()


    def reject(self):
        super(SeriesDialog, self).reject()
from PyQt5.QtWidgets import QCalendarWidget


class CustomCalendar(QCalendarWidget):
    """
    Une classe personalisée qui permet d'étendre les possibilités du calendrier
    Found on: https://stackoverflow.com/questions/19083140/custom-calendar-cell-in-pyqt
    """

    def __init__(self, parent=None):
        QCalendarWidget.__init__(self, parent)
        self.cell_background_color = None
        self.dates = []

    def set_cells_background_color(self, color):
        """
        Une méthode qui permet de choisir la couleur de fond d'une cellule

        :param color:
        :return:
        """

        self.cell_background_color = color

    def paintCell(self, painter, rect, date, **kwargs):
        QCalendarWidget.paintCell(self, painter, rect, date, **kwargs)

        # Si une couleur à été choisi pour l'arrière plan des cellules, alors on l'applique
        if self.cell_background_color:
            if date in self.dates:
                painter.fillRect(rect, self.cell_background_color)

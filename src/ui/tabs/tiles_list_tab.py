#!/usr/bin/python3
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QToolButton
from PyQt6.uic import loadUi

import os
import io

import peewee
from database import Series, Seasons, Planning

import utils


class TilesListTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.max_btn_on_row = 3

        self.init_ui()
        self.init_events()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "tiles_list_tab.ui"), self)

    def init_events(self):
        self.comboBox.currentIndexChanged.connect(self.when_combobox_current_index_changed)

    def when_combobox_current_index_changed(self):
        self.max_btn_on_row = int(self.comboBox.currentText())
        self.fill_data()

    def when_visible(self):
        self.fill_data()

    def fill_data(self):
        # Nettoyage des éléments existants
        for x in reversed(range(self.gridLayout_2.count())):
            self.gridLayout_2.itemAt(x).widget().deleteLater()

        row_index = 0
        col_index = 0

        series = Series().select().where(Series.is_deleted == 0).order_by(Series.sort_id)

        for index, serie in enumerate(series):
            text = f"{serie.sort_id:03d} - {serie.name}"

            btn = QToolButton()
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setText(text)
            btn.setFixedSize(128, 128)
            btn.setToolTip(btn.text())

            if serie.picture:
                with io.BytesIO(serie.picture) as picture_data:
                    pixmap = QPixmap.fromImage(QImage.fromData(picture_data.read()))
                btn.setIcon(QIcon(pixmap))

            btn.setIconSize(QSize(int(btn.height() - 32), int(btn.width() - 32)))
            #btn.clicked.connect(lambda lamdba, profile=profile: self.set_profile(profile))

            # Ligne suivante si maximal attends
            if index != 0 and index % self.max_btn_on_row == 0:
                col_index = 0
                row_index += 1

            self.gridLayout_2.addWidget(btn, row_index, col_index)
            col_index += 1

    def open_serie(self):
        pass
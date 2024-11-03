#!/usr/bin/python3

import os

import utils

from database import Series, Seasons, Planning, SeasonsTypes

from ui.dialogs.serie import SerieDialog
from ui.dialogs.season import SeasonDialog

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QToolButton
from PyQt6.uic import loadUi


class TilesListTab(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.parent = parent

        self.max_btn_on_row = 3
        self.icon_size = 256

        self.init_ui()
        self.init_events()

    def init_ui(self) -> None:
        loadUi(os.path.join(os.path.dirname(__file__), "tiles_list_tab.ui"), self)

        self.comboBox.setCurrentText(str(self.max_btn_on_row))
        self.comboBox_2.setCurrentText(str(self.icon_size))

    def init_events(self) -> None:
        self.comboBox.currentIndexChanged.connect(self.when_combobox_current_index_changed)
        self.comboBox_2.currentIndexChanged.connect(self.when_combobox2_current_index_changed)
        self.comboBox_3.currentIndexChanged.connect(self.when_combobox3_current_index_changed)

        self.checkBox.checkStateChanged.connect(self.fill_data)

    def when_combobox_current_index_changed(self) -> None:
        self.max_btn_on_row = int(self.comboBox.currentText())
        self.fill_data()

    def when_combobox2_current_index_changed(self) -> None:
        self.icon_size = int(self.comboBox_2.currentText())
        self.fill_data()

    def when_combobox3_current_index_changed(self) -> None:
        self.fill_data()

    def when_visible(self) -> None:
        self.fill_data()

    def fill_data(self) -> None:
        current_type_index = self.comboBox_3.currentIndex() # 0 -> Saisons, 1 -> Séries
        current_type_name = "season" if current_type_index == 0 else "serie"

        # Nettoyage des éléments existants
        for x in reversed(range(self.gridLayout_2.count())):
            self.gridLayout_2.itemAt(x).widget().deleteLater()

        row_index = 0
        col_index = 0
        total_bytes = 0

        filter_coverless = self.checkBox.isChecked()

        # Chargement des données depuis la BDD
        if current_type_index == 0:
            data = Seasons().select().where(Seasons.is_deleted == 0).join(Series).order_by(Series.sort_id, Seasons.sort_id)
        else:
            data = Series().select().where(Series.is_deleted == 0).order_by(Series.sort_id)

        for row in data:
            cover_path = utils.load_cover(self.parent.parent.profile.path, current_type_name, row.id)

            # Si on n'a pas de cover et qu'on n'affiche que les séries avec cover, alors on l'ignore
            if not cover_path and filter_coverless:
                continue

            text = f"{row.sort_id:03d} - {row.name}"

            btn = QToolButton()
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setText(text)
            btn.setFixedSize(self.icon_size, self.icon_size)
            btn.setToolTip(btn.text())

            if current_type_index == 0:
                btn.clicked.connect(lambda lamdba, row=row: self.open_season(row))
            else:
                btn.clicked.connect(lambda lamdba, row=row: self.open_serie(row))

            if cover_path:
                pixmap = QPixmap.fromImage(QImage(cover_path))
                btn.setIcon(QIcon(pixmap))

            btn.setIconSize(QSize(int(btn.height() - 32), int(btn.width() - 32)))
            #btn.clicked.connect(lambda lamdba, profile=profile: self.set_profile(profile))

            # Ligne suivante si maximal attends
            if col_index != 0 and col_index % self.max_btn_on_row == 0:
                col_index = 0
                row_index += 1

            self.gridLayout_2.addWidget(btn, row_index, col_index)
            col_index += 1

        # Total du nombre d'éléments
        total_megabytes = int(total_bytes / 1024 / 1024)
        self.label.setText(self.tr(f"Nombre d'éléments: {len(data)}: Taille totale de {total_megabytes}Mo"))


    def open_serie(self, serie) -> None:
        series_dialog = SerieDialog(self, serie)

        if series_dialog.exec():
            self.fill_data()

    def open_season(self, season):
        seasons_types = SeasonsTypes().select()
        season_dialog = SeasonDialog(self, season, serie=None, seasons_types=seasons_types)

        if season_dialog.exec():
            self.fill_data()
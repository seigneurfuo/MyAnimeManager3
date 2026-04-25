#!/usr/bin/python3
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QToolButton, QLabel, QVBoxLayout
from PyQt6.QtCore import pyqtSignal


class CustomIconButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, text, icon_path=None, icon_size=100, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Icon button
        self.btn = QToolButton()
        self.btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.btn.setFixedSize(icon_size - 20, icon_size - 20)

        if icon_path:
            pixmap = QPixmap.fromImage(QImage(icon_path))
            self.btn.setIcon(QIcon(pixmap))
            self.btn.setIconSize(QSize(icon_size - 52, icon_size - 52))

        self.btn.clicked.connect(self.clicked.emit)

        # Text label with word wrap
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setMaximumWidth(icon_size)

        layout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.setMaximumWidth(icon_size)

    def setText(self, text):
        self.label.setText(text)

    def setToolTip(self, text):
        self.btn.setToolTip(text)

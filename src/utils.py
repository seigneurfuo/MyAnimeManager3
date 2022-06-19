#!/bin/env python3

from datetime import datetime, timedelta

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMessageBox


def duration_calculation(episodes_count, duration, pause_every, pause_duration, start):
    """

    :return:
    """

    ret_list = []
    is_pause = True if pause_every > 0 and pause_duration > 0 else False

    start = datetime.strptime(start, "%H:%M")

    for episode_num in range(episodes_count):
        end = start + timedelta(minutes=duration)
        row = "{:02d} - {:02d}:{:02d} -> {:02d}:{:02d}".format(episode_num + 1, start.hour, start.minute, end.hour,
                                                               end.minute)

        ret_list.append(row)

        # Décale la plage
        start = end

        # Gestion des pauses - Effectue une pause si episode_num est bien un multiple de pause_every
        if is_pause and (episode_num + 1) % pause_every == 0:
            end = start + timedelta(minutes=pause_duration)
            row = "Pause - {:02d}:{:02d} -> {:02d}:{:02d}".format(start.hour, start.minute, end.hour, end.minute)
            ret_list.append(row)

            # Décale la plage
            start = end

    return ret_list


def export_qtablewidget(qtablewidget):
    for row_index in range(qtablewidget.rowCount()):
        for col_index in range(qtablewidget.columnCount()):
            item = qtablewidget.item(row_index, col_index).text()


def set_cursor_on_center(qwidget):
    QCursor().setPos(qwidget.mapToGlobal(qwidget.rect().center()))


def tutorial(parent_widget):
    msg = """Bienvenue dans ce tutoriel !
Ce tutoriel va brièvement présenter les différents écrans de l'application.
"""

    QMessageBox.information(None, "Tutoriel", msg, QMessageBox.Ok)

    tabs = ((1, "Voici l'écran dans lequel vous aller définir les séries à voir"),
            2, "Ecran des outils")
    for tab in tabs:
        # Message de bienvenue
        parent_widget.tabWidget.setCurrentIndex(tab[0])  # Onglet de la liste des animé
        parent_widget.tabWidget.setToolTip(tab[1])
        set_cursor_on_center(parent_widget.tabWidget)
        # btn = parent_widget.tab2
        # btn.setStyleSheet("border: 0.5em solid red;")

#!/bin/env python3
from database import Planning

from ui.dialogs.view_history import ViewHistory

import peewee


def show_watch_history_dialog(season_id):
    # Utilisé pour faire un group concat....
    episodes = (peewee.fn.GROUP_CONCAT(Planning.episode).python_value(
        lambda s: ", ".join([str(i) for i in (s or '').split(',') if i])))
    data = Planning().select(Planning.date, Planning.season, episodes.alias('episodes')) \
        .where(Planning.season == season_id) \
        .group_by(Planning.date).order_by(Planning.date, Planning.episode)

    dialog = ViewHistory(season_id, data)
    dialog.exec_()

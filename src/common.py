#!/bin/env python3

from database import Planning, Seasons
import peewee

from ui.dialogs.view_history import ViewHistoryDialog

def display_view_history_dialog(season_id):
    # Utilisé pour faire un group concat...
    season = Seasons.get(season_id)

    episodes = (peewee.fn.GROUP_CONCAT(Planning.episode).python_value(
        lambda s: ", ".join([str(i) for i in (s or '').split(',') if i])))

    serie_episodes = Planning().select(Planning.date, Planning.season, episodes.alias('episodes')) \
        .where(Planning.serie == season.serie.id) \
        .group_by(Planning.date).order_by(Planning.date, Planning.episode)

    season_episodes = Planning().select(Planning.date, Planning.season, episodes.alias('episodes')) \
        .where(Planning.season == season.id) \
        .group_by(Planning.date).order_by(Planning.date, Planning.episode)

    dialog = ViewHistoryDialog(season, serie_episodes, season_episodes)
    dialog.exec_()

def display_friends_dialog():
    pass
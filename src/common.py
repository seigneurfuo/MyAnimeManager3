from database import Planning

from ui.dialogs.view_history import ViewHistory


def show_view_history_dialog(season_id):
    # TODO: Group_CONCAT ? -> episodes sur une ligne par date ?
    data = Planning.select().where(Planning.season == season_id).order_by(Planning.date, Planning.episode)
    dialog = ViewHistory(season_id, data)
    dialog.exec_()

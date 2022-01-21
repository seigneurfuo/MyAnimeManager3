from datetime import datetime, timedelta


def duration_calculation(episodesnumber, episodeslenght, pause_every, pause_duration, start):
    """

    :return:
    """

    ret_list = []
    is_pause = True if pause_every > 0 and pause_duration > 0 else False

    start = datetime.strptime(start, "%H:%M")

    for episode_num in range(episodesnumber):
        end = start + timedelta(minutes=episodeslenght)
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


def open_folder(path):
    """Ouvre un explorateur de fichiers à l'adresse indiquée en argument"""

    import platform

    try:
        if platform.system() == "Windows":
            from os import startfile
            startfile(path)

        elif platform.system() == "Darwin":
            from subprocess import Popen
            Popen(["open", path])

        else:
            from subprocess import Popen
            Popen(["xdg-open", path])

    except:
        return None

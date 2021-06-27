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
        row = "{:02d} - {:02d}:{:02d} -> {:02d}:{:02d}".format(episode_num + 1, start.hour, start.minute, end.hour, end.minute)

        ret_list.append(row)

        # Décale la plage
        start = end

        # Gestion des pauses
        if is_pause:
                # Effectue une pause si episode_num est bien un multiple de pause_every
            if (episode_num +1) % pause_every == 0:
                end = start + timedelta(minutes=pause_duration)
                row = "    Pause - {:02d}:{:02d} -> {:02d}:{:02d}".format(start.hour, start.minute, end.hour, end.minute)
                ret_list.append(row)

                # Décale la plage
                start = end


    return ret_list

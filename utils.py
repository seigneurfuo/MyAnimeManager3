from datetime import datetime, timedelta


def duration_calculation(episodesnumber, episodeslenght, start):
    """

    :return:
    """

    ret_list = []
    start = datetime.strptime(start, "%H:%M")

    for x in range(episodesnumber):
        end = start + timedelta(minutes=episodeslenght)
        row = "{:02d} - {:02d}:{:02d} -> {:02d}:{:02d}".format(x + 1, start.hour, start.minute, end.hour, end.minute)
        ret_list.append(row)

        # Décale la plage
        start = end

    return ret_list

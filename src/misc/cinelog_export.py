# A simple Cinelog CSV output script

import sys
import os
import csv

from datetime import datetime

# ----- Custom -----
sys.path.append("..")
from database import database, Series, Seasons


def main():
    database_path = "/home/seigneurfuo/.myanimemanager3/profiles/Profil principal/database.sqlite3"
    database.init(database_path)

    # id§movie_id§title§overview§year§poster_path§rating§release_date§review§review_date§max_rating§tags

    output_directory = os.path.dirname(__file__)

    #date = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    date = ""
    output_directory = output_filepath = os.path.join(output_directory, f"cinelog-import_series{date}.csv")

    with open(output_filepath, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="§")

        # Entetes
        headers = [
            "id", "movie_id", "title", "overview", "year", "poster_path", "rating", "release_date", "review", "review_date",
            "max_rating", "tags"
        ]
        csv_writer.writerow(headers)

        rows = Seasons.select().where(Seasons.is_deleted == 0)
        for row in rows:
            data = [row.sort_id, row.id, row.name, "", row.year, "", "", row.year, "", ""]
            csv_writer.writerow(data)

        print(f"Fichier: {output_filepath}")


if __name__ == "__main__":
    main()
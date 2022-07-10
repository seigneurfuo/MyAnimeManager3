#!/bin/env python3

import csv
from datetime import datetime
import os
from pathlib import Path

import database


def load_profile():
    database_path = "database.sqlite3"

    # Creation du profil
    app_data_folder = os.path.join(Path.home(), ".myanimemanager3")

    if not os.path.exists(app_data_folder):
        # Création du dossier ./profile/covers qui créer en meme temps le dossier parent ./profile
        os.makedirs(app_data_folder)

    database_path = os.path.join(app_data_folder, database_path)
    print("Database path:", database_path)
    database.database.init(database_path)

    return app_data_folder


# TODO: Asynchrone QThread
def export_planning_to_csv(output_directory):
    app_data_folder = load_profile()

    rows = database.Planning.select().order_by(database.Planning.date, database.Planning.id)

    # Création du dossier exports
    output_directory = os.path.join(app_data_folder, "exports")
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    date = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    output_filepath = os.path.join(output_directory, "{}-planning.csv".format(date))

    with open(output_filepath, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")

        # Entetes
        csv_writer.writerow(["Date", "(Saga / Série)", "Saison", "Episode"])

        for row in rows:
            csv_writer.writerow([row.date, row.serie.name, row.season.name, row.episode])

        print("Fichier: {}".format(output_filepath))

    return output_filepath


if __name__ == "__main__":
    export_planning_to_csv("")

#!/usr/bin/python3

import csv
from datetime import datetime
import os
from pathlib import Path

import database


# TODO: Asynchrone QThread
def export_planning_to_csv(app_data_folder):
    # Création du dossier exports
    output_directory = os.path.join(app_data_folder, "exports")
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    date = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    output_filepath = os.path.join(output_directory, f"planning-{date}.csv")

    with open(output_filepath, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")

        # Entetes
        csv_writer.writerow(["Date", "(Saga / Série)", "Saison", "Episode"])

        rows = database.Planning.select().order_by(database.Planning.date, database.Planning.id)
        for row in rows:
            csv_writer.writerow([row.date, row.serie.name, row.season.name, row.episode])

        print(f"Fichier: {output_filepath}")

    return output_filepath

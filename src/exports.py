#!/usr/bin/python3

import csv
from datetime import datetime
import os
from pathlib import Path

import database


# TODO: Asynchrone QThread
def export_planning_to_csv(app_data_folder, friends_enabled) -> str:
    # Création du dossier exports
    output_directory = os.path.join(app_data_folder, "exports")
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    date = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    output_filepath = os.path.join(output_directory, f"planning-{date}.csv")

    with open(output_filepath, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")

        # Entetes
        headers = ["Date", "(Saga / Série)", "Saison", "Episode"]
        if friends_enabled:
            headers.append("Amis")

        csv_writer.writerow(headers)

        rows = database.Planning.select().order_by(database.Planning.date, database.Planning.id)

        # TODO: Export des amis dans la liste du planning si activé

        for row in rows:
            data = [row.date, row.serie.name, row.season.name, row.episode]

            if friends_enabled:
                friends = [friend_planning.friend.name for friend_planning in row.friends]
                data.append(", ".join(friends))

            csv_writer.writerow(data)

        print(f"Fichier: {output_filepath}")

    return output_filepath

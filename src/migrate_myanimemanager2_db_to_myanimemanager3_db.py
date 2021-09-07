# python pwiz.py --preserve-order --engine sqlite "/home/seigneurfuo/.myanimemanager2/database.sqlite3" > database_myanimemanager_2.py
import os
import time

from pathlib import Path

import database_myanimemanager_2 as mamdb2
import database as mamdb3


MYANIMEMANAGER_2_DATABASE = os.path.join(Path.home(), ".myanimemanager2/database.sqlite3")
MYANIMEMANAGER_3_DATABASE = os.path.join(Path.home(), ".myanimemanager3/database.sqlite3")

# Garde la correspondance entre les anciens ID et les nouveaux ID
id_series = {}
id_seasons = {}

def migration_series():
    series = mamdb2.Serie().select()
    for index, serie in enumerate(series):
        msg = "Série: {0} / {1} -> {2}".format(index + 1, len(series), serie.serie_title)
        print(msg)

        # On migre chaque information
        new_serie = mamdb3.Series()
        new_serie.sort_id = serie.serie_sort_id
        new_serie.name = serie.serie_title

        # TODO:
        #new_serie.path = serie.serie_path
        #new_serie.liked = serie.serie_liked
        new_serie.is_deleted = 0
        new_serie.save()

        # On récupère l'identifiant qui vien d'etre crée afin de garder une trace des anciens / nouveaux ID
        id_series[serie.serie_id] = new_serie.id

def populate_new_table_seasons_type():
    seasons_types = [("Saison", ""), ("OAV / OVA", "")]
    for index, seasons_type in enumerate(seasons_types):
        msg = "Type de Saison: {0} / {1} -> {2}".format(index + 1, len(seasons_types), seasons_type[0])
        print(msg)

        new_season_type = mamdb3.SeasonsTypes()
        new_season_type.name = seasons_type[0]
        new_season_type.save()

def migration_seasons():
    seasons = mamdb2.Season().select()
    for index, season in enumerate(seasons):
        msg = "Saison: {0} / {1} -> {2}".format(index + 1, len(seasons), season.season_title)
        print(msg)

        # On migre chaque information
        new_season = mamdb3.Seasons()
        new_season.sort_id = season.season_sort_id
        new_season.name = season.season_title
        new_season.type = 1 # Saison

        # Migration de l'id de la série ratachée
        old_serie_id = season.season_fk_serie.serie_id
        new_serie_id = id_series[old_serie_id]
        new_season.serie = new_serie_id # On récupère le nouvel ID de le série

        # TODO:
        #Date + champ sur comment est enregistré la date

        new_season.is_deleted = 0
        new_season.save()

        # On récupère l'identifiant qui viens d'etre créer afin de garder une trace des anciens / nouveaux ID
        id_series[season.season_id] = new_season.id


def migration_planning():
    pass


def migration():
    # Supression de la base de données sur MyAnimeManager3
    print("Supression de {}...".format(MYANIMEMANAGER_3_DATABASE))
    if os.path.exists(MYANIMEMANAGER_3_DATABASE):
        os.remove(MYANIMEMANAGER_3_DATABASE)

    time.sleep(1)

    # Chargemet des BDD
    mamdb2.database.init(MYANIMEMANAGER_2_DATABASE)
    mamdb3.database.init(MYANIMEMANAGER_3_DATABASE)

    # Création des tables sur la base de données mam3
    tables = [mamdb3.Series, mamdb3.Seasons, mamdb3.SeasonsTypes, mamdb3.Planning, mamdb3.Studios, mamdb3.Tags,
              mamdb3.TagsGroups]
    mamdb3.database.create_tables(tables)

    # Migration de chaque table
    migration_series()
    populate_new_table_seasons_type()
    migration_seasons()
    migration_planning()

    mamdb3.database.commit()
    mamdb3.database.close()


def main():
    print(MYANIMEMANAGER_2_DATABASE, "->", MYANIMEMANAGER_3_DATABASE)

    msg = "Attention, cela va supprimer toutes les données de {}\nY/N: ".format(MYANIMEMANAGER_3_DATABASE)
    # ask = input(msg).upper()
    # if ask != "Y":
    #     print("-> Sortie")
    #     exit(0)

    migration()


main()
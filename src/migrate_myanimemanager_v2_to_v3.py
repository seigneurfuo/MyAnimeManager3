#!/bin/env python3

# python pwiz.py --preserve-order --engine sqlite "/home/seigneurfuo/.myanimemanager2/database.sqlite3" > database_myanimemanager_2.py
import os

from pathlib import Path

import database_myanimemanager_2 as mamdb2
import database as mamdb3

MYANIMEMANAGER_2_DATABASE = os.path.join(Path.home(), ".myanimemanager2/database.sqlite3")
MYANIMEMANAGER_3_DATABASE = os.path.join(Path.home(), ".myanimemanager3/database.sqlite3")

# Garde la correspondance entre les anciens ID et les nouveaux ID
series_id_list = {}
seasons_id_list = {}


@mamdb3.database.atomic()
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
        new_serie.path = serie.serie_path
        # new_serie.liked = serie.serie_liked
        new_serie.is_deleted = False
        new_serie.save()

        # On récupère l'identifiant qui vien d'etre crée afin de garder une trace des anciens / nouveaux ID
        series_id_list[serie.serie_id] = new_serie.id


@mamdb3.database.atomic()
def populate_new_table_seasons_types():
    seasons_types = [("Saison", ""), ("OAV / OVA", "")]
    for index, seasons_type in enumerate(seasons_types):
        msg = "Type de Saison: {0} / {1} -> {2}".format(index + 1, len(seasons_types), seasons_type[0])
        print(msg)

        new_season_type = mamdb3.SeasonsTypes()
        new_season_type.name = seasons_type[0]
        new_season_type.save()


@mamdb3.database.atomic()
def populate_new_table_seasons_states():
    pass


@mamdb3.database.atomic()
def migration_seasons():
    seasons = mamdb2.Season().select()
    for index, season in enumerate(seasons):
        msg = "Saison: {0} / {1} -> {2}".format(index + 1, len(seasons), season.season_title)
        print(msg)

        # On migre chaque information
        new_season = mamdb3.Seasons()
        new_season.sort_id = season.season_sort_id
        new_season.name = season.season_title

        # TODO: Date + champ sur comment est enregistré la date
        if len(str(season.season_release_year)) == 4:
            new_season.year = season.season_release_year
        else:
            new_season.year = None

        new_season.type = 1  # Saison
        # TODO: Studio ?
        new_season.episodes = season.season_episodes
        new_season.watched_episodes = season.season_watched_episodes
        new_season.view_count = season.season_view_count
        new_season.state = season.season_state
        new_season.description = season.season_notes
        # TODO: new_season.favorite =

        # Migration de l'id de la série ratachée
        old_serie_id = season.season_fk_serie.serie_id
        new_season_id = series_id_list[old_serie_id]
        new_season.serie = new_season_id  # On récupère le nouvel ID de le série

        new_season.is_deleted = False
        new_season.save()

        # On récupère l'identifiant qui viens d'etre créer afin de garder une trace des anciens / nouveaux ID
        seasons_id_list[season.season_id] = new_season.id


@mamdb3.database.atomic()
def migration_planning():
    planning = mamdb2.Planning().select()
    for index, day in enumerate(planning):
        msg = "Planning: {0} / {1} -> {2}".format(index + 1, len(planning), day.planning_date)
        print(msg)

        new_day = mamdb3.Planning()
        new_day.date = day.planning_date
        new_day.episode = day.planning_episode_id

        # Migration de l'id de la série ratachée
        old_serie_id = day.planning_fk_serie.serie_id
        new_serie_id = series_id_list[old_serie_id]
        new_day.serie = new_serie_id  # On récupère le nouvel ID de le série

        # Migration de l'id de la saison ratachée
        try:
            old_season_id = day.planning_fk_season.season_id
            new_season_id = seasons_id_list[old_season_id]
            new_day.season = new_season_id  # On récupère le nouvel ID de le série

            new_day.save()
        except:
            print("Erreur -> avec l'ID {}".format(day.planning_id))


def migration():
    # Supression de la base de données sur MyAnimeManager3
    print("Supression de {}...".format(MYANIMEMANAGER_3_DATABASE))
    if os.path.exists(MYANIMEMANAGER_3_DATABASE):
        os.remove(MYANIMEMANAGER_3_DATABASE)

    # Chargemet des BDD
    mamdb2.database.init(MYANIMEMANAGER_2_DATABASE)
    mamdb3.database.init(MYANIMEMANAGER_3_DATABASE)

    # Création des tables sur la base de données mam3
    print("Création des tables ...")
    tables = [mamdb3.Series, mamdb3.Seasons, mamdb3.SeasonsTypes, mamdb3.Planning, mamdb3.Studios, mamdb3.Tags,
              mamdb3.TagsGroups]
    mamdb3.database.create_tables(tables)

    # Migration de chaque table
    print("Remplissage des tables")
    migration_series()
    populate_new_table_seasons_types()
    migration_seasons()
    migration_planning()

    mamdb3.database.commit()
    mamdb3.database.close()


def main():
    print(MYANIMEMANAGER_2_DATABASE, "->", MYANIMEMANAGER_3_DATABASE)

    migration()

main()

import os

import database

from playhouse.migrate import SqliteMigrator, migrate
from playhouse.sqlite_ext import JSONField

DATABASE_NAME = "database.sqlite3"


def load_or_create_database(profile) -> str:
    database_path = os.path.join(profile.path, DATABASE_NAME)
    print("Database path:", database_path)

    # Génération des tables
    database.database.init(database_path)

    tables = [database.Series, database.Seasons, database.SeasonsTypes, database.Planning, database.Friends,
              database.FriendsPlanning]
    database.database.create_tables(tables)

    populate_tables()

    # Migrations
    migrations()

    return database_path


def migrations() -> None:
    # http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations

    migrator = SqliteMigrator(database.database)
    seasons_fields = [field.name for field in database.database.get_columns("Seasons")]

    # Migration 1
    if not "custom_data" in seasons_fields:
        migrate(migrator.add_column("Seasons", "custom_data", JSONField(default="")))

    # Migration 2: Supression du champ picture pour les images des séries
    #cursor = database.database.execute_sql("ALTER TABLE Series DROP COLUMN picture;")
    #cursor.fetchone()


def populate_tables() -> None:
    populate_seasons_types()

    database.database.commit()


# FIXME: Pas propre, trouver comment corrriger ça
def populate_seasons_types() -> None:
    seasons_types = [
        {"sort_id": 1, "name": "Episodes"},
        {"sort_id": 2, "name": "Film"},
        {"sort_id": 3, "name": "OAV / OVA"},
        {"sort_id": 4, "name": "Specials / Bonus"},
    ]

    for index, seasons_type_data in enumerate(seasons_types):
        season_type_id = index + 1
        season_type = database.SeasonsTypes.get_or_none(database.SeasonsTypes.id == season_type_id)

        # Si existe pas, on crée, sinon on fait une MAJ
        if not season_type:
            season_type = database.SeasonsTypes()

        season_type.name = seasons_type_data["name"]
        season_type.sort_id = seasons_type_data["sort_id"]
        season_type.save()

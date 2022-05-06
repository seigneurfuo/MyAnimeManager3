import os
import shutil
from datetime import datetime


class DBBackupsManager:
    def __init__(self, parent):
        self.parent = parent
        self.backups_limit = self.parent.parent.default_settings["backups_limit"]
        self.database_pattern = "-database.sqlite3"
        self.backups_foldername = "db-backups"
        self.backups_folderpath = os.path.join(self.parent.parent.profile_path, self.backups_foldername)

    def _create_backup_folder(self):
        if not os.path.isdir(self.backups_folderpath):
            os.makedirs(self.backups_folderpath)

    def get_dbs_list(self):
        self._create_backup_folder()

        databases_backups = [
            os.path.join(self.backups_folderpath, filename) \
            for filename in os.listdir(self.backups_folderpath) \
            if os.path.isfile(os.path.join(self.backups_folderpath, filename)) \
               and os.path.join(self.backups_folderpath, filename).endswith(self.database_pattern)
        ]

        return sorted(databases_backups)

    def _remove_old_backups(self):
        backups = self.get_dbs_list()
        if len(backups) >= self.backups_limit:
            # TODO: Supression de la version la plus vieille
            print("Supression des vieilles sauvegardes")

            nb_backups_to_delete = len(backups) - 10
            backups_to_remove = backups[:nb_backups_to_delete]

            for backup in backups_to_remove:
                if os.path.isfile(backup):
                    print("    ", backup)
                    os.remove(backup)

    def backup_current_database(self, automatic=True):
        self._create_backup_folder()

        date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        src = self.parent.parent.database_path
        database_backups_folderpath = os.path.join(self.parent.parent.profile_path, "db-backups")
        backup_type = "auto" if automatic else "manual"
        dst = os.path.join(database_backups_folderpath, "{}-{}-database.sqlite3".format(date,backup_type))

        print("Base de donnée copiée:", src, "->", dst)
        shutil.copy(src, dst)

        self._remove_old_backups()

    def restore_database_backup(self, filename):
        if not os.path.isfile(filename):
            # TODO: Erreur ?
            pass

        else:
            dst = self.parent.parent.database_path

            print("Base de donnée restaurée:", filename, "->", dst)
            shutil.copy(filename, dst)
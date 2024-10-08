import os
import shutil
from datetime import datetime

from database_manager import DATABASE_NAME


class DBBackupsManager:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.backups_limit = self.parent.parent.settings["backups_limit"]
        self.database_pattern = f"-{DATABASE_NAME}"
        self.backups_foldername = "db-backups"
        self.backups_folderpath = os.path.join(self.parent.parent.profile.path, self.backups_foldername)

    def _create_backup_folder(self) -> None:
        if not os.path.isdir(self.backups_folderpath):
            os.makedirs(self.backups_folderpath)

    def get_dbs_list(self) -> list[str]:
        self._create_backup_folder()

        databases_backups = [
            os.path.join(self.backups_folderpath, filename)
            for filename in sorted(os.listdir(self.backups_folderpath))
            if os.path.isfile(os.path.join(self.backups_folderpath, filename))
               and os.path.join(self.backups_folderpath, filename).endswith(self.database_pattern)
               and "-manual-" in filename or "-auto-" in filename
        ]

        return sorted(databases_backups)

    def _remove_old_backups(self) -> None:
        backups = self.get_dbs_list()
        if len(backups) >= self.backups_limit:
            nb_backups_to_delete = len(backups) - self.backups_limit
            backups_to_remove = backups[:nb_backups_to_delete]

            for backup in backups_to_remove:
                if os.path.isfile(backup):
                    os.remove(backup)

    def backup_current_database(self, automatic=True) -> None:
        self._create_backup_folder()

        date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        src = self.parent.parent.database_path
        database_backups_folderpath = os.path.join(self.parent.parent.profile.path, "db-backups")
        backup_type = "auto" if automatic else "manual"
        dst = os.path.join(database_backups_folderpath, f"{date}-{backup_type}{self.database_pattern}")

        print("Base de donnée copiée:", src, "->", dst)
        shutil.copy(src, dst)

        self._remove_old_backups()

    def restore_database_backup(self, filename) -> None:
        if not os.path.isfile(filename):
            # TODO: Erreur ?
            pass

        else:
            dst = self.parent.parent.database_path

            print("Base de donnée restaurée:", filename, "->", dst)
            shutil.copy(filename, dst)

    def remove_database_backup(self, filepath) -> None:
        if os.path.exists(filepath):
            os.remove(filepath)

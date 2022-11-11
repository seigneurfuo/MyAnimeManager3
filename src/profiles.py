import os
import shutil

from core import PROFILES_PATH
from database_manager import DATABASE_NAME, load_or_create_database

class Profiles():
    def __init__(self, name):
        self.name = name
        self.path = os.path.join(PROFILES_PATH, self.name)
        self.picture_filename = "picture.png"

    def __repr__(self):
        return self.path

    def create(self):
        # TODO: Sanitize (déplacer le contenu de la vérificaiton de la fenetre des profils ici ?

        # Existe déja
        if os.path.isdir(self.path):
            return False
        else:
            # Create folder
            os.makedirs(self.path)
            load_or_create_database(self)

    def set_picture(self, picture_path):
        if picture_path and os.path.isfile(picture_path):
            dst = os.path.join(self.path, self.picture_filename)
            shutil.copy(picture_path, dst)

    def get_picture(self):
        picture_path = os.path.join(self.path, "picture.png")
        if not os.path.isfile(picture_path):
            return os.path.join(os.path.dirname(__file__), "resources/icons/question.png")

        else:
            return picture_path

    def rename(self, new_name):
        new_path = os.path.join(PROFILES_PATH, new_name)

        # Le profil existe déja
        if os.path.isdir(new_path):
            return False
        else:
            os.makedirs(new_path)
            os.rename(self.path, new_path)
            self.delete()

    def delete(self):
        if self.exists():
            shutil.rmtree(self.path, ignore_errors=True)

    def exists(self):
        return os.path.isdir(self.path)

    @staticmethod
    def get_profiles_list():
        profiles_list = [Profiles(name=profile) for profile in os.listdir(PROFILES_PATH)
                         if os.path.isdir(os.path.join(PROFILES_PATH, profile))
                         and os.path.isfile(os.path.join(PROFILES_PATH, profile, DATABASE_NAME))]

        # TODO: Tri de la liste ?
        return profiles_list
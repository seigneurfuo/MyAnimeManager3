import os
import shutil

from common import PROFILES_PATH
from database_manager import DATABASE_NAME, load_or_create_database

class Profiles():
    def __init__(self, path=None, name=None):
        if name == None:
            self.path = path
            self.name = os.path.basename(self.path)

        else:
            self.name = name
            self.path = os.path.join(PROFILES_PATH, self.name)

    def __repr__(self):
        return self.path

    def create(self):
        # TODO: Sanitize

        # Create folder
        os.makedirs(self.path)
        load_or_create_database(self.path)

    def get_picture(self):
        picture_path = os.path.join(self.path, "picture.png")
        if not os.path.isfile(picture_path):
            return os.path.join(os.path.dirname(__file__), "resources/icons/question.png")

        else:
            return picture_path

    def delete(self):
        if os.path.isdir(self.path):
            shutil.rmtree(self.path, ignore_errors=True)

    @staticmethod
    def get_profiles_list():
        profiles_list = [Profiles(name=profile) for profile in os.listdir(PROFILES_PATH)
                         if os.path.isdir(os.path.join(PROFILES_PATH, profile))
                         and os.path.isfile(os.path.join(PROFILES_PATH, profile, DATABASE_NAME))]

        # TODO: Tri de la liste ?
        return profiles_list
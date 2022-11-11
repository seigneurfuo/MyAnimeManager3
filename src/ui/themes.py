# Inspiré par: https://pypi.org/project/pyqtdarktheme/
import os.path

class Theme():
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path)

    def __repr__(self):
        return self.path

    def load(self):
        with open(self.path, "r") as theme_file:
            return theme_file.read()


def get_themes_list():
    themes_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "../resources/themes/"))
    extensions = (".stylesheet", ".qss")

    themes = []

    for root, directories, filenames in os.walk(themes_path):
        for filename in filenames:
            if filename.endswith(extensions):
                filepath = os.path.join(root, filename)
                themes.append(Theme(filepath))

    return themes

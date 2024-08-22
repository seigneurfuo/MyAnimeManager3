# Inspiré par: https://pypi.org/project/pyqtdarktheme/
import os.path


class Theme:
    def __init__(self, path) -> None:
        self.path = path
        self.name, extension = os.path.splitext(os.path.basename(self.path))

    def __repr__(self) -> str:
        return self.path

    def load(self) -> str:
        if os.path.isfile(self.path):
            with open(self.path, "r") as theme_file:
                return theme_file.read()
        else:
            return ""


def get_themes_list() -> list[Theme]:
    # Theme par défaut du système
    default_theme = Theme("")
    default_theme.name = "Thême par défaut du système"

    themes_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "../resources/themes/"))
    extensions = (".stylesheet", ".qss")

    themes = [default_theme]

    for root, directories, filenames in os.walk(themes_path):
        for filename in filenames:
            if filename.endswith(extensions):
                filepath = os.path.join(root, filename)
                themes.append(Theme(filepath))

    return themes


def set_theme(qapplication, theme_filename) -> None:
    if theme_filename:
        theme = Theme(theme_filename)
        qapplication.setStyleSheet(theme.load())

from application import Application
import sys
import os

# Pour debug des erreurs
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    sys.excepthook = except_hook

    app_dir = os.path.abspath(os.path.dirname(__file__))

    application = Application(sys.argv, app_dir)
    application.exec_()
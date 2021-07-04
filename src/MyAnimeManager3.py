from application import Application
import sys

# POur debug des erreurs
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    sys.excepthook = except_hook

    application = Application(sys.argv)
    application.exec_()
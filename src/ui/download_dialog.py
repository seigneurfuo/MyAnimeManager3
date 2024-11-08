import sys
import time

import urllib.request

from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QProgressBar, QLabel
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    update_size = pyqtSignal(int)

    def __init__(self, url, filepath):
        super().__init__()
        self.url = url
        self.filepath = filepath

    def run(self):
        # Function to report progress
        def report_progress(block_num, block_size, total_size):
            downloaded_size = block_num * block_size
            if total_size > 0:
                self.progress.emit(int(downloaded_size / total_size * 100))
                self.update_size.emit(downloaded_size)  # Emit the downloaded size

                #time.sleep(0.001)

        urllib.request.urlretrieve(self.url, self.filepath, reporthook=report_progress)
        self.finished.emit()

class DownloadDialog(QDialog):
    def __init__(self, url, filepath):
        super().__init__()

        self.url = url
        self.filepath = filepath

        self.init_ui()

        self.start_download()

    def init_ui(self):
        self.setFixedSize(400, 200)  # Set the fixed width and height

        self.setWindowTitle(self.tr("Téléchargement des données pour l'autocomplétion"))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(self.tr("Téléchargement des données pour l'autocomplétion:"))
        self.layout.addWidget(self.label)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

    def start_download(self):
        self.download_thread = DownloadThread(self.url, self.filepath)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.update_size.connect(self.update_downloaded_size)
        self.download_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_downloaded_size(self, size):
        size_in_mb = size / (1024 * 1024)
        self.status_label.setText(self.tr(f"Téléchargé : {size_in_mb:.2f} Mo"))

    def download_finished(self):
        time.sleep(1)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    url = "https://raw.githubusercontent.com/manami-project/anime-offline-database/refs/heads/master/anime-offline-database-minified.json"
    filepath = "/tmp/anime-offline-database-minified.json"    # Replace with your desired file name

    window = DownloadDialog(url, filepath)
    window.show()
    sys.exit(app.exec())

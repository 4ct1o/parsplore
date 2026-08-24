from PySide6.QtWidgets import QMainWindow

from config.settings import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME}")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
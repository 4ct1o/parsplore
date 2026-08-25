from PySide6.QtWidgets import QMainWindow

from config.settings import load_settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        settings = load_settings()

        self.setWindowTitle(settings.get('app_name', 'parsplore()'))
        self.resize(settings.get('window_width', 800), settings.get('window_height', 600))
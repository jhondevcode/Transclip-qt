from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon
from constant import PROGRAM_NAME, PROGRAM_VERSION


class MainWindow(QWidget):

    def __init__(self, app: QApplication):
        super(MainWindow, self).__init__()
        self.__app_instance = app
        self.init_window()
    
    def init_window(self):
        self.setWindowTitle(f"{PROGRAM_NAME} {PROGRAM_VERSION}")
        self.setWindowIcon(QIcon("resources/svg/favicon.svg"))
        self.start_window_dimensions()

    def start_window_dimensions(self):
        screen_geometry = self.__app_instance.primaryScreen().availableGeometry()
        screen_width: int = screen_geometry.width()
        screen_height: int = screen_geometry.height()
        window_width: int = screen_width // 2
        window_height: int = screen_height // 2
        x_point: int = (screen_width - window_width) // 2
        y_point: int = (screen_height - window_height) // 2
        self.setGeometry(x_point, y_point, window_width, window_height)
        self.setMinimumSize(window_width, window_height)

    def init_ui(self):
        pass

    def init_menu_bar(self):
        pass

    def init_content(self):
        pass

    def init_status_bar(self):
        pass

from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMessageBox
from PyQt6.QtGui import QIcon, QDesktopServices, QCloseEvent
from PyQt6.QtCore import QUrl

from constant import PROGRAM_NAME, PROGRAM_VERSION, PROGRAM_URL
from impl import Requester
from util import browse
from logger import LOG_DIR, log_file


class MainWindow(QMainWindow, Requester):

    def __init__(self, app: QApplication):
        QMainWindow.__init__(self)
        Requester.__init__(self)
        self.app_loop = app
        self.init_window()
    
    def init_window(self):
        self.setWindowTitle(f"{PROGRAM_NAME} {PROGRAM_VERSION}")
        self.setWindowIcon(QIcon("resources/svg/favicon.svg"))
        self.start_window_dimensions()
        self.init_ui()

    def start_window_dimensions(self):
        screen_geometry = self.app_loop.primaryScreen().availableGeometry()
        screen_width: int = screen_geometry.width()
        screen_height: int = screen_geometry.height()
        window_width: int = screen_width // 2
        window_height: int = screen_height // 2
        x_point: int = (screen_width - window_width) // 2
        y_point: int = (screen_height - window_height) // 2
        self.setGeometry(x_point, y_point, window_width, window_height)
        self.setMinimumSize(window_width, window_height)

    def init_ui(self):
        self.init_menu_bar()
        self.init_content()
        self.init_menu_bar()

    def init_menu_bar(self):
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

    def init_content(self):
        pass

    def init_status_bar(self):
        pass

    def closeEvent(self, event: QCloseEvent) -> None:
        quit_message = QMessageBox.question(
            self, "Confirm exit", "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes)
        if quit_message == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


class MenuBar(QMenuBar):

    def __init__(self, parent: MainWindow):
        super(MenuBar, self).__init__()
        self.parent = parent
        self.init_file_menu()
        self.init_run_menu()
        self.init_tools_menu()
        self.init_help_menu()

    def init_file_menu(self):
        self.file_menu = self.addMenu("&File")
        self.open_action = self.file_menu.addAction(QIcon("resources/svg/open_icon.svg"), "&Open")
        self.open_action.setShortcut("Ctrl+O")

        self.save_action = self.file_menu.addAction(QIcon("resources/svg/save_icon.svg"), "&Save")
        self.save_action.setShortcut("Ctrl+S")
        self.file_menu.addSeparator()

        self.exit_action = self.file_menu.addAction(QIcon("resources/svg/exit_icon.svg"), "&Exit")
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.parent.close)

    def init_run_menu(self):
        self.run_menu = self.addMenu("&Run")
        self.start_monitor_action = self.run_menu.addAction(QIcon("resources/svg/start_icon.svg"), "St&art monitor")
        self.start_monitor_action.setShortcut("Ctrl+Shift+A")
        self.stop_monitor_action = self.run_menu.addAction(QIcon("resources/svg/stop_icon.svg"), "St&op monitor")
        self.stop_monitor_action.setShortcut("Ctrl+Shift+O")

    def init_tools_menu(self):
        self.tools_menu = self.addMenu("&Tools")
        self.logs_menu = self.tools_menu.addMenu(QIcon("resources/svg/log_icon.svg"), "&Logs")

        self.show_log_action = self.logs_menu.addAction("&Show log")
        self.show_log_action.setShortcut("Shift+L")
        self.show_log_action.triggered.connect(lambda: browse(log_file))

        self.open_logdir_action = self.logs_menu.addAction("&Open logs dir")
        self.open_logdir_action.setShortcut("Shift+O")
        self.open_logdir_action.triggered.connect(lambda: browse(LOG_DIR))

        self.clear_logs_action = self.logs_menu.addAction("&Clear old logs")
        self.clear_logs_action.setShortcut("Shift+D")

        self.setting_action = self.tools_menu.addAction(QIcon("resources/svg/settings_icon.svg"), "&Settings")
        self.setting_action.setShortcut("Ctrl+Shift+S")

    def init_help_menu(self):
        self.help_menu = self.addMenu("&Help")
        self.help_action = self.help_menu.addAction(QIcon("resources/svg/help_icon.svg"), "H&elp")

        self.github_action = self.help_menu.addAction(QIcon("resources/svg/github_icon.svg"), "&Github")
        self.github_action.triggered.connect(lambda : browse(PROGRAM_URL))
        self.help_menu.addSeparator()
        
        self.about_action = self.help_menu.addAction(QIcon("resources/svg/about_icon.svg"), "&About")

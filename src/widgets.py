from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMessageBox
from PyQt6.QtWidgets import QDialog, QTextEdit, QPushButton
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QIcon, QDesktopServices, QCloseEvent
from PyQt6.QtCore import QUrl

from homedir import get_home_path
from constant import PROGRAM_NAME, PROGRAM_VERSION, PROGRAM_URL
from os import listdir, remove
from os.path import isfile, join
from impl import Requester
from util import browse
from typing import List
from logger import logger, LOG_DIR, log_file, log_file_name


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
        self.show_log_action.triggered.connect(lambda: LogViewer(self.parent).exec())

        self.open_logdir_action = self.logs_menu.addAction("&Open logs dir")
        self.open_logdir_action.setShortcut("Shift+O")
        self.open_logdir_action.triggered.connect(lambda: browse(LOG_DIR))

        self.clear_logs_action = self.logs_menu.addAction("&Clear old logs")
        self.clear_logs_action.setShortcut("Shift+D")
        self.clear_logs_action.triggered.connect(self.__delete_old_logs)

        self.setting_action = self.tools_menu.addAction(QIcon("resources/svg/settings_icon.svg"), "&Settings")
        self.setting_action.setShortcut("Ctrl+Shift+S")

    def init_help_menu(self):
        self.help_menu = self.addMenu("&Help")
        self.help_action = self.help_menu.addAction(QIcon("resources/svg/help_icon.svg"), "H&elp")

        self.github_action = self.help_menu.addAction(QIcon("resources/svg/github_icon.svg"), "&Github")
        self.github_action.triggered.connect(lambda : browse(PROGRAM_URL))
        self.help_menu.addSeparator()
        
        self.about_action = self.help_menu.addAction(QIcon("resources/svg/about_icon.svg"), "&About")

    def __delete_old_logs(self):
        files: List[str] = listdir(LOG_DIR)
        if len(files) > 1:
            quit_message = QMessageBox.question(
                self.parent, "Confirm delete", "Are you sure you want to delete the old log files?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes)
            if quit_message == QMessageBox.StandardButton.Yes:
                try:
                    for fls in files:
                        to_remove = join(LOG_DIR, fls)
                        if fls is not log_file_name and isfile(to_remove):
                            remove(to_remove)
                            logger.warn(f"Deleting {to_remove}")
                    QMessageBox.information(self.parent, "Success", "The old records have been erased.", QMessageBox.StandardButton.Ok)
                except Exception as ex:
                    QMessageBox.critical(self.parent, "Error", str(ex), QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self.parent, PROGRAM_NAME, "No old log files found.", QMessageBox.StandardButton.Ok)


class LogViewer(QDialog):
    
    def __init__(self, parent):
        super(LogViewer, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.init_ui()
        self.init_buttons()
        self.load_log_content()

    def init_ui(self):
        self.setWindowTitle(log_file_name)
        self.resize(400, 300)
        self.editor = QTextEdit(self)
        self.layout.addWidget(self.editor)

    def init_buttons(self):
        buttons_layout = QHBoxLayout()
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.editor.clear())
        buttons_layout.addWidget(clear_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(lambda: self.close())
        buttons_layout.addWidget(close_button)
        self.layout.addLayout(buttons_layout)

    def load_log_content(self):
        log = open(log_file, mode="r", encoding="utf-8")
        self.editor.setPlainText(log.read())
        log.close()

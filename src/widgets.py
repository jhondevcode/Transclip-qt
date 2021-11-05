from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMessageBox
from PyQt6.QtWidgets import QDialog, QTextEdit, QPushButton, QLabel, QWidget
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QIcon, QCloseEvent, QFont, QPixmap

from constant import PROGRAM_NAME, PROGRAM_VERSION, PROGRAM_URL
from os import listdir, remove
from os.path import isfile, join
from impl import Requester
from util import browse
from typing import List
from logger import logger, LOG_DIR, log_file, log_file_name
from clipboard import clear
from dialog import show_text_dialog, show_question_dialog, show_info_dialog, show_error_dialog
from util import locale
from config import config


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
        self.init_status_bar()

    def init_menu_bar(self):
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

    def init_content(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

    def init_status_bar(self):
        self.state_bar = StateBar()
        self.central_layout.addLayout(self.state_bar)
        self.state_bar.set_state(locale.value("STATE_LABEL_OFF"))
        self.state_bar.set_source(config.get("source"))
        self.state_bar.set_target(config.get("target"))
        self.state_bar.set_words(0)
        self.state_bar.set_delay(float(config.get("interval")))

    def closeEvent(self, event: QCloseEvent) -> None:
        quit_message = show_question_dialog(self, locale.value("EXIT_DIALOG_TITLE"), locale.value("EXIT_DIALOG_MESSAGE"))
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
        self.file_menu = self.addMenu(locale.value("MENU_BAR_FILE"))
        self.open_action = self.file_menu.addAction(QIcon("resources/svg/open_icon.svg"), locale.value("MENU_BAR_FILE_OPEN"))
        self.open_action.setShortcut("Ctrl+O")

        self.save_action = self.file_menu.addAction(QIcon("resources/svg/save_icon.svg"), locale.value("MENU_BAR_FILE_SAVE"))
        self.save_action.setShortcut("Ctrl+S")
        self.file_menu.addSeparator()

        self.exit_action = self.file_menu.addAction(QIcon("resources/svg/exit_icon.svg"), locale.value("MENU_BAR_FILE_EXIT"))
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.parent.close)

    def init_run_menu(self):
        self.run_menu = self.addMenu(locale.value("MENU_BAR_RUN"))
        self.start_monitor_action = self.run_menu.addAction(QIcon("resources/svg/start_icon.svg"), locale.value("MENU_BAR_RUN_START_MONITOR"))
        self.start_monitor_action.setShortcut("Ctrl+Shift+T")
        self.stop_monitor_action = self.run_menu.addAction(QIcon("resources/svg/stop_icon.svg"), locale.value("MENU_BAR_RUN_STOP_MONITOR"))
        self.stop_monitor_action.setShortcut("Ctrl+Shift+P")

    def init_tools_menu(self):
        self.tools_menu = self.addMenu(locale.value("MENU_BAR_TOOLS"))
        self.logs_menu = self.tools_menu.addMenu(QIcon("resources/svg/log_icon.svg"), locale.value("MENU_BAR_TOOLS_LOGS"))

        self.show_log_action = self.logs_menu.addAction(locale.value("MENU_BAR_TOOLS_LOGS_SHOW"))
        self.show_log_action.setShortcut("Shift+L")
        self.show_log_action.triggered.connect(lambda: show_text_dialog(self.parent, log_file, log_file_name, True))

        self.open_logdir_action = self.logs_menu.addAction(locale.value("MENU_BAR_TOOLS_LOGS_DIR"))
        self.open_logdir_action.setShortcut("Shift+O")
        self.open_logdir_action.triggered.connect(lambda: browse(LOG_DIR))

        self.clear_logs_action = self.logs_menu.addAction(locale.value("MENU_BAR_TOOLS_LOGS_CLEAR"))
        self.clear_logs_action.setShortcut("Shift+D")
        self.clear_logs_action.triggered.connect(self.__delete_old_logs)

        self.clipboard_menu = self.tools_menu.addMenu(locale.value("MENU_BAR_TOOLS_CLIPBOARD"))

        self.clipboard_history_action = self.clipboard_menu.addAction(locale.value("MENU_BAR_TOOLS_CLIPBOARD_HISTORY"))

        self.clipboard_clear_action = self.clipboard_menu.addAction(locale.value("MENU_BAR_TOOLS_CLIPBOARD_CLEAR"))
        self.clipboard_clear_action.triggered.connect(clear)

        self.setting_action = self.tools_menu.addAction(QIcon("resources/svg/settings_icon.svg"), locale.value("MENU_BAR_TOOLS_SETTINGS"))
        self.setting_action.setShortcut("Ctrl+Shift+S")

    def init_help_menu(self):
        self.help_menu = self.addMenu("&Help")
        self.help_action = self.help_menu.addAction(QIcon("resources/svg/help_icon.svg"), locale.value("MENU_BAR_HELP"))
        self.help_action.setShortcut("Ctrl+Shift+H")

        self.github_action = self.help_menu.addAction(QIcon("resources/svg/github_icon.svg"), locale.value("MENU_BAR_HELP_GITHUB"))
        self.github_action.triggered.connect(lambda: browse(PROGRAM_URL))
        self.github_action.setShortcut("Ctrl+Shift+G")
        self.help_menu.addSeparator()
        
        self.about_action = self.help_menu.addAction(QIcon("resources/svg/about_icon.svg"), locale.value("MENU_BAR_HELP_ABOUT"))
        self.about_action.setShortcut("Ctrl+Shift+A")

    def __delete_old_logs(self):
        files: List[str] = listdir(LOG_DIR)
        if len(files) > 1:
            quit_message = show_question_dialog(self.parent, locale.value("CLEAR_LOG_DIALOG_TITLE"), locale.value("CLEAR_LOG_DIALOG_MESSAGE"))
            if quit_message == QMessageBox.StandardButton.Yes:
                try:
                    for fls in files:
                        to_remove = join(LOG_DIR, fls)
                        if fls is not log_file_name and isfile(to_remove):
                            remove(to_remove)
                            logger.warn(f"Deleting {to_remove}")
                    show_info_dialog(self.parent, locale.value("SUCCESSFUL_TITLE"), locale.value("CLEAR_LOG_DIALOG_SUCCESS"))
                except Exception as ex:
                    logger.error(ex)
                    show_error_dialog(self.parent, "Error", str(ex))
        else:
            show_info_dialog(self.parent, PROGRAM_NAME, locale.value("CLEAR_LOG_DIALOG_NOT_FOUND"))


class StateBar(QHBoxLayout):

    def __init__(self):
        super(StateBar, self).__init__()
        self.load_ui()

    def load_ui(self):
        self.state_label = QLabel()
        self.addWidget(self.state_label)

        self.source_label = QLabel()
        self.addWidget(self.source_label)

        self.target_label = QLabel()
        self.addWidget(self.target_label)

        self.words_label = QLabel()
        self.addWidget(self.words_label)

        self.delay_label = QLabel()
        self.addWidget(self.delay_label)

    def set_state(self, state: str):
        self.state_label.setText(f'{locale.value("STATE_LABEL_TEXT")}: {state}')

    def set_source(self, source: str):
        self.source_label.setText(f'{locale.value("SOURCE_LABEL_TEXT")}: {source}')

    def set_target(self, target: str):
        self.target_label.setText(f'{locale.value("TARGET_LABEL_TEXT")}: {target}')

    def set_words(self, words: int):
        self.words_label.setText(f'{locale.value("WORDS_LABEL_TEXT")}: {words}')

    def set_delay(self, delay: float):
        self.delay_label.setText(f'{locale.value("DELAY_LABEL_TEXT")}: {delay}')

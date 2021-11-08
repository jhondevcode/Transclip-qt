import sys

import setproctitle as spt
from PyQt5.QtWidgets import QApplication

from clipboard import clear
from constant import PROGRAM_NAME
from logger import logger
from widgets import MainWindow
from util import load_style


def main():
    try:
        spt.setproctitle(PROGRAM_NAME)
        app = QApplication(sys.argv)
        clear()
        load_style(app.setStyleSheet)
        window = MainWindow(app)
        window.show()
        sys.exit(app.exec())
    except Exception as ex:
        logger.error(ex)


if __name__ == "__main__":
    main()

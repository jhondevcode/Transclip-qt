import sys

import setproctitle as spt
from PyQt5.QtWidgets import QApplication

from clipboard import clear
from config import config
from constant import PROGRAM_NAME
from widgets import MainWindow


def main():
    spt.setproctitle(PROGRAM_NAME)
    app = QApplication(sys.argv)
    clear()
    with open(f"resources/styles/{config.get('style')}", mode="r", encoding="utf-8") as stylesheet:
        app.setStyleSheet(stylesheet.read())
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

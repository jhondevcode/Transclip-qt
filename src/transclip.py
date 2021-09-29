import os
import sys
from PyQt6.QtWidgets import QApplication
from widgets import MainWindow
from util import WORKSPACE


def prepare_workspace():
    if os.getcwd() != WORKSPACE:
        os.chdir(WORKSPACE)


def main():
    prepare_workspace()
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

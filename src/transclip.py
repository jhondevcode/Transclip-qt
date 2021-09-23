import os
import sys
from PyQt6.QtWidgets import QApplication
from widgets import MainWindow


def prepare_workspace():
    static_home = str(__file__).replace("/transclip.py", "")
    if os.getcwd() != static_home:
        os.chdir(static_home)


def main():
    prepare_workspace()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

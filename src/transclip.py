import sys
from PyQt5.QtWidgets import QApplication
from widgets import MainWindow
import setproctitle as spt
from constant import PROGRAM_NAME
from qtsass import compile
from config import config


def main():
    spt.setproctitle(PROGRAM_NAME)
    app = QApplication(sys.argv)
    with open(f"resources/styles/{config.get('style')}", mode="r", encoding="utf-8") as stylesheet:
        app.setStyleSheet(compile(stylesheet.read()))
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

import sys
from PyQt5.QtWidgets import QApplication
from widgets import MainWindow
import setproctitle as spt
from constant import PROGRAM_NAME


def main():
    spt.setproctitle(PROGRAM_NAME)
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

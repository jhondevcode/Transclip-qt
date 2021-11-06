import sys
from PyQt5.QtWidgets import QApplication
from widgets import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

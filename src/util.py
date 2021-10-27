from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl


def browse(url: str):
    """
        This function uses the Qt core to open a url in the system's
        default browser.
    """
    QDesktopServices.openUrl(QUrl(url))

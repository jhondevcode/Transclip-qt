from json import load

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from config import config


class LocaleUtil:

    def __init__(self):
        file_path = f"resources/locales/{config.get('locale')}"
        file = open(file_path, mode="r", encoding="utf-8")
        self.dictionary = load(file)
        file.close()

    def value(self, key: str) -> str:
        return self.dictionary[key]


locale = LocaleUtil()


def browse(url: str):
    """
        This function uses the Qt core to open a url in the system's
        default browser.
    """
    QDesktopServices.openUrl(QUrl(url))

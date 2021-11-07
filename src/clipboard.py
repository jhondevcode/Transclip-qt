from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import QApplication
from pyperclip import copy, paste


def clear():
    QApplication.clipboard().clear(QClipboard.Clipboard)

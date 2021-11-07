from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import QApplication


def copy(content: str):
    QApplication.clipboard().setText(content, QClipboard.Clipboard)


def paste() -> str:
    return QApplication.clipboard().text(QClipboard.Clipboard)


def clear():
    QApplication.clipboard().clear(QClipboard.Clipboard)

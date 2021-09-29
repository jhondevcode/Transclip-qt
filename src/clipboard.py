from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QClipboard


def copy(content: str):
    QApplication.clipboard().setText(content, QClipboard.Mode.Clipboard)


def paste() -> str:
    return QApplication.clipboard().text(QClipboard.Mode.Clipboard)


def clear():
    QApplication.clipboard().clear(QClipboard.Mode.Clipboard)

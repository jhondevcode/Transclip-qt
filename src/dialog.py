"""
This module provides widgets to display information in text boxes as well as
functions to display dialog.
"""

from PyQt5.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QTextEdit, QPushButton

from exceptions import UnsatisfiedResourceException
from util import locale


# noinspection PyAttributeOutsideInit
class TextDialog(QDialog):

    def __init__(self, parent, file: str, title, buttons=True):
        super(TextDialog, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle(title)
        self.with_buttons = buttons
        self.text_file = None
        self.resize(400, 300)
        if file is not None and len(file) > 0:
            self.text_file = file
            self.init_widgets()
        else:
            self.close()
            raise UnsatisfiedResourceException("File path not specified")

    def init_widgets(self):
        self.editor = QTextEdit(self)
        self.layout.addWidget(self.editor)
        if self.with_buttons:
            self.init_buttons()

    def init_buttons(self):
        buttons_layout = QHBoxLayout()
        self.clear_button = QPushButton(locale.value("CLEAR"))
        self.clear_button.clicked.connect(lambda: self.editor.clear())
        self.clear_button.setEnabled(False)
        buttons_layout.addWidget(self.clear_button)

        close_button = QPushButton(locale.value("CLOSE"))
        close_button.clicked.connect(self.close)
        buttons_layout.addWidget(close_button)
        self.layout.addLayout(buttons_layout)
        self.editor.textChanged.connect(self.change_event)
        self.load_file_content()

    def change_event(self):
        if len(self.editor.toPlainText()) > 0:
            self.clear_button.setEnabled(True)
        else:
            self.clear_button.setEnabled(False)

    def load_file_content(self):
        file = open(self.text_file, mode="r", encoding="utf-8")
        self.editor.setPlainText(file.read())
        file.close()


def show_question_dialog(parent, title, message):
    buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    return QMessageBox.question(parent, title, message, buttons, QMessageBox.StandardButton.Yes)


def show_error_dialog(parent, title, message):
    return QMessageBox.critical(parent, title, message, QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)


def show_info_dialog(parent, title, message):
    return QMessageBox.information(parent, title, message, QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)


def show_warning_dialog(parent, title, message):
    buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    return QMessageBox.warning(parent, title, message, buttons, QMessageBox.StandardButton.Yes)


def show_text_dialog(parent=None, file="", title="", buttons=False):
    TextDialog(parent=parent, file=file, title=title, buttons=buttons).exec()

"""
This module provides widgets to display information in text boxes as well as
functions to display dialog.
"""

from os.path import join

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QTextEdit, QPushButton, QLabel, QTabWidget

from constant import PROGRAM_NAME, PROGRAM_DESCRIPTION, PROGRAM_VERSION
from exceptions import UnsatisfiedResourceException
from util import locale, svg_loader, resources_path

AUTHORS = [{'name': 'Jhon Fernandez', 'email': 'jhondev.code@gmail.com', 'github': 'github.com/jhondevcode'}]


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


class AboutDialog(QDialog):

    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent)
        self.setWindowTitle(locale.value("TRANSCLIP_ABOUT_TITLE") + " " + PROGRAM_NAME)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.center_dialog()
        self.init_ui()

    def center_dialog(self):
        # self.resize(round(self.parent().width() * 0.9), round(self.parent().height() * 0.8))
        self.resize(600, 300)

    def init_ui(self):
        header_layout = QVBoxLayout()
        icon = QLabel()
        svg_loader.load_scaled_pixmap('favicon', 64, 64, icon.setPixmap)
        icon.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(icon)
        title = QLabel(f'{PROGRAM_NAME} {PROGRAM_VERSION}')
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        description = QLabel(locale.value("TRANSCLIP_DESCRIPTION"))
        description.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(description)
        self.main_layout.addLayout(header_layout)

        tab_panel = QTabWidget()
        tab_panel.resize(round(self.width() * 0.9), round(self.height() * 0.5))
        tab_panel.addTab(self.get_authors(), locale.value("ABOUT_TAB_DEVELOPERS"))
        tab_panel.addTab(self.get_license(), locale.value("ABOUT_TAB_LICENSE"))
        self.main_layout.addWidget(tab_panel)

    def get_authors(self):
        widget = QTextEdit()
        widget.setReadOnly(True)
        text = f"{locale.value('ABOUT_TAB_BY')}\n\n"
        for author in AUTHORS:
            text += f"\t{author['name']}\n\t{author['email']}\n\t{author['github']}\n\n"
        widget.setText(text)
        return widget

    def get_license(self):
        widget = QTextEdit()
        widget.setReadOnly(True)
        with open(join(join(resources_path(), "other"), "license.txt"), mode='r', encoding='utf-8') as license_file:
            widget.setPlainText(license_file.read())
        widget.setAlignment(Qt.AlignJustify)
        return widget


def show_question_dialog(parent, title, message):
    buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    return QMessageBox.question(parent, title, message, buttons, QMessageBox.StandardButton.Yes)


def show_error_dialog(parent, title="Error", message="Error message"):
    return QMessageBox.critical(parent, title, message, QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)


def show_info_dialog(parent, title, message):
    return QMessageBox.information(parent, title, message, QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)


def show_warning_dialog(parent, title, message, buttons=True):
    if buttons:
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        return QMessageBox.warning(parent, title, message, buttons, QMessageBox.StandardButton.Yes)
    else:
        return QMessageBox.warning(parent, title, message, QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)


def show_text_dialog(parent=None, file="", title="", buttons=False):
    TextDialog(parent=parent, file=file, title=title, buttons=buttons).exec()


def show_about_dialog(parent=None):
    AboutDialog(parent=parent).exec()

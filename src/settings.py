"""
This module contains widgets to manipulate the various settings of the program.
"""
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QDialog, QComboBox, QPushButton, QLabel, QDoubleSpinBox, QMessageBox
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout

from os.path import join, isfile
from json import load
from config import config
from dialog import show_question_dialog, show_warning_dialog, show_error_dialog, show_info_dialog
from util import locale, resources_path
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES


# noinspection PyAttributeOutsideInit
class SettingsAssistant(QDialog):
    """Main configuration window"""

    def __init__(self, parent):
        super(SettingsAssistant, self).__init__(parent)
        self.setWindowTitle(locale.value("TRANSCLIP_SETTINGS_TITLE"))
        # self.resize(300, 200)
        self.setFixedSize(300, 200)

        self.dialog_layout = QVBoxLayout()
        self.setLayout(self.dialog_layout)

        self.widgets_layout = QGridLayout()
        self.dialog_layout.addLayout(self.widgets_layout)

        self.start_translator_widgets()
        self.start_additional_widgets()
        self.start_settings_option()

    def start_translator_widgets(self):
        """ Settings for target, source, sleep interval """
        self.widgets_layout.addWidget(QLabel(locale.value("SOURCE_LABEL_TEXT")), 0, 0)
        self.widgets_layout.addWidget(self._get_sources(), 0, 1)

        self.widgets_layout.addWidget(QLabel(locale.value("TARGET_LABEL_TEXT")), 1, 0)
        self.widgets_layout.addWidget(self._get_targets(), 1, 1)

        self.widgets_layout.addWidget(
            QLabel(locale.value("DELAY_LABEL_TEXT") + " (" + locale.value("TRANSCLIP_SECONDS") + ")"), 2, 0)
        self.widgets_layout.addWidget(self._get_monitor_delay(), 2, 1)

    def start_additional_widgets(self):
        """ Settings for theme and lang """
        self.widgets_layout.addWidget(QLabel(locale.value("TRANSCLIP_LOCALE_LANG")), 3, 0)
        self.widgets_layout.addWidget(self._get_locales(), 3, 1)

        self.widgets_layout.addWidget(QLabel(locale.value("TRANSCLIP_GLOBAL_THEME")), 4, 0)
        self.widgets_layout.addWidget(self._get_themes(), 4, 1)

        self.widgets_layout.addWidget(QLabel(locale.value("TRANSCLIP_ORIGINAL_TEXT")), 5, 0)
        self.widgets_layout.addWidget(self._get_source_options(), 5, 1)

    def start_settings_option(self):
        foot_layout = QHBoxLayout()

        self.save_button = QPushButton(locale.value("TRANSCLIP_SAVE"))
        self.save_button.clicked.connect(self.save_changes)
        foot_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton(locale.value("TRANSCLIP_CANCEL"))
        self.cancel_button.clicked.connect(self.close)
        foot_layout.addWidget(self.cancel_button)

        self.dialog_layout.addLayout(foot_layout)

    def save_changes(self):
        if self._have_changes():
            config.clean_to_save()
            config.add_to_save(key="translator.source", value=self.source_combo.currentText())
            config.add_to_save(key="translator.target", value=self.target_combo.currentText())
            config.add_to_save(key="monitor.interval", value=self.delay_selector.text())
            config.add_to_save(key="transclip.locale", value=self.locale_combo.currentText())
            config.add_to_save(key="transclip.theme", value=self.theme_combo.currentText())
            config.add_to_save(key="editext.source.view", value="True" if self.text_source_combo.currentText() == locale.value("TRANSCLIP_YES_OPTION") else "False")
            save_state: bool = config.save()
            if not save_state:  # Checking not error occurred
                show_info_dialog(self, title=locale.value("TRANSCLIP_SAVE_SUCCESS_TITLE"),
                                 message=locale.value("TRANSCLIP_SAVE_SUCCESS_MESSAGE"))
                config.load()
                self.close()
            else:
                show_error_dialog(self, title=locale.value("TRANSCLIP_SAVE_ERROR_TITLE"),
                                  message=locale.value("TRANSCLIP_SAVE_ERROR_MESSAGE"))
        else:
            show_warning_dialog(self, title=locale.value("TRANSCLIP_WARNING"),
                                message=locale.value("TRANSCLIP_UNCHANGED"), buttons=False)

    def _get_sources(self) -> QComboBox:
        current_source = config.get("translator.source")
        sources = list(GOOGLE_LANGUAGES_TO_CODES.keys())
        self.source_combo = QComboBox()
        self.source_combo.addItems(sources)
        self.source_combo.setCurrentIndex(sources.index(current_source))
        return self.source_combo

    def _get_targets(self) -> QComboBox:
        current_target = config.get("translator.target")
        targets = list(GOOGLE_LANGUAGES_TO_CODES.keys())
        self.target_combo = QComboBox()
        self.target_combo.addItems(targets)
        self.target_combo.setCurrentIndex(targets.index(current_target))
        return self.target_combo

    def _get_monitor_delay(self) -> QDoubleSpinBox:
        self.delay_selector = QDoubleSpinBox()
        self.delay_selector.setValue(config.get_float("monitor.interval"))
        self.delay_selector.setDecimals(1)
        self.delay_selector.setSingleStep(0.1)
        return self.delay_selector

    def _get_themes(self) -> QComboBox:
        # config.get("transclip.style")
        theme_list = join(resources_path(), "styles", "index.json")
        themes = {}
        if isfile(theme_list):
            with open(theme_list, mode="r", encoding="utf-8") as theme_file:
                themes = load(theme_file)

        self.theme_combo = QComboBox()
        themes_list = list(themes.keys())
        themes_list.append("System default")
        # print(list(themes.values()))
        if len(themes) > 0:
            self.theme_combo.addItems(themes_list)
            self.theme_combo.setCurrentIndex(themes_list.index(config.get("transclip.theme")))
        else:
            self.theme_combo.setDisabled(True)
        return self.theme_combo

    def _get_locales(self) -> QComboBox:
        self.locale_combo = QComboBox()
        # transclip.locale
        locale_list = list(locale.list_locales().keys())
        if len(locale_list) > 0:
            self.locale_combo.addItems(locale_list)
            self.locale_combo.setCurrentIndex(locale_list.index(config.get("transclip.locale")))
        else:
            self.locale_combo.setDisabled(True)
        return self.locale_combo

    def _get_source_options(self) -> QComboBox:
        self.text_source_combo = QComboBox()
        current_option = config.get("editext.source.view")
        if current_option is not None:
            options = [locale.value("TRANSCLIP_YES_OPTION"), locale.value("TRANSCLIP_NO_OPTION")]
            self.text_source_combo.addItems(options)
            self.text_source_combo.setCurrentIndex(0 if current_option == 'True' else 1)
        else:
            self.text_source_combo.setDisabled(True)
        return self.text_source_combo

    def _have_changes(self) -> bool:
        source_changed = config.get("translator.source") != self.source_combo.currentText()
        target_changed = config.get("translator.target") != self.target_combo.currentText()
        delay_changed = config.get("monitor.interval") != self.delay_selector.text()
        lang_changed = config.get("transclip.locale") != self.locale_combo.currentText()
        theme_changed = config.get("transclip.theme") != self.theme_combo.currentText()
        source_view_changed = config.get("editext.source.view") != ("True" if self.text_source_combo.currentText() == locale.value("TRANSCLIP_YES_OPTION") else "False")
        return source_changed or target_changed or delay_changed or lang_changed or theme_changed or source_view_changed

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._have_changes():
            quit_message = show_question_dialog(self, locale.value("TRANSCLIP_CONTINUE"),
                                                locale.value("TRANSCLIP_UNSAVED_CHANGES"))
            if quit_message == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def show_settings_dialog(parent=None):
    SettingsAssistant(parent=parent).exec()

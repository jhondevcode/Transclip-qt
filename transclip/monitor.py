"""
"""

from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES

from clipboard import copy, paste
from config import config
from formatters import PlainTextFormatter
from impl import AbstractMonitor, AbstractFormatter
from logger import logger
from translation import PlainTextTranslator
from util import locale


class Monitor(QThread, AbstractMonitor):
    source = pyqtSignal(str)
    target = pyqtSignal(str)
    words = pyqtSignal(int)

    def __init__(self, owner):
        QThread.__init__(self)
        AbstractMonitor.__init__(self)
        self.owner = owner
        self.interval_time = config.get("monitor.interval")
        self.formatter = PlainTextFormatter()
        self.translator = PlainTextTranslator(self._get_safe_lang_key(config.get("translator.source")),
                                              self._get_safe_lang_key(config.get("translator.target")))

    def set_interval_time(self, interval: int):
        self.interval_time = interval
        
    def set_formatter(self, new_formatter: AbstractFormatter):
        self.formatter = new_formatter
        
    def set_translator(self, new_translator):
        self.translator = new_translator

    def invoke_translate(self, actual: str, old: str):
        self.source.emit(actual)
        self.target.emit(locale.value("TRANSLATING"))
        try:
            translated = self.translator.translate(actual)
            copy(translated)
            return translated
        except Exception as ex:
            logger.error(ex)
            print(ex)
            return old

    def run(self) -> None:
        old_text = ""
        while self.is_running():
            clipboard_content = paste()
            if clipboard_content is not None and len(clipboard_content) > 0:
                if clipboard_content != old_text:
                    clipboard_content = self.formatter.format(clipboard_content)
                    old_text = self.invoke_translate(clipboard_content, old_text)
                    self.words.emit(len(clipboard_content.split(" ")))
                    self.target.emit(old_text)
                else:
                    if old_text == "":
                        old_text = self.invoke_translate(clipboard_content, old_text)
            sleep(float(self.interval_time))

    def start_monitoring(self):
        super().start_monitoring()
        self.start()

    def stop_monitoring(self):
        super().stop_monitoring()
        if not self.isRunning() and self.isFinished():
            self.exit(0)

    def _get_safe_lang_key(self, lang: str):
        return GOOGLE_LANGUAGES_TO_CODES[lang] if lang in GOOGLE_LANGUAGES_TO_CODES else "auto"

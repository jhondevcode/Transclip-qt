"""
"""

from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from clipboard import copy, paste
from config import config
from formatters import PlainTextFormatter
from impl import AbstractMonitor
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
        self.translator = PlainTextTranslator(config.get("translator.source"), config.get("translator.target"))

    def invoke_translate(self, actual: str, old: str):
        self.source.emit(actual)
        self.target.emit(locale.value("TRANSLATING"))
        try:
            translated = self.translator.translate(actual)
            self.target.emit(translated)
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
                clipboard_content = self.formatter.format(clipboard_content)
                self.words.emit(len(clipboard_content.split(" ")))
                if clipboard_content != old_text:
                    old_text = self.invoke_translate(clipboard_content, old_text)
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

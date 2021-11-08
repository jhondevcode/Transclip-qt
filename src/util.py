from json import load
from os import getcwd
from os.path import isfile, join

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices, QIcon, QBitmap, QImage

from config import config
from homedir import get_home_path
from logger import logger


class ImageLoader:

    def __init__(self):
        super(ImageLoader, self).__init__()
        self.image_dir = None
        res_config: str = config.get("resources")
        if "${HOME}" in res_config:
            path = res_config.replace("${HOME}", get_home_path())
            logger.info(f"Resources path: {path}")
        elif "${CURRENT}" in res_config:
            path = res_config.replace("${CURRENT}", getcwd())
            logger.info(f"Resources path: {path}")
        else:
            path = None
            logger.error("Not found resources path")
        if path is not None:
            self.image_dir = join(path, "svg")

    def load(self, name: str, function, object_type="icon"):
        if self.image_dir is not None and isfile(join(self.image_dir, f"{name}.svg")):
            file_name = join(self.image_dir, f"{name}.svg")
            logger.info(f"Loading: {file_name}")
            if object_type == "bitmap":
                function(QBitmap(file_name))
            elif object_type == "icon":
                function(QIcon(file_name))
            elif object_type == "image":
                function(QImage(file_name))


class LocaleUtil:

    def __init__(self):
        self.dictionary = None
        try:
            file_path = f"resources/locales/{config.get('locale')}"
            file = open(file_path, mode="r", encoding="utf-8")
            self.dictionary = load(file)
            file.close()
        except Exception as ex:
            logger.error(ex)

    def value(self, key: str) -> str:
        return self.dictionary[key] if self.dictionary is not None else "unknown"


svg_loader = None
if svg_loader is None:
    svg_loader = ImageLoader()

locale = None
if locale is None:
    locale = LocaleUtil()


def load_style(function):
    resources = config.get("resources").replace("${CURRENT}", getcwd()).replace("${HOME}", get_home_path())
    style = join(join(resources, "styles"), config.get("style"))
    if isfile(style):
        with open(style, mode="r", encoding="utf-8") as stylesheet:
            function(stylesheet.read())
        logger.info("Stylesheet found in:", style)


def browse(url: str):
    """
        This function uses the Qt core to open a url in the system's
        default browser.
    """
    QDesktopServices.openUrl(QUrl(url))

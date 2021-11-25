from json import load
from os import getcwd
from os.path import isfile, join

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices, QIcon, QBitmap, QImage
from requests import get

from config import config
from homedir import get_home_path, create_dir
from logger import logger


def browse(url: str):
    """
        This function uses the Qt core to open a url in the system's
        default browser.
    """
    QDesktopServices.openUrl(QUrl(url))


def load_remote_file(url: str):
    file_path = join(create_dir("cache"), url.split("/")[-1])
    if not isfile(file_path):
        remote_file = open(file=file_path, mode="w", encoding="utf-8")
        data = get(url)
        remote_file.write(data.content.decode("utf-8"))
        data.close()
        remote_file.close()
    return file_path


def load_style(function):
    resources = config.get("transclip.resources.path").replace("${CURRENT}", getcwd()).replace("${HOME}", get_home_path())
    style = join(join(resources, "styles"), config.get("transclip.style"))
    if isfile(style):
        with open(style, mode="r", encoding="utf-8") as stylesheet:
            function(stylesheet.read())
        logger.info(f"Stylesheet found in: {style}")


class ImageLoader:

    def __init__(self):
        super(ImageLoader, self).__init__()
        self.image_dir = None
        res_config: str = config.get("transclip.resources.path")
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
        resources = config.get("transclip.resources.path").replace("${CURRENT}", getcwd()).replace("${HOME}", get_home_path())
        file_path = f"{resources}/locales/{config.get('transclip.locale')}"
        if isfile(file_path):
            print("Dictionary found in:", file_path)
            file = open(file_path, mode="r", encoding="utf-8")
            self.dictionary = load(file)
            file.close()
        else:
            file_path = load_remote_file(f"https://raw.githubusercontent.com/jhondevcode/Transclip-qt/master/src"
                                         f"/resources/locales/{config.get('transclip.locale')}")
            logger.info(f"Dictionary downloaded from: {file_path}")
            file = open(file=file_path, mode="r", encoding="utf-8")
            try:
                self.dictionary = load(file)
            except Exception as err:
                logger.error(err)
            file.close()

    def value(self, key: str) -> str:
        return self.dictionary[key] if self.dictionary is not None else "unknown"


svg_loader = None
if svg_loader is None:
    svg_loader = ImageLoader()

locale = None
if locale is None:
    locale = LocaleUtil()

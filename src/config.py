"""
"""

import sqlite3 as sql
import sys
from typing import Dict
from os.path import join, isfile

from requests import get

from homedir import get_home_path
from impl import AbstractLoader
from logger import logger


class Configuration(AbstractLoader):

    def __init__(self):
        super(Configuration, self).__init__()
        self.__config = {}
        self._to_save: Dict[str, str] = {}
        self.load()

    def load(self):
        try:
            db_file = join(get_home_path(), "config.db")
            if not isfile(db_file):
                connection = sql.connect(db_file)
                cursor = connection.cursor()
                cursor.execute('CREATE TABLE "config" ("id"	INTEGER NOT NULL, "key"	TEXT NOT NULL, "value"	TEXT NOT '
                               'NULL, PRIMARY KEY("id" AUTOINCREMENT))')
                self.load_default()
                for key, value in self.__config.items():
                    cursor.execute(f'INSERT INTO "config" (key, value) VALUES ("{key}", "{value}")')
                connection.commit()
                cursor.close()
                connection.close()
            else:
                connection = sql.connect(db_file)
                cursor = connection.cursor()
                cursor.execute("SELECT key, value FROM config")
                rows = cursor.fetchall()
                for row in rows:
                    self.__config[row[0]] = row[1]
                cursor.close()
                connection.close()
        except Exception as ex:
            logger.error(ex)
            self.load_default()

    def register_configs(self, stream: list):
        """
            This method is in charge of processing and validating the content
            of the properties file
        """
        for line in stream:
            if (line != '\n' or line[0] != '#') and '=' in line:
                try:
                    key, value = line.replace("\n", "").split("=")
                    self.__config[key] = value
                except ValueError as ex:
                    logger.error(ex)

    def load_default(self):
        # loading default configuration
        try:
            default = open("resources/other/default_config.txt")
            lines = default.readlines()
            default.close()
            self.register_configs(lines)
        except Exception as ex:
            logger.error(ex)
            try:
                # loading default configuration from github
                data = get("https://raw.githubusercontent.com/jhondevcode/Transclip-qt/master/src/resources/other/default_config.txt")
                lines = data.content.decode("utf-8")
                data.close()
                lines = lines.split("\n")
                del lines[-1]
                self.register_configs(lines)
            except Exception as ex:
                logger.error(ex)
                sys.exit(-1)

    def save(self) -> bool:
        have_error = False
        connection = None
        cursor = None
        if len(self._to_save):
            try:
                connection = sql.connect(join(get_home_path(), "config.db"))
                cursor = connection.cursor()
                # cursor.execute("UPDATE config SET value")

                for key, value in self._to_save.items():
                    try:
                        cursor.execute(f'UPDATE config SET value="{value}" WHERE key="{key}"')
                    except Exception as ex:
                        logger.error(ex)
                        connection.rollback()
                        have_error = True
                        break
                connection.commit()
                # cursor.close()
                # connection.close()
            except Exception as ex:
                logger.error(ex)
                have_error = True
                if connection:
                    connection.rollback()
            finally:
                if cursor:
                    cursor.close()

                if connection:
                    connection.close()
        return have_error

    def get(self, key: str):
        try:
            return self.__config[key]
        except KeyError as err:
            logger.error(err)
            return None
    
    def get_bool(self, key: str) -> bool:
        try:
            return True if self.get(key) == 'True' else False
        except Exception as err:
            logger.error(err)
            return False

    def get_float(self, key: str) -> float:
        try:
            return float(self.get(key))
        except Exception as err:
            logger.error(err)
            return 0.0

    def get_int(self, key: str) -> int:
        try:
            return int(self.get(key))
        except Exception as err:
            logger.error(err)
            return 0

    def get_string(self, key: str) -> str:
        try:
            return str(self.get(key))
        except Exception as err:
            logger.error(err)
            return ""

    def set(self, key: str, value: str):
        self.__config[key] = value

    def clean_to_save(self):
        self._to_save.clear()

    def add_to_save(self, key: str, value: str):
        self._to_save[key] = value


config = None
if config is None:
    config = Configuration()

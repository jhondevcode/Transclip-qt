"""
"""

import sqlite3 as sql
from os.path import join, isfile

from homedir import get_home_path
from impl import AbstractLoader
from logger import logger


class Configuration(AbstractLoader):

    def __init__(self):
        super(Configuration, self).__init__()
        self.__config = {}
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

    def load_default(self):
        # loading default configuration
        default = open("resources/other/default_config.txt")
        lines = default.readlines()
        default.close()
        for line in lines:
            pair = line.replace("\n", "").split("=")
            self.__config[pair[0]] = pair[1]

    def save(self):
        try:
            connection = sql.connect(join(get_home_path(), "config.db"))
            cursor = connection.cursor()
            cursor.execute("UPDATE config SET value")
            for key, value in self.__config.items():
                cursor.execute(f'UPDATE config SET value="{value}" WHERE key="{key}"')
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as ex:
            logger.error(ex)

    def get(self, key: str):
        return self.__config[key]

    def set(self, key: str, value: str):
        self.__config[key] = value


config = None
if config is None:
    config = Configuration()

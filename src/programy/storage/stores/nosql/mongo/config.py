"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.config.base import BaseConfigurationData
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.utils.logging.ylogger import YLogger
from programy.utils.substitutions.substitues import Substitutions


class MongoStorageConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="config")

        self._url = "mongodb://localhost:27017/"
        self._database = "programy"
        self._drop_all_first = False

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    @property
    def drop_all_first(self):
        return self._drop_all_first

    @drop_all_first.setter
    def drop_all_first(self, drop_all):
        self._drop_all_first = drop_all

    def create_mongostorage_config(self):
        return {
            "url": self._url,
            "database": self._database,
            "drop_all_first": self._drop_all_first,
        }

    def load_config_section(
        self, configuration_file, configuration, bot_root, subs: Substitutions = None
    ):
        del bot_root
        del subs
        storage = configuration_file.get_section(self._section_name, configuration)
        if storage is not None:
            self._url = configuration_file.get_option(storage, "url")
            self._database = configuration_file.get_option(storage, "database")
            self._drop_all_first = configuration_file.get_option(
                storage, "drop_all_first"
            )
        else:
            YLogger.error(None, "'config' section missing from storage config")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["url"] = "mongodb://localhost:27017/"
            data["database"] = "programy"
            data["drop_all_first"] = True
        else:
            data["url"] = self._url
            data["database"] = self._database
            data["drop_all_first"] = self._drop_all_first

    def create_engine(self):
        engine = MongoStorageEngine(self)
        engine.initialise()
        return engine

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
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.utils.logging.ylogger import YLogger
from programy.utils.substitutions.substitues import Substitutions


class RedisStorageConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="config")

        self._host = "localhost"
        self._port = 6379
        self._password = None
        self._db = 0
        self._prefix = "programy"
        self._drop_all_first = True

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def password(self):
        return self._password

    @property
    def db(self):
        return self._db

    @property
    def prefix(self):
        return self._prefix

    @property
    def drop_all_first(self):
        return self._drop_all_first

    def load_config_section(
        self, configuration_file, configuration, bot_root, subs: Substitutions = None
    ):
        del bot_root
        del subs
        storage = configuration_file.get_section(self._section_name, configuration)
        if storage is not None:
            self._host = configuration_file.get_option(storage, "host")
            self._port = configuration_file.get_option(storage, "port")
            self._password = configuration_file.get_option(storage, "password")
            self._db = configuration_file.get_option(storage, "db")
            self._prefix = configuration_file.get_option(storage, "prefix")
            self._drop_all_first = configuration_file.get_option(
                storage, "drop_all_first"
            )
        else:
            YLogger.error(None, "'config' section missing from storage config")

    def create_redisstorage_config(self):
        return {
            "host": self._host,
            "port": self._port,
            "password": self._password,
            "db": self._db,
            "prefix": self._prefix,
            "drop_all_first": self._drop_all_first,
        }

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["host"] = "localhost"
            data["port"] = 6379
            data["password"] = None
            data["db"] = 0
            data["prefix"] = "programy"
            data["drop_all_first"] = True
        else:
            data["host"] = self._host
            data["port"] = self._port
            data["password"] = self._password
            data["db"] = self._db
            data["prefix"] = self._prefix
            data["drop_all_first"] = self._drop_all_first

    def create_engine(self):
        engine = RedisStorageEngine(self)
        engine.initialise()
        return engine

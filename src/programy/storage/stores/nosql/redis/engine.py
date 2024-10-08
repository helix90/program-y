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

import redis

from programy.storage.engine import StorageEngine
from programy.storage.stores.nosql.redis.store.conversations import (
    RedisConversationStore,
)
from programy.utils.logging.ylogger import YLogger


class RedisStorageEngine(StorageEngine):

    def __init__(self, configuration):
        StorageEngine.__init__(self, configuration)
        self._prefix = "programy"  # Default value
        self._sessions_set_key = self._create_sessions_set_key()
        self._redis = None

    @property
    def redis(self):
        return self._redis

    @property
    def prefix(self):
        return self._prefix

    @property
    def sessions_set_key(self):
        return self._sessions_set_key

    def _create_sessions_set_key(self):
        return "{prefix}:sessions".format(prefix=self._prefix)

    def initialise(self):
        self._prefix = self.configuration.prefix
        self._sessions_set_key = self._create_sessions_set_key()

        if self.configuration.password is not None:
            self._redis = redis.StrictRedis(
                host=self.configuration.host,
                port=self.configuration.port,
                password=self.configuration.password,
                db=self.configuration.db,
            )
        else:
            self._redis = redis.StrictRedis(
                host=self.configuration.host,
                port=self.configuration.port,
                db=self.configuration.db,
            )

        if self.configuration.drop_all_first is True:
            try:
                self.conversation_store().empty()
            except Exception as excep:
                YLogger.exception(
                    self, "Failed deleting conversation redis data - ", excep
                )

    def conversation_store(self):
        return RedisConversationStore(self)

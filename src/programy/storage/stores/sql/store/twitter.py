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

from programy.storage.entities.twitter import TwitterStore
from programy.storage.stores.sql.dao.twitter import Twitter
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.utils.logging.ylogger import YLogger


class SQLTwitterStore(SQLStore, TwitterStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        TwitterStore.__init__(self)

    def _get_all(self):
        return self._storage_engine.session.query(Twitter)

    def empty(self):
        return self._get_all()

    def store_last_message_ids(self, last_direct_message_id, last_status_id):
        ids = Twitter(
            last_direct_message_id=last_direct_message_id, last_status_id=last_status_id
        )
        self._storage_engine.session.query(Twitter).delete()
        self._storage_engine.session.add(ids)

    def load_last_message_ids(self):
        twitter = self._storage_engine.session.query(Twitter)
        try:
            ids = twitter.one()
            return ids.last_direct_message_id, ids.last_status_id

        except Exception as error:
            YLogger.exception(self, "Failed to find previous message ids", error)

        return "-1", "-1"

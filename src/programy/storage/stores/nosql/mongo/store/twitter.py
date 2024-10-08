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
from programy.storage.stores.nosql.mongo.dao.twitter import Twitter
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.utils.logging.ylogger import YLogger


class MongoTwitterStore(MongoStore, TwitterStore):
    TWITTER = "twitter"

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)
        TwitterStore.__init__(self)

    def collection_name(self):
        return MongoTwitterStore.TWITTER

    def store_last_message_ids(self, last_direct_message_id, last_status_id):
        YLogger.info(
            self,
            "Storing last message ids (%s, %s) to Mongo",
            last_direct_message_id,
            last_status_id,
        )

        collection = self.collection()
        twitter = collection.find_one({})
        if twitter is not None:
            twitter["last_direct_message_id"] = last_direct_message_id
            twitter["last_status_id"] = last_status_id
            result = collection.replace_one({"_id": twitter["_id"]}, twitter)
            return bool(result.modified_count > 0)

        else:
            twitter = Twitter(last_direct_message_id, last_status_id)
            return self.add_document(twitter)

    def load_last_message_ids(self):
        YLogger.info(self, "Loading last message ids from Mongo")

        collection = self.collection()
        twitter = collection.find_one({})
        if twitter is not None:
            return twitter["last_direct_message_id"], twitter["last_status_id"]

        else:
            return "-1", "-1"

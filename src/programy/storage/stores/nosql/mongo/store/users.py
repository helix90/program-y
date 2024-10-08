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

from programy.storage.entities.user import UserStore
from programy.storage.stores.nosql.mongo.dao.user import User
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.utils.logging.ylogger import YLogger


class MongoUserStore(MongoStore, UserStore):
    USERS = "users"
    USERID = "userid"
    CLIENT = "client"

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)
        UserStore.__init__(self)

    def collection_name(self):
        return MongoUserStore.USERS

    def add_user(self, userid, clientid):
        YLogger.info(self, "Adding user [%s] for client [%s]", userid, clientid)
        user = User(userid, clientid)
        return self.add_document(user)

    def exists(self, userid, clientid):
        collection = self.collection()
        user = collection.find_one(
            {MongoUserStore.USERID: userid, MongoUserStore.CLIENT: clientid}
        )
        return bool(user is not None)

    def get_links(self, userid):
        collection = self.collection()
        users = collection.find({MongoUserStore.USERID: userid})
        links = []
        for user in users:
            links.append(user["client"])
        return links

    def _remove_user_from_db(self, userid, clientid):
        collection = self.collection()
        result = collection.delete_many(
            {MongoUserStore.USERID: userid, MongoUserStore.CLIENT: clientid}
        )
        return bool(result.deleted_count > 0)

    def remove_user(self, userid, clientid):
        try:
            return self._remove_user_from_db(userid, clientid)

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to remove user", excep)

        return False

    def _remove_user_from_all_clients_from_db(self, userid):
        collection = self.collection()
        result = collection.delete_many({MongoUserStore.USERID: userid})
        return bool(result.deleted_count > 0)

    def remove_user_from_all_clients(self, userid):
        try:
            return self._remove_user_from_all_clients_from_db(userid)

        except Exception as excep:
            YLogger.exception_nostack(
                self, "Failed to remove user from all clients", excep
            )

        return False

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
from programy.storage.stores.sql.dao.user import User
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.utils.logging.ylogger import YLogger


class SQLUserStore(SQLStore, UserStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        UserStore.__init__(self)

    def _get_all(self):
        return self._storage_engine.session.query(User)

    def empty(self):
        self._get_all().delete()

    def add_user(self, userid, clientid):
        user = User(userid=userid, client=clientid)
        self._storage_engine.session.add(user)
        return user

    def exists(self, userid, clientid):
        try:
            self._storage_engine.session.query(User).filter(
                User.userid == userid, User.client == clientid
            ).one()
            return True
        except Exception:
            return False

    def get_links(self, userid):
        links = []
        db_users = self._storage_engine.session.query(User).filter(
            User.userid == userid
        )
        for user in db_users:
            links.append(user.client)
        return links

    def _remove_user_from_db(self, userid, clientid):
        rowcount = (
            self._storage_engine.session.query(User)
            .filter(User.userid == userid, User.client == clientid)
            .delete()
        )
        return bool(rowcount > 0)

    def remove_user(self, userid, clientid):
        try:
            return self._remove_user_from_db(userid, clientid)

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to remove user", excep)

        return False

    def _remove_user_from_all_clients_from_db(self, userid):
        rowcount = (
            self._storage_engine.session.query(User)
            .filter(User.userid == userid)
            .delete()
        )
        return bool(rowcount > 0)

    def remove_user_from_all_clients(self, userid):
        try:
            return self._remove_user_from_all_clients_from_db(userid)

        except Exception as excep:
            YLogger.exception_nostack(
                self, "Failed to remove user from all clients", excep
            )

        return False

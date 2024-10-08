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

from sqlalchemy import and_

from programy.storage.entities.link import LinkStore
from programy.storage.stores.sql.dao.link import Link
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.utils.logging.ylogger import YLogger


class SQLLinkStore(SQLStore, LinkStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        LinkStore.__init__(self)

    def _get_all(self):
        return self._storage_engine.session.query(Link)

    def empty(self):
        self._get_all().delete()

    def create_link(
        self,
        primary_userid,
        provided_key,
        generated_key,
        expires,
        expired=False,
        retry_count=0,
    ):
        link = Link(
            primary_user=primary_userid,
            generated_key=generated_key,
            provided_key=provided_key,
            expires=expires,
            expired=expired,
            retry_count=retry_count,
        )
        self._storage_engine.session.add(link)
        return link

    def get_link(self, userid):
        try:
            link = (
                self._storage_engine.session.query(Link)
                .filter(Link.primary_user == userid)
                .one()
            )
            return link

        except Exception as e:
            YLogger.exception_nostack(self, "Failed to get link", e)

        return None

    def _delete_link(self, userid):
        result = (
            self._storage_engine.session.query(Link)
            .filter(Link.primary_user == userid)
            .delete()
        )
        return bool(result == 1)

    def remove_link(self, userid):
        try:
            return self._delete_link(userid)

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to remove link", excep)

        return False

    def link_exists(self, userid, provided_key, generated_key):
        try:
            self._storage_engine.session.query(Link).filter(
                Link.primary_user == userid,
                Link.provided_key == provided_key,
                Link.generated_key == generated_key,
            ).one()
            return True

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to check link exists", excep)
            return False

    def _get_link(self, id):
        return (
            self._storage_engine.session.query(Link).filter(and_(Link.id == id)).one()
        )

    def update_link(self, link):
        existing = self._get_link(link.id)
        if existing is not None:
            existing.primary_user = link.primary_user
            existing.generated_key = link.generated_key
            existing.provided_key = link.provided_key
            existing.expired = link.expired
            existing.expires = link.expires
            existing.retry_count = link.retry_count

            self._storage_engine.session.commit()
            return True

        return False

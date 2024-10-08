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

from programy.storage.entities.sets import SetsReadWriteStore
from programy.storage.stores.sql.dao.set import Set
from programy.storage.stores.sql.store.sqlstore import SQLStore


class SQLSetsStore(SQLStore, SetsReadWriteStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        SetsReadWriteStore.__init__(self)

    def _get_all(self):
        return self._storage_engine.session.query(Set)

    def empty(self):
        self._get_all().delete()

    def empty_named(self, name):
        self._storage_engine.session.query(Set).filter(Set.name == name).delete()

    def add_to_set(self, name, value, replace_existing=False):
        aset = Set(name=name, value=value.upper())
        self._storage_engine.session.add(aset)
        return True

    def remove_from_set(self, name, value):
        result = (
            self._storage_engine.session.query(Set)
            .filter(Set.name == name, Set.value == value.upper())
            .delete()
        )
        if result == 0:
            return False

        return True

    def load_all(self, collector):
        collector.empty()
        names = self._storage_engine.session.query(Set.name).distinct()
        for name in names:
            self.load(collector, name[0])

    def load(self, collector, name=None):
        collector.remove(name)
        values = self._storage_engine.session.query(Set).filter(Set.name == name)
        the_set = {}
        for pair in values:
            value = pair.value.strip()
            self.add_set_values(the_set, value)

        if the_set:
            collector.add_set(name, the_set, SQLStore.SQL)
            return True

        return False

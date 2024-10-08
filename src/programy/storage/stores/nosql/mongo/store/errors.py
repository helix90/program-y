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

from programy.storage.entities.errors import ErrorsStore
from programy.storage.stores.nosql.mongo.dao.duplicate import Duplicate
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.utils.logging.ylogger import YLogger


class MongoErrorsStore(MongoStore, ErrorsStore):
    ERRORS = "errors"

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)
        ErrorsStore.__init__(self)

    def collection_name(self):
        return MongoErrorsStore.ERRORS

    def save_errors(self, errors, commit=True):
        YLogger.info(self, "Saving errors to Mongo")
        for duplicate in errors:
            db_duplicate = Duplicate(
                duplicate=duplicate[0],
                file=duplicate[1],
                start=duplicate[2],
                end=duplicate[3],
            )
            self.add_document(db_duplicate)

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

from programy.storage.entities.learnf import LearnfStore
from programy.storage.stores.sql.dao.category import Category
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.utils.logging.ylogger import YLogger


class SQLLearnfStore(SQLStore, LearnfStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        LearnfStore.__init__(self)

    def _get_all(self):
        raise Exception("Learnf _get_all not possible, call Category _get_all instead!")

    def save_learnf(self, client_context, category):
        YLogger.debug(
            self,
            "Storing learnf category in Mongo [%s] [%s] [%s] [%s] [%s] [%s]",
            client_context.client.id,
            client_context.userid,
            category.pattern,
            category.topic,
            category.that,
            category.template,
        )

        # pattern = category.pattern
        # topic = category.topic
        # that = category.that
        # template = category.template
        # Changes
        pattern = category.pattern.text
        topic = category.topic.text
        that = category.that.text
        template = category.template.resolve(client_context)
        # End Changes

        groupid = "LEARNF"
        userid = client_context.userid

        category = Category(
            groupid=groupid,
            userid=userid,
            pattern=pattern,
            topic=topic,
            that=that,
            template=template,
        )
        self.storage_engine.session.add(category)

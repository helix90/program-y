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

from programy.storage.entities.nodes import NodesStore
from programy.storage.entities.store import Store
from programy.storage.stores.nosql.mongo.dao.node import PatternNode, TemplateNode
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.utils.classes.loader import ClassLoader
from programy.utils.logging.ylogger import YLogger


class MongoNodeStore(MongoStore, NodesStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)
        NodesStore.__init__(self)

    def load(self, collector, name=None):
        YLogger.info(self, "Loading %s nodes from Mongo", self.collection_name())
        nodes = self.get_all_nodes()
        for node in nodes:
            try:
                collector.add_node(
                    node["name"], ClassLoader.instantiate_class(node["node_class"])
                )

            except Exception as excep:
                YLogger.exception(
                    self,
                    "Failed pre-instantiating %s Node [%s]",
                    excep,
                    collector.type,
                    node["node_class"],
                )

    def get_all_nodes(self):
        collection = self.collection()
        return collection.find()

    def _load_nodes_from_file(self, filename, verbose):
        count = 0
        success = 0
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if self.process_config_line(line, verbose) is True:
                    success += 1
                count += 1
        return count, success

    def upload_from_file(
        self, filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=False
    ):

        YLogger.info(
            self,
            "Uploading %s to Mongo from file [%s]",
            self.collection_name(),
            filename,
        )
        try:
            return self._load_nodes_from_file(filename, verbose)

        except Exception as excep:
            YLogger.exception(self, "Error loading file [%s]", excep, filename)

        return 0, 0

    def process_config_line(self, line, verbose=False):
        line = line.strip()
        if line.startswith("#") is False:
            splits = line.split("=")
            if len(splits) > 1:
                node_name = splits[0].strip()
                class_name = splits[1].strip()
                node = self._get_entity(node_name, class_name)
                if verbose is True:
                    YLogger.debug(
                        self, "Loading node [%s] = [%s]", node_name, class_name
                    )
                return self.add_document(node)

        return False

    def _get_entity(self, name, classname):
        raise NotImplementedError()  # pragma: no cover


class MongoPatternNodeStore(MongoNodeStore):
    PATTERN_NODES = "pattern_nodes"

    def __init__(self, storage_engine):
        MongoNodeStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoPatternNodeStore.PATTERN_NODES

    def _get_entity(self, name, classname):
        return PatternNode(name, classname)


class MongoTemplateNodeStore(MongoNodeStore):
    TEMPLATE_NODES = "template_nodes"

    def __init__(self, storage_engine):
        MongoNodeStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoTemplateNodeStore.TEMPLATE_NODES

    def _get_entity(self, name, classname):
        return TemplateNode(name, classname)

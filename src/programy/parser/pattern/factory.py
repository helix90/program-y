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

import os

from programy.parser.factory import NodeFactory
from programy.storage.factory import StorageFactory
from programy.utils.classes.loader import ClassLoader
from programy.utils.logging.ylogger import YLogger


class PatternNodeFactory(NodeFactory):

    def __init__(self):
        NodeFactory.__init__(self, "Pattern")

    def default_config_file(self):
        return os.path.dirname(__file__) + os.sep + "pattern_nodes.conf"

    def get_root_node(self):
        try:
            root_class = self.new_node_class("root")
            return root_class()

        except Exception as excep:
            YLogger.exception_nostack(
                self, "Failed to get root pattern node, reverting to default", excep
            )
            return ClassLoader.instantiate_class(
                "programy.parser.pattern.nodes.root.PatternRootNode"
            )()

    def load(self, storage_factory):
        if (
            storage_factory.entity_storage_engine_available(
                StorageFactory.PATTERN_NODES
            )
            is True
        ):
            storage_engine = storage_factory.entity_storage_engine(
                StorageFactory.PATTERN_NODES
            )
            pattern_store = storage_engine.pattern_nodes_store()
            pattern_store.load(self)
        else:
            YLogger.error(None, "No storage engine available for pattern_nodes!")

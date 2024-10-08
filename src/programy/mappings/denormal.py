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

from programy.mappings.base import DoubleStringPatternSplitCollection
from programy.storage.factory import StorageFactory
from programy.utils.logging.ylogger import YLogger


class DenormalCollection(DoubleStringPatternSplitCollection):

    def __init__(self):
        DoubleStringPatternSplitCollection.__init__(self)

    def denormalise(self, normal):
        if self.has_key(normal):
            return self.value(normal)
        return None

    def denormalise_string(self, string):
        return self.replace_by_pattern(string)

    def _load_collection(self, lookups_engine):
        lookups_store = lookups_engine.denormal_store()
        lookups_store.load_all(self)

    def load(self, storage_factory):
        if (
            storage_factory.entity_storage_engine_available(StorageFactory.DENORMAL)
            is True
        ):
            lookups_engine = storage_factory.entity_storage_engine(
                StorageFactory.DENORMAL
            )
            try:
                self._load_collection(lookups_engine)
                return True

            except Exception as e:
                YLogger.exception(self, "Failed to load lookups from storage", e)

        return False

    def reload(self, storage_factory):
        return self.load(storage_factory)

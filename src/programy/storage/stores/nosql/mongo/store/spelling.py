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

from programy.storage.entities.spelling import SpellingStore
from programy.storage.entities.store import Store
from programy.storage.stores.nosql.mongo.dao.corpus import Corpus
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.utils.console.console import outputLog
from programy.utils.logging.ylogger import YLogger


class MongoSpellingStore(MongoStore, SpellingStore):
    SPELLING = "spelling"

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)
        SpellingStore.__init__(self)

    def collection_name(self):
        return MongoSpellingStore.SPELLING

    def _read_corpus_from_file(self, filename, verbose):
        corpus_words = []
        with open(filename, "r") as text_file:
            for lines in text_file:
                words = lines.split(" ")
                for word in words:
                    corpus_words.append(word)

        corpus = Corpus(words=corpus_words)
        if self.add_document(corpus) is False:
            return 0, 0

        count = len(corpus_words)
        return count, count

    def upload_from_file(
        self, filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=False
    ):

        YLogger.info(self, "Uplading spelling corpus file [%s] to Mongo", filename)

        count = success = 0
        try:
            count, success = self._read_corpus_from_file(filename, verbose)

        except Exception as excep:
            YLogger.exception(
                self, "Failed to load spelling corpus from [%s]", excep, filename
            )

        # Assume all words loaded are success, no need for additional count
        return count, success

    def load_spelling(self, spell_checker):
        YLogger.info(self, "Loading spelling corpus from Mongo")

        collection = self.collection()
        corpus = collection.find_one({})
        if corpus is not None:
            spell_checker.add_corpus(" ".join(corpus["words"]))

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
import os.path

from programy.storage.entities.spelling import SpellingStore
from programy.storage.stores.file.store.filestore import FileStore
from programy.utils.logging.ylogger import YLogger


class FileSpellingStore(FileStore, SpellingStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)
        SpellingStore.__init__(self)

    def _get_storage_path(self):
        return self.storage_engine.configuration.spelling_storage.file

    def get_storage(self):
        return self.storage_engine.configuration.spelling_storage

    def _load_corpus_from_file(self, filename, encoding, spell_checker):
        with open(filename, encoding=encoding) as words_file:
            all_words = words_file.read()
            spell_checker.add_corpus(all_words)

    def load_spelling(self, spell_checker):
        corpus_filename = self.get_storage().file
        encoding = self.get_storage().encoding

        YLogger.info(self, "Loading spelling corpus [%s]", corpus_filename)
        try:
            self._load_corpus_from_file(corpus_filename, encoding, spell_checker)
            return True

        except Exception as e:
            YLogger.exception_nostack(
                self, "Failed to load corpus [%s]", e, corpus_filename
            )

        return False

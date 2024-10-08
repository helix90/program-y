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

from programy.storage.entities.license import LicenseStore
from programy.storage.stores.file.store.filestore import FileStore
from programy.utils.logging.ylogger import YLogger


class FileLicenseStore(FileStore, LicenseStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)
        LicenseStore.__init__(self)

    def _get_storage_path(self):
        return self.storage_engine.configuration.license_storage.file

    def get_storage(self):
        return self.storage_engine.configuration.license_storage

    def _load_file_contents(self, collection, filename):
        try:
            YLogger.info(self, "Loading license key file: [%s]", filename)
            with open(filename, "r", encoding="utf-8") as license_file:
                for line in license_file:
                    self._process_license_key_line(collection, line)

        except Exception as excep:
            YLogger.exception_nostack(
                self, "Invalid license key file [%s]", excep, filename
            )

    def _process_license_key_line(self, license_collection, line):
        line = line.strip()
        if line and line.startswith("#") is False:
            splits = line.split("=")
            if len(splits) > 1:
                key_name = splits[0].strip()
                # If key has = signs in it, then combine all elements past the first
                key = "".join(splits[1:]).strip()
                license_collection.add_key(key_name, key)
                return True

            else:
                YLogger.warning(self, "Invalid license key [%s]", line)

        return False

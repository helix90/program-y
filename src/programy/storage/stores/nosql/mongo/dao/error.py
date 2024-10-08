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

from programy.storage.stores.utils import DAOUtils


class Error:

    def __init__(self, error, file, start, end):
        self.id = None
        self.error = error
        self.file = file
        self.start = start
        self.end = end

    def __repr__(self):
        return "<Error(id='%s', error='%s', file='%s', start='%s', end='%s')>" % (
            DAOUtils.valid_id(self.id),
            self.error,
            self.file,
            self.start,
            self.end,
        )

    def to_document(self):
        document = {
            "error": self.error,
            "file": self.file,
            "start": self.start,
            "end": self.end,
        }
        if self.id is not None:
            document["_id"] = self.id
        return document

    @staticmethod
    def from_document(data):
        error = Error(None, None, None, None)
        error.id = DAOUtils.get_value_from_data(data, "_id")
        error.error = DAOUtils.get_value_from_data(data, "error")
        error.file = DAOUtils.get_value_from_data(data, "file")
        error.start = DAOUtils.get_value_from_data(data, "start")
        error.end = DAOUtils.get_value_from_data(data, "end")
        return error

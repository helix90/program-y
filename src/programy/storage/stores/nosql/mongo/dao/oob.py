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


class OOB:

    def __init__(self, name, oob_class):
        self.id = None
        self.name = name
        self.oob_class = oob_class

    def to_document(self):
        document = {"name": self.name, "oob_class": self.oob_class}
        if self.id is not None:
            document["_id"] = self.id
        return document

    def __repr__(self):
        return "<OOB(id='%s', name='%s', oob_class='%s')>" % (
            DAOUtils.valid_id(self.id),
            self.name,
            self.oob_class,
        )

    @staticmethod
    def from_document(data):
        oob = OOB(None, None)
        oob.id = DAOUtils.get_value_from_data(data, "_id")
        oob.name = DAOUtils.get_value_from_data(data, "name")
        oob.oob_class = DAOUtils.get_value_from_data(data, "oob_class")
        return oob

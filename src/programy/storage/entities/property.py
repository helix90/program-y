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

from programy.storage.entities.store import Store


class PropertyStore(Store):

    def __init__(self):
        Store.__init__(self)

    def empty_properties(self):
        raise NotImplementedError(
            "empty_properties missing from User Store"
        )  # pragma: no cover

    def add_property(self, name, value):
        raise NotImplementedError(
            "add_property missing from User Store"
        )  # pragma: no cover

    def add_properties(self, properties):
        raise NotImplementedError(
            "add_properties missing from User Store"
        )  # pragma: no cover

    def get_properties(self):
        raise NotImplementedError(
            "get_properties missing from Property Store"
        )  # pragma: no cover

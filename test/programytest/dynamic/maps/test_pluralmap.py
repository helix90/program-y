import unittest

from programytest.client import TestClient

from programy.context import ClientContext
from programy.dynamic.maps.plural import PluralMap


class TestPluralMaps(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")

    def test_static_map(self):
        map = PluralMap(None)
        self.assertEqual("MICE", map.map_value(self._client_context, "MOUSE"))

    def test_singular_y_to_plural(self):
        map = PluralMap(None)
        self.assertEqual("HOLLIES", map.map_value(self._client_context, "HOLLY"))

    def test_singular_s_to_plural(self):
        map = PluralMap(None)
        self.assertEqual("COWS", map.map_value(self._client_context, "COW"))

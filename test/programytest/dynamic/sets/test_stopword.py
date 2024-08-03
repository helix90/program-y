import unittest

from programytest.client import TestClient

from programy.context import ClientContext
from programy.dynamic.sets.stopword import IsStopWord


class IsStopWordDynamicSetTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")

    def test_is_stopword(self):
        dyn_var = IsStopWord(None)
        self.assertIsNotNone(dyn_var)
        self.assertTrue(dyn_var.is_member(self._client_context, "is"))
        self.assertFalse(dyn_var.is_member(self._client_context, "Python"))
        self.assertFalse(dyn_var.is_member(self._client_context, None))

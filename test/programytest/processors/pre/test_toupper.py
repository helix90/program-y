import unittest

from programytest.client import TestClient

from programy.context import ClientContext
from programy.processors.pre.toupper import ToUpperPreProcessor


class ToUpperTests(unittest.TestCase):

    def test_to_upper(self):
        processor = ToUpperPreProcessor()

        context = ClientContext(TestClient(), "testid")

        result = processor.process(context, "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("HELLO", result)

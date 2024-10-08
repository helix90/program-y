import unittest

from programytest.client import TestClient

from programy.processors.pre.stemming import StemmingPreProcessor


class StemmingTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()

    def test_to_stemming(self):
        processor = StemmingPreProcessor()

        context = self.client.create_client_context("testid")

        result = processor.process(context, "My troubles with cats")
        self.assertIsNotNone(result)
        self.assertEqual("My troubl with cat", result)

import unittest

from programytest.client import TestClient

from programy.processors.pre.stopwords import StopWordsPreProcessor


class StopWordsTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()

    def test_to_stopwords(self):
        processor = StopWordsPreProcessor()

        context = self.client.create_client_context("testid")

        result = processor.process(context, "This is a cat")
        self.assertIsNotNone(result)
        self.assertEqual("This cat", result)

import unittest

from programytest.client import TestClient

from programy.context import ClientContext
from programy.processors.pre.removepunctuation import RemovePunctuationPreProcessor


class RemovePunctuationTests(unittest.TestCase):

    def test_remove_punctuation(self):
        processor = RemovePunctuationPreProcessor()

        context = ClientContext(TestClient(), "testid")

        result = processor.process(context, "'Hello'")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

        result = processor.process(context, "$100")
        self.assertIsNotNone(result)
        self.assertEqual("$100", result)

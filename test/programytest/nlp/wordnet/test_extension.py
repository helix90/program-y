import unittest

from programytest.client import TestClient

from programy.nlp.wordnet.extension import WordNetExtension


class WordNetExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")

    def test_get_definition(self):
        extension = WordNetExtension()
        self.assertIsNotNone(extension)
        self.assertEqual(
            "feline mammal usually having thick soft fur and no ability to roar: domestic cats; wildcats",
            extension.execute(self.context, "CAT"),
        )

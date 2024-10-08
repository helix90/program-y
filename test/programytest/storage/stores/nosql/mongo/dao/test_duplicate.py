import unittest

from programy.storage.stores.nosql.mongo.dao.duplicate import Duplicate


class DuplicateTests(unittest.TestCase):

    def test_init_no_id(self):
        duplicate = Duplicate(
            duplicate="This is a duplicate", file="afile", start="300", end="500"
        )

        self.assertIsNotNone(duplicate)
        self.assertIsNone(duplicate.id)
        self.assertEqual("This is a duplicate", duplicate.duplicate)
        self.assertEqual("afile", duplicate.file)
        self.assertEqual("300", duplicate.start)
        self.assertEqual("500", duplicate.end)
        self.assertEqual(
            {
                "duplicate": "This is a duplicate",
                "end": "500",
                "file": "afile",
                "start": "300",
            },
            duplicate.to_document(),
        )

    def test_init_with_id(self):
        duplicate = Duplicate(
            duplicate="This is a duplicate", file="afile", start="300", end="500"
        )
        duplicate.id = "666"

        self.assertIsNotNone(duplicate)
        self.assertIsNotNone(duplicate.id)
        self.assertEqual("666", duplicate.id)
        self.assertEqual("This is a duplicate", duplicate.duplicate)
        self.assertEqual("afile", duplicate.file)
        self.assertEqual("300", duplicate.start)
        self.assertEqual("500", duplicate.end)
        self.assertEqual(
            {
                "_id": "666",
                "duplicate": "This is a duplicate",
                "end": "500",
                "file": "afile",
                "start": "300",
            },
            duplicate.to_document(),
        )

    def test_from_document_no_id(self):
        duplicate1 = Duplicate.from_document(
            {
                "duplicate": "This is a duplicate",
                "end": "500",
                "file": "afile",
                "start": "300",
            }
        )
        self.assertIsNotNone(duplicate1)
        self.assertIsNone(duplicate1.id)
        self.assertEqual("This is a duplicate", duplicate1.duplicate)
        self.assertEqual("afile", duplicate1.file)
        self.assertEqual("300", duplicate1.start)
        self.assertEqual("500", duplicate1.end)

    def test_from_document_with_id(self):
        duplicate2 = Duplicate.from_document(
            {
                "_id": "666",
                "duplicate": "This is a duplicate",
                "end": "500",
                "file": "afile",
                "start": "300",
            }
        )
        self.assertIsNotNone(duplicate2)
        self.assertIsNotNone(duplicate2.id)
        self.assertEqual("666", duplicate2.id)
        self.assertEqual("This is a duplicate", duplicate2.duplicate)
        self.assertEqual("afile", duplicate2.file)
        self.assertEqual("300", duplicate2.start)
        self.assertEqual("500", duplicate2.end)

    def test_from_document_with_no_data(self):
        duplicate2 = Duplicate.from_document({"_id": "666"})
        self.assertIsNotNone(duplicate2)
        self.assertIsNotNone(duplicate2.id)
        self.assertEqual("666", duplicate2.id)
        self.assertIsNone(duplicate2.duplicate)
        self.assertIsNone(duplicate2.file)
        self.assertIsNone(duplicate2.start)
        self.assertIsNone(duplicate2.end)

    def test_repr_no_id(self):
        duplicate1 = Duplicate.from_document(
            {
                "duplicate": "This is a duplicate",
                "end": "500",
                "file": "afile",
                "start": "300",
            }
        )
        self.assertEquals(
            "<Duplicate(id='n/a', duplicate='This is a duplicate', file='afile', start='300', end='500')>",
            str(duplicate1),
        )

    def test_repr_id(self):
        duplicate2 = Duplicate.from_document(
            {
                "_id": "666",
                "duplicate": "This is a duplicate",
                "end": "500",
                "file": "afile",
                "start": "300",
            }
        )
        self.assertEquals(
            "<Duplicate(id='666', duplicate='This is a duplicate', file='afile', start='300', end='500')>",
            str(duplicate2),
        )

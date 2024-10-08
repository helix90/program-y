import unittest

from programy.storage.stores.nosql.mongo.dao.error import Error


class ErrorTests(unittest.TestCase):

    def test_init_no_id(self):
        error = Error(error="This is a error", file="afile", start="300", end="500")

        self.assertIsNotNone(error)
        self.assertIsNone(error.id)
        self.assertEqual("This is a error", error.error)
        self.assertEqual("afile", error.file)
        self.assertEqual("300", error.start)
        self.assertEqual("500", error.end)
        self.assertEqual(
            {"error": "This is a error", "end": "500", "file": "afile", "start": "300"},
            error.to_document(),
        )

    def test_init_with_id(self):
        error = Error(error="This is a error", file="afile", start="300", end="500")
        error.id = "666"

        self.assertIsNotNone(error)
        self.assertIsNotNone(error.id)
        self.assertEqual("666", error.id)
        self.assertEqual("This is a error", error.error)
        self.assertEqual("afile", error.file)
        self.assertEqual("300", error.start)
        self.assertEqual("500", error.end)
        self.assertEqual(
            {
                "_id": "666",
                "error": "This is a error",
                "end": "500",
                "file": "afile",
                "start": "300",
            },
            error.to_document(),
        )

    def test_from_document_no_id(self):
        error1 = Error.from_document(
            {"error": "This is a error", "end": "500", "file": "afile", "start": "300"}
        )
        self.assertIsNotNone(error1)
        self.assertIsNone(error1.id)
        self.assertEqual("This is a error", error1.error)
        self.assertEqual("afile", error1.file)
        self.assertEqual("300", error1.start)
        self.assertEqual("500", error1.end)

    def test_from_document_with_id(self):
        error2 = Error.from_document(
            {
                "_id": "666",
                "error": "This is a error",
                "end": "500",
                "file": "afile",
                "start": "300",
            }
        )
        self.assertIsNotNone(error2)
        self.assertIsNotNone(error2.id)
        self.assertEqual("666", error2.id)
        self.assertEqual("This is a error", error2.error)
        self.assertEqual("afile", error2.file)
        self.assertEqual("300", error2.start)
        self.assertEqual("500", error2.end)

    def test_from_document_with_no_data(self):
        error2 = Error.from_document({"_id": "666"})
        self.assertIsNotNone(error2)
        self.assertIsNotNone(error2.id)
        self.assertEqual("666", error2.id)
        self.assertIsNone(error2.error)
        self.assertIsNone(error2.file)
        self.assertIsNone(error2.start)
        self.assertIsNone(error2.end)

    def test_repr_no_id(self):
        error1 = Error.from_document(
            {"error": "This is a error", "end": "500", "file": "afile", "start": "300"}
        )
        self.assertEquals(
            "<Error(id='n/a', error='This is a error', file='afile', start='300', end='500')>",
            str(error1),
        )

    def test_repr_with_id(self):
        error2 = Error.from_document(
            {
                "_id": "666",
                "error": "This is a error",
                "end": "500",
                "file": "afile",
                "start": "300",
            }
        )
        self.assertEquals(
            "<Error(id='666', error='This is a error', file='afile', start='300', end='500')>",
            str(error2),
        )

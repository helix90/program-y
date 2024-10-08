import os
import os.path
import re

from programytest.storage.asserts.store.assert_normals import NormalsStoreAsserts

from programy.mappings.normal import NormalCollection
from programy.storage.stores.file.config import (
    FileStorageConfiguration,
    FileStoreConfiguration,
)
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.lookups import FileNormalStore


class FileNormalStoreTests(NormalsStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileNormalStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileNormalStore(engine)

        self.assertEquals("/tmp/lookups/normal.txt", store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_load_from_file(self):
        config = FileStorageConfiguration()
        config._normal_storage = FileStoreConfiguration(
            file=os.path.dirname(__file__)
            + os.sep
            + "data"
            + os.sep
            + "lookups"
            + os.sep
            + "text"
            + os.sep
            + "normal.txt",
            fileformat="text",
            encoding="utf-8",
            delete_on_start=False,
        )
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileNormalStore(engine)

        normal_collection = NormalCollection()

        store.load(normal_collection)

        self.assertEqual(
            normal_collection.normalise(".COM"),
            [re.compile("(^\\.COM|\\.COM|\\.COM$)", re.IGNORECASE), " DOT COM "],
        )
        self.assertEqual(
            normal_collection.normalise_string("keith.com"), "keith dot com"
        )

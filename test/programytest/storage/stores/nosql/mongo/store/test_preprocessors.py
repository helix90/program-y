import unittest
from unittest.mock import patch

import programytest.storage.engines as Engines
from programytest.storage.asserts.store.assert_preprocessors import (
    PreProcessorsStoreAsserts,
)

from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.processors import MongoPreProcessorStore


class MongoPreProcessorStoreTests(PreProcessorsStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPreProcessorStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_load(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPreProcessorStore(engine)

        self.assert_load(store)

    @staticmethod
    def patch_instantiate_class(class_string):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch(
        "programy.utils.classes.loader.ClassLoader.instantiate_class",
        patch_instantiate_class,
    )
    def test_load_exception(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPreProcessorStore(engine)

        self.assert_load_exception(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPreProcessorStore(engine)

        self.assert_upload_from_file(store, verbose=False)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file_verbose(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPreProcessorStore(engine)

        self.assert_upload_from_file(store, verbose=True)

    def patch_load_processors_from_file(self, filename, verbose):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch(
        "programy.storage.stores.nosql.mongo.store.processors.MongoProcessorStore._load_processors_from_file",
        patch_load_processors_from_file,
    )
    def test_upload_from_file_exception(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPreProcessorStore(engine)

        self.assert_upload_from_file_exception(store)

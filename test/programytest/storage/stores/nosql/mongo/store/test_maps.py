import unittest

import programytest.storage.engines as Engines
from programytest.storage.asserts.store.assert_maps import MapStoreAsserts

from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.maps import MongoMapsStore


class MongoMapsStoreTests(MapStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_map_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_map_storage(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_text(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_upload_from_text(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_text_files_from_directory_no_subdir(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_upload_text_files_from_directory_no_subdir(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_text_files_from_directory_with_subdir(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_upload_text_files_from_directory_with_subdir(store, "mongo")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_csv_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_upload_from_csv_file(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_csv_files_from_directory_with_subdir(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_upload_csv_files_from_directory_with_subdir(store, "mongo")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_empty_named(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_empty_named(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_add_to_map_overwrite_existing(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_add_to_map_overwrite_existing(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_add_to_map_no_overwrite_existing(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_add_to_map_overwrite_existing(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_load_no_map_found(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_load_no_map_found(store)

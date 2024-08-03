import unittest
from unittest.mock import patch

import programytest.storage.engines as Engines
from programytest.storage.asserts.store.assert_genders import GenderStoreAsserts

from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.lookups import SQLGenderStore


class SQLGenderStoreTests(GenderStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLGenderStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_lookup_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLGenderStore(engine)

        self.assert_lookup_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_text(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLGenderStore(engine)

        self.assert_upload_from_text(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_text_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLGenderStore(engine)

        self.assert_upload_from_text_file(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_csv_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLGenderStore(engine)

        self.assert_upload_csv_file(store)

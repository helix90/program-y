import unittest

import programytest.storage.engines as Engines
from programytest.storage.asserts.store.assert_rdfs import RDFStoreAsserts

from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.rdfs import SQLRDFsStore


class SQLRDFsStoreTests(RDFStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRDFsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_rdf_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRDFsStore(engine)

        self.assert_rdf_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_empty_named(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRDFsStore(engine)

        self.assert_empty_named(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_text(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRDFsStore(engine)

        self.assert_upload_from_text(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRDFsStore(engine)

        self.assert_load(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_all(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRDFsStore(engine)

        self.assert_load_all(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_text_files_from_directory_no_subdir(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRDFsStore(engine)

        self.assert_upload_text_files_from_directory_no_subdir(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_csv_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRDFsStore(engine)

        self.assert_upload_from_csv_file(
            store,
        )

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_csv_files_from_directory_with_subdir(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRDFsStore(engine)

        self.assert_upload_csv_files_from_directory_with_subdir(store)

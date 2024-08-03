import unittest

import programytest.storage.engines as Engines
from programytest.storage.asserts.store.assert_twitter import TwitterStoreAsserts

from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.twitter import SQLTwitterStore


class SQLTwitterStoreTests(TwitterStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLTwitterStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_twitter_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLTwitterStore(engine)

        self.assert_twitter_storage(store)

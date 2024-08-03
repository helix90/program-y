import unittest
import unittest.mock

from programytest.storage.test_utils import StorageEngineTestUtils

from programy.storage.stores.logger.config import LoggerStorageConfiguration
from programy.storage.stores.logger.engine import LoggerStorageEngine


class LoggerStorageEngineTests(StorageEngineTestUtils):

    def test_init_with_configuration(self):
        config = unittest.mock.Mock
        engine = LoggerStorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)

    def test_conversations(self):
        config = LoggerStorageConfiguration()
        engine = LoggerStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(storage_engine=engine, visit=False)

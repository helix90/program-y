import os
import re
import unittest

from programytest.client import TestClient

from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext
from programy.processors.processing import PostQuestionProcessorCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import (
    FileStorageConfiguration,
    FileStoreConfiguration,
)
from programy.storage.stores.file.engine import FileStorageEngine


class PostQuestionProcessingTests(unittest.TestCase):

    def test_load(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._postquestionprocessors_storage = FileStoreConfiguration(
            file=os.path.dirname(__file__)
            + os.sep
            + "test_files"
            + os.sep
            + "postquestionprocessors.conf",
            fileformat="text",
            extension="txt",
            encoding="utf-8",
            delete_on_start=False,
        )

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.POSTQUESTIONPROCESSORS] = (
            storage_engine
        )
        storage_factory._store_to_engine_map[StorageFactory.POSTQUESTIONPROCESSORS] = (
            storage_engine
        )

        collection = PostQuestionProcessorCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory))

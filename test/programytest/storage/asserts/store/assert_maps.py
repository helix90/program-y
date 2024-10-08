import os
import os.path
import unittest

from programy.mappings.maps import MapCollection
from programy.storage.entities.store import Store


class MockMapCollection(object):

    def __init__(self):
        self.maps = {}

    def empty(self):
        self.maps.clear()

    def remove(self, name):
        self.maps.pop(name, None)

    def add_map(self, map_name, the_map, store):
        self.maps[map_name] = the_map


class MapStoreAsserts(unittest.TestCase):

    def assert_map_storage(self, store):
        store.empty()

        store.add_to_map("TESTMAP1", "Key1", "Val1")
        store.add_to_map("TESTMAP1", "Key2", "Val2")
        store.add_to_map("TESTMAP1", "Key3", "Val3")
        store.add_to_map("TESTMAP2", "Key1", "Val1")
        store.commit()

        map_collection = MockMapCollection()
        store.load_all(map_collection)
        self.assertEqual(2, len(map_collection.maps.keys()))
        self.assertTrue("TESTMAP1" in map_collection.maps)
        self.assertTrue("Val1", map_collection.maps["TESTMAP1"]["Key1"])
        self.assertTrue("Val2", map_collection.maps["TESTMAP1"]["Key2"])
        self.assertTrue("Val3", map_collection.maps["TESTMAP1"]["Key3"])
        self.assertTrue("TESTMAP2" in map_collection.maps)
        self.assertTrue("Val1", map_collection.maps["TESTMAP2"]["Key1"])

        self.assertTrue(store.remove_from_map("TESTMAP1", "Key1"))
        self.assertTrue(store.remove_from_map("TESTMAP2", "Key1"))
        self.assertFalse(store.remove_from_map("TESTMAP2", "Key666"))
        self.assertFalse(store.remove_from_map("TESTMAP3", "Key1"))
        store.commit()

        map_collection = MockMapCollection()
        store.load_all(map_collection)
        self.assertEqual(1, len(map_collection.maps.keys()))
        self.assertTrue("TESTMAP1" in map_collection.maps)
        self.assertTrue("Val2", map_collection.maps["TESTMAP1"]["Key2"])
        self.assertTrue("Val3", map_collection.maps["TESTMAP1"]["Key3"])
        self.assertFalse("TESTMAP2" in map_collection.maps)

    def assert_upload_from_text(self, store):
        store.empty()

        store.upload_from_text(
            "TESTMAP",
            """
        ant:6
        bat:2
        bear:4
        bee:6
        bird:2
        """,
        )

        map_collection = MapCollection()
        store.load(map_collection, "TESTMAP")

        self.assertTrue(map_collection.contains("TESTMAP"))
        map = map_collection.map("TESTMAP")
        self.assertIsNotNone(map)
        self.assertTrue("ANT" in map)
        self.assertEqual("6", map["ANT"])

    def assert_upload_text_files_from_directory_no_subdir(self, store):
        store.empty()

        store.upload_from_directory(
            os.path.dirname(__file__)
            + os.sep
            + "data"
            + os.sep
            + "maps"
            + os.sep
            + "text",
            subdir=False,
        )

        map_collection = MapCollection()
        store.load_all(map_collection)

        self.assertTrue(map_collection.contains("TESTMAP"))
        map = map_collection.map("TESTMAP")
        self.assertIsNotNone(map)
        self.assertTrue("ANT" in map)
        self.assertEqual("6", map["ANT"])

    def assert_upload_text_files_from_directory_with_subdir(self, store, filestore):
        store.empty()

        store.upload_from_directory(
            os.path.dirname(__file__)
            + os.sep
            + "data"
            + os.sep
            + "maps"
            + os.sep
            + "text",
            subdir=True,
        )

        map_collection = MapCollection()
        store.load_all(map_collection)

        self.assertTrue(map_collection.contains("TESTMAP"))
        map = map_collection.map("TESTMAP")
        self.assertIsNotNone(map)
        self.assertTrue("ANT" in map)
        self.assertEqual("6", map["ANT"])

        self.assertTrue(map_collection.contains("TESTMAP2"))
        self.assertEqual(filestore, map_collection.storename("TESTMAP2"))
        map = map_collection.map("TESTMAP2")
        self.assertIsNotNone(map)
        self.assertTrue("BIRD" in map)
        self.assertEqual("TWEET", map["BIRD"])

    def assert_upload_from_csv_file(self, store):
        store.empty()

        store.upload_from_file(
            os.path.dirname(__file__)
            + os.sep
            + "data"
            + os.sep
            + "maps"
            + os.sep
            + "csv"
            + os.sep
            + "testmap.csv",
            fileformat=Store.CSV_FORMAT,
        )

        map_collection = MapCollection()
        store.load(map_collection, "TESTMAP")

        self.assertTrue(map_collection.contains("TESTMAP"))
        map = map_collection.map("TESTMAP")
        self.assertIsNotNone(map)
        self.assertTrue("ANT" in map)
        self.assertEqual("6", map["ANT"])

    def assert_upload_csv_files_from_directory_with_subdir(self, store, filestore):

        store.empty()

        store.upload_from_directory(
            os.path.dirname(__file__)
            + os.sep
            + "data"
            + os.sep
            + "maps"
            + os.sep
            + "csv",
            fileformat=Store.CSV_FORMAT,
        )

        map_collection = MapCollection()
        store.load_all(map_collection)

        self.assertTrue(map_collection.contains("TESTMAP"))
        map = map_collection.map("TESTMAP")
        self.assertIsNotNone(map)
        self.assertTrue("ANT" in map)
        self.assertEqual("6", map["ANT"])

        self.assertTrue(map_collection.contains("TESTMAP2"))
        self.assertEqual(filestore, map_collection.storename("TESTMAP2"))
        map = map_collection.map("TESTMAP2")
        self.assertIsNotNone(map)
        self.assertTrue("BIRD" in map)
        self.assertEqual("FEATHERS", map["BIRD"])

    def assert_empty_named(self, store):
        store.empty()

        store.upload_from_text(
            "TESTMAP",
            """
        ant:6
        bat:2
        bear:4
        bee:6
        bird:2
        """,
        )

        map_collection = MapCollection()
        store.load(map_collection, "TESTMAP")

        self.assertTrue(map_collection.contains("TESTMAP"))

        store.empty_named("TESTMAP")

        map_collection.empty()
        self.assertFalse(store.load(map_collection, "TESTMAP"))

        self.assertFalse(map_collection.contains("TESTMAP"))

    def assert_add_to_map_overwrite_existing(self, store):
        store.add_to_map("TESTMAP", "key1", "value1", overwrite_existing=True)
        store.add_to_map("TESTMAP", "key2", "value2", overwrite_existing=True)
        store.add_to_map("TESTMAP", "key2", "value3", overwrite_existing=True)

        map_collection = MapCollection()
        store.load(map_collection, "TESTMAP")

        self.assertEqual(1, len(map_collection.maps.keys()))
        self.assertTrue("TESTMAP" in map_collection.maps)
        self.assertTrue("val1", map_collection.maps["TESTMAP"]["key1"])
        self.assertTrue("val3", map_collection.maps["TESTMAP"]["key2"])

    def assert_add_to_map_no_overwrite_existing(self, store):

        store.add_to_map("TESTMAP", "key1", "value1", overwrite_existing=False)
        store.add_to_map("TESTMAP", "key2", "value2", overwrite_existing=False)
        store.add_to_map("TESTMAP", "key2", "value3", overwrite_existing=False)

        map_collection = MapCollection()
        store.load(map_collection, "TESTMAP")

        self.assertEqual(1, len(map_collection.maps.keys()))
        self.assertTrue("TESTMAP" in map_collection.maps)
        self.assertTrue("val1", map_collection.maps["TESTMAP"]["key1"])
        self.assertTrue("val2", map_collection.maps["TESTMAP"]["key2"])

    def assert_load_no_map_found(self, store):
        store.add_to_map("TESTMAP", "key1", "value1", overwrite_existing=False)
        store.add_to_map("TESTMAP", "key2", "value2", overwrite_existing=False)
        store.add_to_map("TESTMAP", "key2", "value3", overwrite_existing=False)

        map_collection = MapCollection()
        self.assertTrue(store.load(map_collection, "TESTMAP"))

        map_collection2 = MapCollection()
        self.assertFalse(store.load(map_collection2, "TESTMAP2"))

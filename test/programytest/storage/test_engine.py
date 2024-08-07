import unittest
import unittest.mock

from programy.storage.engine import StorageEngine, StorageEngineException


class StorageEngineTests(unittest.TestCase):

    def test_test_initialise_with_config_not_implemented(self):

        config = unittest.mock.Mock()

        engine = StorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)
        self.assertEqual(engine.configuration, config)

    def test_user_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.user_store()

    def test_linked_account_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.linked_account_store()

    def test_link_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.link_store()

    def test_category_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.category_store()

    def test_errors_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.errors_store()

    def test_duplicates_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.duplicates_store()

    def test_learnf_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.learnf_store()

    def test_conversation_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.conversation_store()

    def test_sets_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.sets_store()

    def test_maps_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.maps_store()

    def test_rdf_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.rdf_store()

    def test_denormal_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.denormal_store()

    def test_normal_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.normal_store()

    def test_gender_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.gender_store()

    def test_person_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.person_store()

    def test_person2_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.person2_store()

    def test_regex_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.regex_store()

    def test_property_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.property_store()

    def test_twitter_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.twitter_store()

    def test_spelling_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.spelling_store()

    def test_license_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.license_store()

    def test_pattern_nodes_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.pattern_nodes_store()

    def test_template_nodes_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.template_nodes_store()

    def test_binaries_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.binaries_store()

    def test_braintree_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.braintree_store()

    def test_preprocessors_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.preprocessors_store()

    def test_postprocessors_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.postprocessors_store()

    def test_postquestionprocessors_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.postquestionprocessors_store()

    def test_usergroups_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.usergroups_store()

    def test_triggers_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.triggers_store()

    def test_defaults_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.defaults_store()

    def test_variables_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(StorageEngineException):
            _ = engine.variables_store()

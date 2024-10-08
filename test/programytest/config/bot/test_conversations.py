import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.bot.conversations import BotConversationsConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.utils.license.keys import LicenseKeys


class BotConversationsConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        bot:
            conversations:
              max_histories: 666
              initial_topic: topic1
              restore_last_topic: true
              multi_client: true
        
        """,
            ConsoleConfiguration(),
            ".",
        )

        bot_config = yaml.get_section("bot")

        convo_config = BotConversationsConfiguration()
        convo_config.load_config_section(yaml, bot_config, ".")

        license_keys = LicenseKeys()
        convo_config.check_for_license_keys(license_keys)

        self.assertEqual(convo_config.section_name, "conversations")

        self.assertEqual(666, convo_config.max_histories)
        self.assertEqual("topic1", convo_config.initial_topic)
        self.assertTrue(convo_config.restore_last_topic)
        self.assertTrue(convo_config.multi_client)

    def test_with_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        bot:
            conversations:
        """,
            ConsoleConfiguration(),
            ".",
        )

        bot_config = yaml.get_section("bot")

        convo_config = BotConversationsConfiguration()
        convo_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual(convo_config.section_name, "conversations")

        self.assertEqual(100, convo_config.max_histories)
        self.assertEqual("*", convo_config.initial_topic)
        self.assertFalse(convo_config.restore_last_topic)
        self.assertFalse(convo_config.multi_client)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        bot:
        """,
            ConsoleConfiguration(),
            ".",
        )

        bot_config = yaml.get_section("bot")

        convo_config = BotConversationsConfiguration()
        convo_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual(convo_config.section_name, "conversations")

        self.assertEqual(100, convo_config.max_histories)
        self.assertEqual("*", convo_config.initial_topic)
        self.assertFalse(convo_config.restore_last_topic)
        self.assertFalse(convo_config.multi_client)

    def test_defaults(self):
        convo_config = BotConversationsConfiguration()
        data = {}
        convo_config.to_yaml(data, True)

        BotConversationsConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertEqual(data["max_histories"], 100)
        test.assertEqual(data["restore_last_topic"], True)
        test.assertEqual(data["initial_topic"], "*")
        test.assertEqual(data["empty_on_start"], True)
        test.assertEqual(data["multi_client"], False)

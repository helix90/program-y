import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.bot.bot import BotConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class ConsoleConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        console:
          default_userid: console
          prompt: $
        """,
            ConsoleConfiguration(),
            ".",
        )

        config = ConsoleConfiguration()
        config.load_configuration(yaml, ".")

        self.assertEqual("console", config.default_userid)
        self.assertEqual("$", config.prompt)

        self.assertIsNotNone(config.configurations)
        self.assertEqual(1, len(config.configurations))
        self.assertIsInstance(config.configurations[0], BotConfiguration)

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        console:
        """,
            ConsoleConfiguration(),
            ".",
        )

        config = ConsoleConfiguration()
        config.load_configuration(yaml, ".")

        self.assertIsNotNone(config.configurations)
        self.assertEqual(1, len(config.configurations))

    def test_to_yaml_with_defaults(self):
        config = ConsoleConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual("console", data["default_userid"])
        self.assertEqual(">>>", data["prompt"])

        self.assertEqual(data["renderer"], "programy.clients.render.text.TextRenderer")

        self.assertTrue("bots" in data)
        self.assertTrue("bot" in data["bots"])
        self.assertEqual(
            data["bot_selector"], "programy.clients.botfactory.DefaultBotSelector"
        )

        self.assertTrue("brains" in data["bots"]["bot"])
        self.assertTrue("brain" in data["bots"]["bot"]["brains"])

    def test_to_yaml_without_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        console:
          default_userid: console
          prompt: $
          bot_selector: programy.clients.botfactory.DefaultBotSelector
          renderer: programy.clients.render.text.TextRenderer
        """,
            ConsoleConfiguration(),
            ".",
        )

        config = ConsoleConfiguration()
        config.load_configuration(yaml, ".")

        data = {}
        config.to_yaml(data, False)

        self.assertEqual("console", data["default_userid"])
        self.assertEqual("$", data["prompt"])

        self.assertEqual(
            data["bot_selector"], "programy.clients.botfactory.DefaultBotSelector"
        )
        self.assertEqual(data["renderer"], "programy.clients.render.text.TextRenderer")

        self.assertTrue("bots" in data)
        self.assertTrue("bot" in data["bots"])
        self.assertEqual(
            data["bot_selector"], "programy.clients.botfactory.DefaultBotSelector"
        )

        self.assertTrue("brains" in data["bots"]["bot"])
        self.assertTrue("brain" in data["bots"]["bot"]["brains"])

    def test_to_yaml_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        other:
        """,
            ConsoleConfiguration(),
            ".",
        )

        config = ConsoleConfiguration()
        config.load_configuration(yaml, ".")

        data = {}
        config.to_yaml(data, False)

        self.assertEqual("console", data["default_userid"])
        self.assertEqual(">>>", data["prompt"])

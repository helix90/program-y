import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.brain.tokenizer import BrainTokenizerConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class BrainTokenizerConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        brain:
            tokenizer:
                classname: programy.utils.language.chinese.ChineseLanguage
        """,
            ConsoleConfiguration(),
            ".",
        )

        brain_config = yaml.get_section("brain")

        tokenizer_config = BrainTokenizerConfiguration()
        tokenizer_config.load_config_section(yaml, brain_config, ".")

        self.assertEqual(
            "programy.utils.language.chinese.ChineseLanguage",
            tokenizer_config.classname,
        )

    def test_with_default_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        brain:
            tokenizer:
                classname: programy.utils.language.default.DefaultLangauge
                split_chars: .:'
        """,
            ConsoleConfiguration(),
            ".",
        )

        brain_config = yaml.get_section("brain")

        tokenizer_config = BrainTokenizerConfiguration()
        tokenizer_config.load_config_section(yaml, brain_config, ".")

        self.assertEqual(
            "programy.utils.language.default.DefaultLangauge",
            tokenizer_config.classname,
        )
        self.assertEqual(".:'", tokenizer_config.split_chars)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        brain:
            tokenizer:
        """,
            ConsoleConfiguration(),
            ".",
        )

        brain_config = yaml.get_section("brain")

        tokenizer_config = BrainTokenizerConfiguration()
        tokenizer_config.load_config_section(yaml, brain_config, ".")

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        brain:
        """,
            ConsoleConfiguration(),
            ".",
        )

        brain_config = yaml.get_section("brain")

        tokenizer_config = BrainTokenizerConfiguration()
        tokenizer_config.load_config_section(yaml, brain_config, ".")

    def test_defaults(self):
        tokenizer_config = BrainTokenizerConfiguration()
        data = {}
        tokenizer_config.to_yaml(data, True)

        BrainTokenizerConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertEqual(
            data["classname"], "programy.dialog.tokenizer.tokenizer.Tokenizer"
        )
        test.assertEqual(data["split_chars"], " ")

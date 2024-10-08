import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.utils.email.config import EmailConfiguration
from programy.utils.license.keys import LicenseKeys


class EmailConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        console:
            email:
                host: 127.0.0.1
                port: 80
                username: emailuser
                password: emailpassword
                from_addr: emailfromuser
        """,
            ConsoleConfiguration(),
            ".",
        )

        client_config = yaml.get_section("console")

        email_config = EmailConfiguration()
        email_config.load_config_section(yaml, client_config, ".")

        license_keys = LicenseKeys()
        email_config.check_for_license_keys(license_keys)

        self.assertEqual("127.0.0.1", email_config.host)
        self.assertEqual(80, email_config.port)
        self.assertEqual("emailuser", email_config.username)
        self.assertEqual("emailpassword", email_config.password)
        self.assertEqual("emailfromuser", email_config.from_addr)

    def test_with_data_no_useridpassword(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        console:
            email:
                host: 127.0.0.1
                port: 80
                from_addr: emailfromuser
        """,
            ConsoleConfiguration(),
            ".",
        )

        client_config = yaml.get_section("console")

        email_config = EmailConfiguration()
        email_config.load_config_section(yaml, client_config, ".")

        license_keys = LicenseKeys()
        email_config.check_for_license_keys(license_keys)

        self.assertEqual("127.0.0.1", email_config.host)
        self.assertEqual(80, email_config.port)
        self.assertIsNone(email_config.username)
        self.assertIsNone(email_config.password)
        self.assertEqual("emailfromuser", email_config.from_addr)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        console:
            email:
        """,
            ConsoleConfiguration(),
            ".",
        )

        client_config = yaml.get_section("email")

        email_config = EmailConfiguration()
        email_config.load_config_section(yaml, client_config, ".")

        self.assertIsNone(email_config.host)
        self.assertIsNone(email_config.port)
        self.assertIsNone(email_config.username)
        self.assertIsNone(email_config.password)
        self.assertIsNone(email_config.from_addr)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        console:
        """,
            ConsoleConfiguration(),
            ".",
        )

        client_config = yaml.get_section("email")

        email_config = EmailConfiguration()
        email_config.load_config_section(yaml, client_config, ".")

        self.assertIsNone(email_config.host)
        self.assertIsNone(email_config.port)
        self.assertIsNone(email_config.username)
        self.assertIsNone(email_config.password)
        self.assertIsNone(email_config.from_addr)

    def test_with_username_for_addr(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        console:
            email:
                host: 127.0.0.1
                port: 80
                username: emailuser
                password: emailpassword
        """,
            ConsoleConfiguration(),
            ".",
        )

        client_config = yaml.get_section("console")

        email_config = EmailConfiguration()
        email_config.load_config_section(yaml, client_config, ".")

        self.assertEquals("emailuser", email_config.from_addr)

    def test_to_yaml_with_defaults(self):
        email_config = EmailConfiguration()
        data = {}
        email_config.to_yaml(data, defaults=True)
        self.assertEquals(
            {
                "from_addr": None,
                "host": None,
                "password": None,
                "port": None,
                "username": None,
            },
            data,
        )

    def test_to_yaml_without_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text(
            """
        console:
            email:
                host: 127.0.0.1
                port: 80
                username: emailuser
                password: emailpassword
        """,
            ConsoleConfiguration(),
            ".",
        )

        client_config = yaml.get_section("console")

        email_config = EmailConfiguration()
        email_config.load_config_section(yaml, client_config, ".")

        data = {}
        email_config.to_yaml(data, defaults=False)
        self.assertEquals(
            {
                "from_addr": "emailuser",
                "host": "127.0.0.1",
                "password": "emailpassword",
                "port": 80,
                "username": "emailuser",
            },
            data,
        )

    def test_defaults(self):
        email_config = EmailConfiguration()
        data = {}
        email_config.to_yaml(data, True)

        EmailConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertIsNone(data["host"])
        test.assertIsNone(data["port"])
        test.assertIsNone(data["username"])
        test.assertIsNone(data["password"])
        test.assertIsNone(data["from_addr"])

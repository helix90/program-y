import unittest

from programytest.client import TestClient

from programy.extensions.energy.usage import EnergyUsageExtension


class EnergyUsageExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")

    def test_usage(self):

        usage = EnergyUsageExtension()
        self.assertIsNotNone(usage)

        result = usage.execute(self.context, "NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0 0 KWh", result)

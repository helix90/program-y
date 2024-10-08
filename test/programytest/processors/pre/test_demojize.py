import unittest

from programytest.client import TestClient

from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext
from programy.processors.pre.demojize import DemojizePreProcessor


class DemoizeTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()

        self.bot = Bot(config=BotConfiguration(), client=self.client)

    def test_demojize(self):
        processor = DemojizePreProcessor()

        context = ClientContext(self.client, "testid")

        self.assertEqual(
            "Python is :thumbs_up:", processor.process(context, "Python is 👍")
        )

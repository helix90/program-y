import unittest

from programytest.client import TestClient

from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext
from programy.processors.pre.normalize import NormalizePreProcessor


class NormalizeTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()

        self.bot = Bot(config=BotConfiguration(), client=self.client)

    def test_normalize(self):
        processor = NormalizePreProcessor()

        context = ClientContext(self.client, "testid")
        context.bot = self.bot
        context.brain = self.bot.brain

        result = processor.process(context, "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

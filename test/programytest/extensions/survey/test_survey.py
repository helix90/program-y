import unittest

from programytest.client import TestClient

from programy.extensions.survey.survey import SurveyExtension


class SurveyExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")

    def test_survey(self):

        minutes = SurveyExtension()
        self.assertIsNotNone(minutes)

        result = minutes.execute(self.context, "Answer1| Answer2")
        self.assertIsNotNone(result)
        self.assertEqual("OK", result)

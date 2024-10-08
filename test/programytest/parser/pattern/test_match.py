import unittest

from programytest.client import TestClient

from programy.parser.pattern.match import Match
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.word import PatternWordNode


class MatcherTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(MatcherTestClient, self).load_storage()
        self.add_default_stores()
        self.add_pattern_nodes_store()


class MatchTests(unittest.TestCase):

    def setUp(self):
        client = MatcherTestClient()
        self._client_context = client.create_client_context("testid")

    def test_string_to_type(self):
        self.assertEquals(0, Match.string_to_type("Word"))
        self.assertEquals(2, Match.string_to_type("Topic"))
        self.assertEquals(3, Match.string_to_type("That"))
        self.assertEquals(-1, Match.string_to_type("Other"))

    def test_match_no_word(self):
        topic = PatternOneOrMoreWildCardNode("*")
        match = Match(Match.TOPIC, topic, None)
        self.assertEqual(Match.TOPIC, match.matched_node_type)
        self.assertEqual(Match.TOPIC, match.matched_node_type)
        self.assertEqual([], match.matched_node_words)
        self.assertEqual(
            "Match=(Topic) Node=(ONEORMORE [*]) Matched=()",
            match.to_string(self._client_context),
        )

    def test_match_word(self):
        topic = PatternOneOrMoreWildCardNode("*")
        match = Match(Match.TOPIC, topic, "Hello")

        self.assertEqual(Match.TOPIC, match.matched_node_type)
        self.assertTrue(match.matched_node_multi_word)
        self.assertTrue(match.matched_node_wildcard)
        self.assertEqual("ONEORMORE [*]", match.matched_node_str)
        self.assertEqual(
            "Match=(Topic) Node=(ONEORMORE [*]) Matched=(Hello)",
            match.to_string(self._client_context),
        )
        self.assertEqual(["Hello"], match.matched_node_words)

    def test_match_multi_word(self):
        topic = PatternOneOrMoreWildCardNode("*")
        match = Match(Match.TOPIC, topic, None)
        match.add_word("Hello")
        match.add_word("World")

        self.assertEqual(Match.TOPIC, match.matched_node_type)
        self.assertTrue(match.matched_node_multi_word)
        self.assertTrue(match.matched_node_wildcard)
        self.assertEqual("ONEORMORE [*]", match.matched_node_str)
        self.assertEqual(
            "Match=(Topic) Node=(ONEORMORE [*]) Matched=(Hello World)",
            match.to_string(self._client_context),
        )
        self.assertEqual(["Hello", "World"], match.matched_node_words)
        self.assertEqual("Hello World", match.joined_words(self._client_context))

    def test_type_to_string(self):
        self.assertEqual("Word", Match.type_to_string(Match.WORD))
        self.assertEqual("Topic", Match.type_to_string(Match.TOPIC))
        self.assertEqual("That", Match.type_to_string(Match.THAT))
        self.assertEqual("Unknown", Match.type_to_string(999))

    def test_to_json_word_node(self):
        word = PatternWordNode("Hello")
        match = Match(Match.WORD, word, "Hello")

        json_data = match.to_json()
        self.assertIsNotNone(json_data)
        self.assertEqual(json_data["type"], "Word")
        self.assertEqual(json_data["node"], "WORD [Hello]")
        self.assertEqual(json_data["words"], ["Hello"])
        self.assertEqual(json_data["multi_word"], False)
        self.assertEqual(json_data["wild_card"], False)

    def test_from_json(self):

        json_data = {
            "type": Match.type_to_string(Match.WORD),
            "node": "WORD [Hello]",
            "words": ["Hello"],
            "multi_word": False,
            "wild_card": False,
        }

        match = Match.from_json(json_data)
        self.assertIsNotNone(match)
        self.assertEqual(Match.WORD, match.matched_node_type)
        self.assertEqual(False, match._matched_node_multi_word)
        self.assertEqual(False, match._matched_node_wildcard)
        self.assertEqual("WORD [Hello]", match._matched_node_str)
        self.assertEqual(["Hello"], match._matched_node_words)

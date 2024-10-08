import xml.etree.ElementTree as ET

from programytest.parser.base import ParserTestsBaseClass

from programy.dialog.conversation import Conversation
from programy.dialog.question import Question
from programy.parser.pattern.match import Match
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.sr import TemplateSrNode


class MockTemplateSrNode(TemplateSrNode):
    def __init__(self):
        TemplateSrNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateSrNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSrNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("", node.resolve(self._client_context))

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateSrNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><sr /></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateSrNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_node_with_star(self):
        root = TemplateNode()
        node = TemplateSrNode()
        root.append(node)

        conversation = Conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)

        question = Question.create_from_text(self._client_context, "How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)

        match = PatternOneOrMoreWildCardNode("*")
        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        context.add_match(Match(Match.WORD, match, "Matched"))
        question.current_sentence()._matched_context = context

        conversation.record_dialog(question)
        self._client_context.bot._conversation_mgr._conversations["testid"] = (
            conversation
        )

        self.assertEqual("Unknown", root.resolve(self._client_context))

    def test_node_with_invalid_index(self):
        root = TemplateNode()
        node = TemplateSrNode()
        root.append(node)

        conversation = Conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)

        question = Question.create_from_text(self._client_context, "How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)

        match = PatternOneOrMoreWildCardNode("*")
        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        context.add_match(Match(Match.TOPIC, match, "Matched"))
        question.current_sentence()._matched_context = context

        conversation.record_dialog(question)
        self._client_context.bot._conversation_mgr._conversations["testid"] = (
            conversation
        )

        self.assertEqual("", root.resolve(self._client_context))

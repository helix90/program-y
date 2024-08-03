from programytest.parser.base import ParserTestsBaseClass

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.link import TemplateLinkNode
from programy.parser.template.nodes.word import TemplateWordNode


class TemplateLinkNodeTests(ParserTestsBaseClass):

    def test_link_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        link = TemplateLinkNode()
        link._text = TemplateWordNode("Servusai.com")
        link._url = TemplateWordNode("http://Servusai.com")

        root.append(link)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual(
            "<link><text>Servusai.com</text><url>http://Servusai.com</url></link>",
            resolved,
        )

        self.assertEqual(
            "<link><text>Servusai.com</text><url>http://Servusai.com</url></link>",
            root.to_xml(self._client_context),
        )

    def test_link_no_url(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        link = TemplateLinkNode()
        link._text = TemplateWordNode("Servusai.com")

        root.append(link)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("<link><text>Servusai.com</text></link>", resolved)
        self.assertEqual(
            "<link><text>Servusai.com</text></link>", root.to_xml(self._client_context)
        )

import xml.etree.ElementTree as ET

from programytest.parser.base import ParserTestsBaseClass

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode


class TemplateWordNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node1 = TemplateWordNode("Hello")
        root.append(node1)
        node2 = TemplateWordNode("World!")
        root.append(node2)
        self.assertEqual(len(root.children), 2)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved, "Hello World!")

        node2.word = "Again!"
        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved, "Hello Again!")

    def test_to_xml(self):
        root = TemplateNode()
        root.append(TemplateWordNode("Hello"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template>Hello</template>", xml_str)

    def test_resolve_no_word(self):
        node = TemplateWordNode(None)
        self.assertEquals("", node.resolve(self._client_context))

    def test_resolve_to_string_no_word(self):
        node = TemplateWordNode(None)
        self.assertEquals("", node.resolve_to_string(self._client_context))

    def test_to_string(self):
        node = TemplateWordNode("Hello")
        self.assertEquals("[WORD]Hello", node.to_string())

    def test_to_string_no_word(self):
        node = TemplateWordNode(None)
        self.assertEquals("[WORD]", node.to_string())

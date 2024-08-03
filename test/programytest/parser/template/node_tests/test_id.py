import xml.etree.ElementTree as ET

from programytest.parser.base import ParserTestsBaseClass

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.id import TemplateIdNode


class TemplateIdNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIdNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual(root.resolve(self._client_context), "testclient")

    def test_node_with_clientid(self):
        self._client_context.client._id = "Test01"
        node = TemplateIdNode()
        self.assertIsNotNone(node)
        self.assertEquals("Test01", node.resolve(self._client_context))

    def test_node_without_clientid(self):
        self._client_context.client._id = None
        node = TemplateIdNode()
        self.assertIsNotNone(node)
        self.assertEquals("", node.resolve(self._client_context))

    def test_to_xml(self):
        root = TemplateNode()
        root.append(TemplateIdNode())

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><id /></template>", xml_str)

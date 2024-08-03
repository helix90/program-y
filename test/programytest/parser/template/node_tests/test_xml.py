import xml.etree.ElementTree as ET

from programytest.parser.base import ParserTestsBaseClass

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.xml import TemplateXMLNode


class MockTemplateXMLNode(TemplateXMLNode):
    def __init__(self):
        TemplateXMLNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateXMLNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        xml = TemplateXMLNode()
        xml._name = "dial"
        root.append(xml)

        xml.append(TemplateWordNode("07777777777"))

        self.assertEqual(len(root.children), 1)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("<dial>07777777777</dial>", resolved)
        self.assertEqual(
            "<dial>07777777777</dial>", xml.resolve_to_string(self._client_context)
        )
        self.assertEquals("[XML]", xml.to_string())

    def test_node_with_attribs(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        xml = TemplateXMLNode()
        xml._name = "dial"
        xml._attribs["leave_message"] = TemplateWordNode("true")
        root.append(xml)

        xml.append(TemplateWordNode("07777777777"))

        self.assertEqual(len(root.children), 1)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual('<dial leave_message="true">07777777777</dial>', resolved)

    def test_node_with_attribs_as_children(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        attrib = TemplateNode()
        attrib.append(TemplateWordNode("true"))

        xml = TemplateXMLNode()
        xml._name = "dial"
        xml._attribs["leave_message"] = attrib
        root.append(xml)

        xml.append(TemplateWordNode("07777777777"))

        self.assertEqual(len(root.children), 1)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual('<dial leave_message="true">07777777777</dial>', resolved)

    def test_to_xml(self):
        root = TemplateNode()
        xml_node = TemplateXMLNode()
        xml_node._name = "dial"
        root.append(xml_node)
        xml_node.append(TemplateWordNode("07777777777"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><dial>07777777777</dial></template>", xml_str)
        self.assertEqual(
            "<dial>07777777777</dial>", xml_node.to_xml(self._client_context)
        )

    def test_to_xml_no_name(self):
        xml = TemplateXMLNode()
        self.assertEquals("", xml.to_xml(self._client_context))

    def test_resolve_no_name(self):
        xml = TemplateXMLNode()
        self.assertEquals("", xml.resolve(self._client_context))

    def test_to_xml_with_attribs(self):
        root = TemplateNode()
        xml = TemplateXMLNode()
        xml._name = "dial"
        xml._attribs["leave_message"] = TemplateWordNode("true")
        root.append(xml)
        xml.append(TemplateWordNode("07777777777"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual(
            '<template><dial leave_message="true">07777777777</dial></template>',
            xml_str,
        )

    def test_to_xml_with_attribs_as_children(self):
        root = TemplateNode()

        attrib = TemplateNode()
        attrib.append(TemplateWordNode("true"))

        xml = TemplateXMLNode()
        xml._name = "dial"
        xml._attribs["leave_message"] = attrib
        root.append(xml)

        xml.append(TemplateWordNode("07777777777"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual(
            '<template><dial leave_message="true">07777777777</dial></template>',
            xml_str,
        )

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateXMLNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

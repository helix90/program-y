from programytest.parser.base import ParserTestsBaseClass

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.split import TemplateSplitNode


class TemplateSplitNodeTests(ParserTestsBaseClass):

    def test_split_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        split = TemplateSplitNode()

        root.append(split)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("<split />", resolved)

        self.assertEqual("<split />", root.to_xml(self._client_context))

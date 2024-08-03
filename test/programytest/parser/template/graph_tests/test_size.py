import xml.etree.ElementTree as ET

from programytest.parser.template.graph_tests.graph_test_client import (
    TemplateGraphTestClient,
)

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.size import TemplateSizeNode


class TemplateGraphSizeTests(TemplateGraphTestClient):

    def test_size(self):
        template = ET.fromstring(
            """
			<template>
				<size />
			</template>
			"""
        )
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateSizeNode)

    def test_size_with_children(self):
        template = ET.fromstring(
            """
			<template>
				<size>Something</size>
			</template>
			"""
        )
        with self.assertRaises(ParserException):
            root = self._graph.parse_template_expression(template)

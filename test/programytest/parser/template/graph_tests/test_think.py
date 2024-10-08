import xml.etree.ElementTree as ET

from programytest.parser.template.graph_tests.graph_test_client import (
    TemplateGraphTestClient,
)

from programy.parser.template.nodes.think import TemplateThinkNode


class TemplateGraphThinkTests(TemplateGraphTestClient):

    def test_think(self):
        template = ET.fromstring(
            """
			<template>
				<think>XYZ</think>
			</template>
			"""
        )
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateThinkNode)

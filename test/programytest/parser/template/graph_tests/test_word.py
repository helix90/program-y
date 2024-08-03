import xml.etree.ElementTree as ET

from programytest.parser.template.graph_tests.graph_test_client import (
    TemplateGraphTestClient,
)

from programy.parser.template.nodes.word import TemplateWordNode


class TemplateGraphWordNodeTests(TemplateGraphTestClient):

    def test_word_only_template(self):
        template = ET.fromstring(
            """
    			<template>HELLO</template>
    			"""
        )
        ast = self._graph.parse_template_expression(template)

        self.assertIsNotNone(ast)
        self.assertEqual(1, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateWordNode)

    def test_words_only_template(self):
        template = ET.fromstring(
            """
			<template>HELLO WORLD</template>
			"""
        )
        ast = self._graph.parse_template_expression(template)

        self.assertIsNotNone(ast)
        self.assertEqual(2, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateWordNode)
        self.assertIsInstance(ast.children[1], TemplateWordNode)

    def test_words_exception(self):
        template = ET.fromstring(
            """
			<template>HELLO WORLD</template>
			"""
        )

        node = TemplateWordNode(None)
        with self.assertRaises(NotImplementedError):
            node.parse_expression(self._graph, template)

import xml.etree.ElementTree as ET

from programytest.parser.template.graph_tests.graph_test_client import (
    TemplateGraphTestClient,
)

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.deletetriple import TemplateDeleteTripleNode


class TemplateGraphDeleteTripleTests(TemplateGraphTestClient):

    def test_delete_triple_type1(self):
        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))
        self._client_context.brain.rdf.add_entity("X", "Y", "Z", "LETTERS")
        self.assertTrue(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

        template = ET.fromstring(
            """
			<template>
			    <deletetriple>
			        <subj>X</subj>
			        <pred>Y</pred>
			        <obj>Z</obj>
			    </deletetriple>
			</template>
			"""
        )

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateDeleteTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

    def test_delete_triple_type2(self):
        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))
        self._client_context.brain.rdf.add_entity("X", "Y", "Z", "LETTERS")
        self.assertTrue(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

        template = ET.fromstring(
            """
			<template>
			    <deletetriple subj="X" pred="Y" obj="Z">
			    </deletetriple>
			</template>
			"""
        )

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateDeleteTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

    def test_delete_triple_type3(self):
        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))
        self._client_context.brain.rdf.add_entity("X", "Y", "Z", "LETTERS")
        self.assertTrue(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

        template = ET.fromstring(
            """
			<template>
			    <deletetriple subj="X" pred="Y" obj="Z" />
			</template>
			"""
        )

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateDeleteTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

    def test_del_triple_missing_subj(self):
        template = ET.fromstring(
            """
			<template>
			    <deletetriple pred="Y" obj="Z" />
			</template>
			"""
        )

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

    def test_del_triple_missing_pred(self):
        template = ET.fromstring(
            """
			<template>
			    <deletetriple subj="X" obj="Z" />
			</template>
			"""
        )

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNone(ast.children[0]._pred)

    def test_del_triple_missing_obj(self):
        template = ET.fromstring(
            """
			<template>
			    <deletetriple subj="X" pred="Y" />
			</template>
			"""
        )

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNone(ast.children[0]._obj)

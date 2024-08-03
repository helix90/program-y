import unittest

from programy.storage.stores.nosql.mongo.dao.node import PatternNode, TemplateNode


class PatternNodeTests(unittest.TestCase):

    def test_init_no_id(self):
        node = PatternNode(name="test", node_class="test.nodeclass")

        self.assertIsNotNone(node)
        self.assertIsNone(node.id)
        self.assertEqual("test", node.name)
        self.assertEqual("test.nodeclass", node.node_class)
        self.assertEqual(
            {"name": "test", "node_class": "test.nodeclass"}, node.to_document()
        )

    def test_init_with_id(self):
        node = PatternNode(name="test", node_class="test.nodeclass")
        node.id = "666"

        self.assertIsNotNone(node)
        self.assertIsNotNone(node.id)
        self.assertEqual("666", node.id)
        self.assertEqual("test", node.name)
        self.assertEqual("test.nodeclass", node.node_class)
        self.assertEqual(
            {"_id": "666", "name": "test", "node_class": "test.nodeclass"},
            node.to_document(),
        )

    def test_from_document_no_id(self):
        node1 = PatternNode.from_document(
            {"name": "test", "node_class": "test.nodeclass"}
        )
        self.assertIsNotNone(node1)
        self.assertIsNone(node1.id)
        self.assertEqual("test", node1.name)
        self.assertEqual("test.nodeclass", node1.node_class)

    def test_from_document_with_id(self):
        node2 = PatternNode.from_document(
            {"_id": "666", "name": "test", "node_class": "test.nodeclass"}
        )
        self.assertIsNotNone(node2)
        self.assertIsNotNone(node2.id)
        self.assertEqual("666", node2.id)
        self.assertEqual("test", node2.name)
        self.assertEqual("test.nodeclass", node2.node_class)

    def test_from_document_no_id(self):
        node1 = PatternNode.from_document(
            {"name": "test", "node_class": "test.nodeclass"}
        )
        self.assertEquals(
            "<PatternNode(id='n/a', name='test', node_class='test.nodeclass')>",
            str(node1),
        )

    def test_from_document_with_id(self):
        node2 = PatternNode.from_document(
            {"_id": "666", "name": "test", "node_class": "test.nodeclass"}
        )
        self.assertEquals(
            "<PatternNode(id='666', name='test', node_class='test.nodeclass')>",
            str(node2),
        )


class TemplateNodeTests(unittest.TestCase):

    def test_init_no_id(self):
        node = TemplateNode(name="test", node_class="test.nodeclass")

        self.assertIsNotNone(node)
        self.assertIsNone(node.id)
        self.assertEqual("test", node.name)
        self.assertEqual("test.nodeclass", node.node_class)
        self.assertEqual(
            {"name": "test", "node_class": "test.nodeclass"}, node.to_document()
        )

    def test_init_with_id(self):
        node = TemplateNode(name="test", node_class="test.nodeclass")
        node.id = "666"

        self.assertIsNotNone(node)
        self.assertIsNotNone(node.id)
        self.assertEqual("666", node.id)
        self.assertEqual("test", node.name)
        self.assertEqual("test.nodeclass", node.node_class)
        self.assertEqual(
            {"_id": "666", "name": "test", "node_class": "test.nodeclass"},
            node.to_document(),
        )

    def test_from_document_no_id(self):
        node1 = TemplateNode.from_document(
            {"name": "test", "node_class": "test.nodeclass"}
        )
        self.assertIsNotNone(node1)
        self.assertIsNone(node1.id)
        self.assertEqual("test", node1.name)
        self.assertEqual("test.nodeclass", node1.node_class)

    def test_from_document_with_id(self):
        node2 = TemplateNode.from_document(
            {"_id": "666", "name": "test", "node_class": "test.nodeclass"}
        )
        self.assertIsNotNone(node2)
        self.assertIsNotNone(node2.id)
        self.assertEqual("666", node2.id)
        self.assertEqual("test", node2.name)
        self.assertEqual("test.nodeclass", node2.node_class)

    def test_repr_no_id(self):
        node1 = TemplateNode.from_document(
            {"name": "test", "node_class": "test.nodeclass"}
        )
        self.assertEquals(
            "<TemplateNode(id='n/a', name='test', node_class='test.nodeclass')>",
            str(node1),
        )

    def test_repr_with_id(self):
        node2 = TemplateNode.from_document(
            {"_id": "666", "name": "test", "node_class": "test.nodeclass"}
        )
        self.assertEquals(
            "<TemplateNode(id='666', name='test', node_class='test.nodeclass')>",
            str(node2),
        )

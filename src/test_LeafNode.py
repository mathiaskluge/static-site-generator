import unittest

from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_value_required(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_to_html_tag_value(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual("<p>This is a paragraph of text.</p>", node.to_html())

    def test_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>', node.to_html()
        )

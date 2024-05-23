import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):

    def test_tag_required(self):
        with self.assertRaises(ValueError):
            ParentNode(children=[LeafNode("b", "Bold text")])

    def test_children_required(self):
        with self.assertRaises(ValueError):
            ParentNode("p")

    def test_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode("p", [])

    def test_to_html(self):
        inner_node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        outer_node = ParentNode("p", [inner_node])
        self.assertEqual(
            '<p><div><b>Bold text</b>Normal text<i>italic text</i>Normal text</div></p>',
            outer_node.to_html()
        )

if __name__ == '__main__':
    unittest.main()

import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from inline_markdown import text_node_to_html_node, split_nodes_delimiter


class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_value(self):
        with self.assertRaises(ValueError):
            text_node_to_html_node(TextNode("This is a text node", "bold"))

    def test_conversion_text(self):
        text = text_node_to_html_node(TextNode("Plain text", TextType.TEXT))
        self.assertEqual(repr(text), repr(LeafNode(None, "Plain text", None)))

    def test_conversion_bold(self):
        text = text_node_to_html_node(TextNode("Bold text", TextType.BOLD))
        self.assertEqual(repr(text), repr(LeafNode("b", "Bold text", None)))

    def test_conversion_italic(self):
        text = text_node_to_html_node(TextNode("Italic text", TextType.ITALIC))
        self.assertEqual(repr(text), repr(LeafNode("i", "Italic text", None)))

    def test_conversion_code(self):
        text = text_node_to_html_node(TextNode("Some code", TextType.CODE))
        self.assertEqual(repr(text), repr(LeafNode("code", "Some code", None)))

    def test_conversion_link(self):
        text = text_node_to_html_node(
            TextNode("Link label", TextType.LINK, "https://www.test.com")
        )
        self.assertEqual(
            repr(text),
            repr(
                LeafNode("a", "Link label", {"href": "https://www.test.com"})
                ),
        )

    def test_conversion_image(self):
        text = text_node_to_html_node(
            TextNode("Alt text", TextType.IMAGE, "https://www.test.com")
        )
        self.assertEqual(
            repr(text),
            repr(
                LeafNode(
                    "img",
                    "",
                    {"src": "https://www.test.com",
                     "alt": "Alt text"}
                    )
            ),
        )


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_invalid_syntax(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [TextNode("`code block", TextType.TEXT)], "`", TextType.CODE
            )

    def test_only_processing_text(self):
        node = [TextNode("_This is text with a word_", TextType.ITALIC)]
        new_nodes = split_nodes_delimiter(node, "_", TextType.BOLD)
        self.assertEqual(node, new_nodes)

    def test_processing(self):
        node = [
            TextNode("This is text with a `code block` word", TextType.TEXT)
            ]
        new_nodes = split_nodes_delimiter(node, "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()

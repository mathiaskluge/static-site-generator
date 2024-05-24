import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from inline_markdown import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


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
            repr(LeafNode("a", "Link label", {"href": "https://www.test.com"})),
        )

    def test_conversion_image(self):
        text = text_node_to_html_node(
            TextNode("Alt text", TextType.IMAGE, "https://www.test.com")
        )
        self.assertEqual(
            repr(text),
            repr(
                LeafNode("img", "", {"src": "https://www.test.com", "alt": "Alt text"})
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
        node = [TextNode("This is text with a `code block` word", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(node, "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


class TestExtractMarkdownImages(unittest.TestCase):

    def test_extraction(self):
        text = "This is text with an ![image](https://test.com/zjjcJKZ.png) and ![another](https://test.com/dfsdkjfd.png)"
        result = [
            (
                "image",
                "https://test.com/zjjcJKZ.png",
            ),
            (
                "another",
                "https://test.com/dfsdkjfd.png",
            ),
        ]
        self.assertEqual(extract_markdown_images(text), result)


class TestExtractMarkdownLinks(unittest.TestCase):

    def test_extraction(self):
        text = "This is text with a [link](https://test.com/zjjcJKZ.png) and [another](https://test.com/dfsdkjfd.png)"
        result = [
            (
                "link",
                "https://test.com/zjjcJKZ.png",
            ),
            (
                "another",
                "https://test.com/dfsdkjfd.png",
            ),
        ]
        self.assertEqual(extract_markdown_links(text), result)


class TestSplitNodesImage(unittest.TestCase):

    def test_processing_mid(self):
        node = TextNode(
            "This is text with an ![image](https://test.com/zjjcJKZ.png) and ![another](https://test.com/dfsdkjfd.png) one",
            TextType.TEXT,
        )
        result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://test.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.IMAGE, "https://test.com/dfsdkjfd.png"),
            TextNode(" one", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image([node]), result)

    def test_processing_start(self):
        node = TextNode(
            "![image](https://test.com/zjjcJKZ.png)![another](https://test.com/dfsdkjfd.png) one",
            TextType.TEXT,
        )
        result = [
            TextNode("image", TextType.IMAGE, "https://test.com/zjjcJKZ.png"),
            TextNode("another", TextType.IMAGE, "https://test.com/dfsdkjfd.png"),
            TextNode(" one", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image([node]), result)

    def test_processing_end(self):
        node = TextNode(
            "Ends with an ![image](https://test.com/zjjcJKZ.png) and ![another](https://test.com/dfsdkjfd.png)",
            TextType.TEXT,
        )
        result = [
            TextNode("Ends with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://test.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.IMAGE, "https://test.com/dfsdkjfd.png"),
        ]
        self.assertEqual(split_nodes_image([node]), result)

    def test_no_image(self):
        node = TextNode("There is no image", TextType.TEXT)
        result = [TextNode("There is no image", TextType.TEXT)]
        self.assertEqual(split_nodes_image([node]), result)


class TestSplitNodesLink(unittest.TestCase):

    def test_processing_mid(self):
        node = TextNode(
            "This is text with a link [label](https://test.com/zjjcJKZ.png) and [labels](https://test.com/dfsdkjfd.png) one",
            TextType.TEXT,
        )
        result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("label", TextType.LINK, "https://test.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("labels", TextType.LINK, "https://test.com/dfsdkjfd.png"),
            TextNode(" one", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link([node]), result)

    def test_processing_start(self):
        node = TextNode(
            "[image](https://test.com/zjjcJKZ.png)[another](https://test.com/dfsdkjfd.png) one",
            TextType.TEXT,
        )
        result = [
            TextNode("image", TextType.LINK, "https://test.com/zjjcJKZ.png"),
            TextNode("another", TextType.LINK, "https://test.com/dfsdkjfd.png"),
            TextNode(" one", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link([node]), result)

    def test_processing_end(self):
        node = TextNode(
            "Ends with an [link](https://test.com/zjjcJKZ.png) and [another](https://test.com/dfsdkjfd.png)",
            TextType.TEXT,
        )
        result = [
            TextNode("Ends with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://test.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.LINK, "https://test.com/dfsdkjfd.png"),
        ]
        self.assertEqual(split_nodes_link([node]), result)

    def test_no_image(self):
        node = TextNode("There is no image", TextType.TEXT)
        result = [TextNode("There is no image", TextType.TEXT)]
        self.assertEqual(split_nodes_link([node]), result)


class TestTextToTextNodes(unittest.TestCase):

    def test_processing(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://test.com/zjjcJKZ.png) and a [link](https://test.com/dfsdkjfd.png)"
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://test.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://test.com/dfsdkjfd.png"),
        ]
        self.assertEqual(result, text_to_textnodes(text))


if __name__ == "__main__":
    unittest.main()

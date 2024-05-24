import unittest
from pathlib import Path

from block_markdown import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
    heading_to_html_node,
    codeblock_to_html_node,
    quote_to_html_node,
    unordered_list_to_html_node,
    ordered_list_to_html_node,
    paragraph_to_html_node,
    markdown_to_html_node,
)
from htmlnode import ParentNode, LeafNode

test_markdown = Path("src/test_markdown.md").read_text()
test_markdown_to_html_nodes = Path("src/test_markdown_to_html_nodes.md").read_text()


class TestMarkdownToBlocks(unittest.TestCase):

    def test_no_markdown(self):
        markdown = ""
        self.assertEqual([""], markdown_to_blocks(markdown))

    def test_single_block(self):
        markdown = "          ###### Heading\nstuff    "
        result = ["###### Heading\nstuff"]
        self.assertEqual(result, markdown_to_blocks(markdown))

    def test_multi_blocks(self):
        result = [
            "This is **bolded** paragraph",
            "*italic* text and `code`\nin the same paragraph.",
            "* This is a list\n* with items",
        ]
        self.assertEqual(result, markdown_to_blocks(test_markdown))


class TestBlockToBlockType(unittest.TestCase):

    def test_heading_h1(self):
        block = "# Somestuff"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_heading_h6(self):
        block = "###### Somestuff"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_heading_linebreak(self):
        block = "###### Somestuff\nSomeStuff"
        with self.assertRaises(Exception):
            block_to_block_type(block)

    def test_code_blocks_multi(self):
        block = "```Code\nCode\nCode```"
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_code_blocks_single(self):
        block = "```Code```"
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_code_block_not_closed(self):
        block = "```Code\nCode\nCode``"
        with self.assertRaises(Exception):
            block_to_block_type(block)

    def test_quotes_single(self):
        block = ">Quote"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_quotes_multi(self):
        block = ">Quote\n>Quote\n>Quote"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_quotes_not_all(self):
        block = ">Quote\n>Quote\nQuote"
        with self.assertRaises(Exception):
            block_to_block_type(block)

    def test_ul_single_star(self):
        block = "* list item"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_ul_single_dash(self):
        block = "- list item"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_ul_multi_star(self):
        block = "* list item\n* list item"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_ul_multi_dash(self):
        block = "- list item\n- list item"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_ul_multi_mixed(self):
        block = "- list item\n* list item"
        with self.assertRaises(Exception):
            block_to_block_type(block)

    def test_ul_multi_not_all(self):
        block = "- list item\nlist item"
        with self.assertRaises(Exception):
            block_to_block_type(block)

    def test_ol_single(self):
        block = "1. list item"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_ol_multi(self):
        block = "1. list item\n2. list item"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_ol_not_all(self):
        block = "1. list item\nlist item"
        with self.assertRaises(Exception):
            block_to_block_type(block)

    def test_paragraph_single(self):
        inputs = [
            "This is some text",
            " #### more strange text",
            " > some text",
            " * stuff",
        ]
        result = BlockType.PARAGRAPH

        for input_text in inputs:
            with self.subTest(input_text=input_text):
                self.assertEqual(result, block_to_block_type(input_text))

    def test_paragraph_multi(self):
        inputs = [
            "This is some text\ntest",
        ]
        result = BlockType.PARAGRAPH

        for input_text in inputs:
            with self.subTest(input_text=input_text):
                self.assertEqual(result, block_to_block_type(input_text))


class TestHeadingToHTMLNode(unittest.TestCase):

    def test_single_text(self):
        block = "### Heading"
        result = ParentNode("h3", [LeafNode(None, "Heading", None)])
        self.assertEqual(repr(result), repr(heading_to_html_node(block)))

    def test_single_styled(self):
        block = "###### **Bold** *Heading*"
        result = ParentNode(
            "h6",
            [
                LeafNode("b", "Bold", None),
                LeafNode(None, " ", None),
                LeafNode("i", "Heading", None),
            ],
        )
        self.assertEqual(repr(result), repr(heading_to_html_node(block)))


class TestCodeBlockToHTMLNode(unittest.TestCase):

    def test_codeblock(self):
        block = "```x = 'hi'\nprint('Hi')```"
        result = ParentNode(
            "pre", [ParentNode("code", [LeafNode(None, "x = 'hi'\nprint('Hi')")])]
        )
        self.assertEqual(repr(result), repr(codeblock_to_html_node(block)))


class TestQuoteToHTMLNode(unittest.TestCase):

    def test_quote(self):
        block = ">Line 1\n>**bold line 2**\n>Some *italic* in the middle"
        result = ParentNode(
            "blockquote",
            [
                LeafNode(None, "Line 1\n"),
                LeafNode("b", "bold line 2"),
                LeafNode(None, "\nSome "),
                LeafNode("i", "italic"),
                LeafNode(None, " in the middle"),
            ],
        )
        self.assertEqual(repr(result), repr(quote_to_html_node(block)))


class TestListsToHTMLNodes(unittest.TestCase):

    def test_ul_dots(self):
        block = "* list item 1\n* list item 2"
        result = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "list item 1")]),
                ParentNode("li", [LeafNode(None, "list item 2")]),
            ],
        )
        self.assertEqual(repr(result), repr(unordered_list_to_html_node(block)))

    def test_ul_dashes(self):
        block = "- list item 1\n- list item 2"
        result = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "list item 1")]),
                ParentNode("li", [LeafNode(None, "list item 2")]),
            ],
        )
        self.assertEqual(repr(result), repr(unordered_list_to_html_node(block)))

    def test_ul_nested(self):
        block = "* *list* item 1\n* list **item 2**"
        result = ParentNode(
            "ul",
            [
                ParentNode(
                    "li",
                    [
                        LeafNode("i", "list"),
                        LeafNode(None, " item 1"),
                    ],
                ),
                ParentNode(
                    "li",
                    [
                        LeafNode(None, "list "),
                        LeafNode("b", "item 2"),
                    ],
                ),
            ],
        )
        self.assertEqual(repr(result), repr(unordered_list_to_html_node(block)))

    def test_ol_single(self):
        block = "1. list item 1\n2. list item 2"
        result = ParentNode(
            "ol",
            [
                ParentNode("li", [LeafNode(None, "list item 1")]),
                ParentNode("li", [LeafNode(None, "list item 2")]),
            ],
        )
        self.assertEqual(repr(result), repr(ordered_list_to_html_node(block)))


class TestParagraphToHTMLNodes(unittest.TestCase):

    def test_paragraph(self):
        block = "Some text with `code` and **bold** on\n multiple lines ending *italic*"
        result = ParentNode(
            "p",
            [
                LeafNode(None, "Some text with "),
                LeafNode("code", "code"),
                LeafNode(None, " and "),
                LeafNode("b", "bold"),
                LeafNode(None, " on\n multiple lines ending "),
                LeafNode("i", "italic"),
            ],
        )
        self.assertEqual(repr(result), repr(paragraph_to_html_node(block)))


class TestMarkdownToHTMLNodes(unittest.TestCase):

    def test_processing(self):
        result = ParentNode(
            "div",
            [
                ParentNode("h1", [LeafNode(None, "H1 Heading")]),
                ParentNode("h6", [LeafNode(None, "H6 Heading")]),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "This is a paragraph with "),
                        LeafNode("b", "bold text"),
                        LeafNode(None, " on\nmultiple "),
                        LeafNode("i", "italic"),
                        LeafNode(None, " "),
                        LeafNode("code", "coded"),
                        LeafNode(None, " lines."),
                    ],
                ),
                ParentNode(
                    "ul",
                    [
                        ParentNode(
                            "li",
                            [
                                LeafNode(None, "Image Item 1 "),
                                LeafNode(
                                    "img", "", {"src": "https://test.com", "alt": "alt"}
                                ),
                            ],
                        ),
                        ParentNode(
                            "li",
                            [
                                LeafNode(None, "Link Item 2 "),
                                LeafNode("a", "label", {"href": "https://test.com"}),
                            ],
                        ),
                    ],
                ),
                ParentNode(
                    "ul",
                    [
                        ParentNode(
                            "li",
                            [
                                LeafNode(None, "List Item 1"),
                            ],
                        ),
                        ParentNode(
                            "li",
                            [
                                LeafNode(None, "List Item 2"),
                            ],
                        ),
                    ],
                ),
                ParentNode(
                    "ol",
                    [
                        ParentNode(
                            "li",
                            [
                                LeafNode(None, "List Item"),
                            ],
                        ),
                        ParentNode(
                            "li",
                            [
                                LeafNode(None, "List Item"),
                            ],
                        ),
                    ],
                ),
                ParentNode(
                    "blockquote", [LeafNode(None, "This is a multi\nline quote")]
                ),
            ],
        )
        self.assertEqual(
            repr(result), repr(markdown_to_html_node(test_markdown_to_html_nodes))
        )

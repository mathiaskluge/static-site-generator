import unittest
from pathlib import Path

from block_markdown import markdown_to_blocks, BlockType, block_to_block_type

test_markdown = Path("src/test_markdown.md").read_text()


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
        block = ". list item"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_ol_multi(self):
        block = ". list item\n. list item"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_ol_not_all(self):
        block = ". list item\n list item"
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

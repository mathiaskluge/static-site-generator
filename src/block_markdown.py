import re
from enum import Enum

from htmlnode import ParentNode, LeafNode
from inline_markdown import (
    text_to_textnodes,
    text_node_to_html_node,
    text_to_html_nodes,
)


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def markdown_to_blocks(markdown):
    """Splits into a list of blocks.

    Splits by \n\n and strips whitespace
    left and right of each block.

    RETURNS
    -------
        list
    """
    pattern = r"(?:\r?\n){2,}"
    return re.split(pattern, markdown.strip())


def block_to_block_type(markdown_block):
    """Returns the BlockType of a given markdown block.

    Returns
    -------
        BlockType
    """
    lines = markdown_block.split("\n")

    # Headings
    headings_pattern = r"^#{1,6}\s"
    match = 1 if re.match(headings_pattern, lines[0]) else 0

    if match and len(lines) == 1:
        return BlockType.HEADING
    elif match and len(lines) > 1:
        raise Exception("Heading contains a line break.")
        # ToDo: Deal with more than 6 #

    # Code Blocks
    if lines[0][:3] == "```" and lines[-1][-3:] == "```":
        return BlockType.CODE
    if lines[0][:3] == "```" and lines[-1][-3:] != "```":
        raise Exception(f"Code Block not closed: {lines[-1]}.")

    # Quotes
    quotes_pattern = r"^>"
    matches = sum(1 for line in lines if re.match(quotes_pattern, line))

    if matches == len(lines):
        return BlockType.QUOTE
    elif matches and matches != len(lines):
        raise Exception("Quotes Block Syntax not correct.")

    # Unordered List
    ul_pattern_star = r"^\*\s"
    ul_pattern_dash = r"^\-\s"
    matches_star = sum(1 for line in lines if re.match(ul_pattern_star, line))
    matches_dash = sum(1 for line in lines if re.match(ul_pattern_dash, line))

    if matches_star == len(lines) or matches_dash == len(lines):
        return BlockType.UNORDERED_LIST

    elif matches_star and matches_star != len(lines):
        raise Exception("Incorrect unordered list syntax.")
    elif matches_dash and matches_dash != len(lines):
        raise Exception("Incorrect unordered list syntax.")

    # Ordered List
    if lines[0].startswith("1. "):
        item_count = 1
        for line in lines:
            if not line.startswith(f"{item_count}. "):
                raise Exception("Incorrect ordered list syntax.")
            else:
                item_count += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def heading_to_html_node(heading_block):
    """Converts a Markdown Heading Block into HTMLNodes."""
    heading_level = f"h{heading_block.count('#')}"
    heading_text = heading_block.lstrip("# ")
    return ParentNode(heading_level, text_to_html_nodes(heading_text))


def codeblock_to_html_node(code_block):
    """Converts a Markdown Code Block into HTMLNodes."""
    code_text = code_block[3:-3]
    return ParentNode("pre", [ParentNode("code", text_to_html_nodes(code_text))])


def quote_to_html_node(quote_block):
    """Converts a Markdown Quote Block into HTMLNodes."""
    quote_text = "\n".join(line.lstrip(">") for line in quote_block.split("\n"))
    return ParentNode("blockquote", text_to_html_nodes(quote_text))


def unordered_list_to_html_node(ul_block):
    """Converts a Markdown Unordered List Block into HTMLNodes."""
    list_item_texts = [re.sub(r"^[*-]\s", "", line) for line in ul_block.split("\n")]
    list_items = []

    for list_item_text in list_item_texts:
        list_items.append(ParentNode("li", text_to_html_nodes(list_item_text)))

    return ParentNode("ul", list_items)


def ordered_list_to_html_node(ol_block):
    """Converts a Markdown Ordered List Block into HTMLNodes."""
    list_item_texts = [re.sub(r"^.*?\s", "", line) for line in ol_block.split("\n")]
    list_items = []

    for list_item_text in list_item_texts:
        list_items.append(ParentNode("li", text_to_html_nodes(list_item_text)))

    return ParentNode("ol", list_items)


def paragraph_to_html_node(paragraph_block):
    """Converts a Markdown Paragraph into HTMLNodes."""
    return ParentNode("p", text_to_html_nodes(paragraph_block))


def markdown_to_html_node(markdown):
    """Converts Markdown to HTMLNodes."""
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.HEADING:
                block_nodes.append(heading_to_html_node(block))
            case BlockType.CODE:
                block_nodes.append(codeblock_to_html_node(block))
            case BlockType.QUOTE:
                block_nodes.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                block_nodes.append(unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                block_nodes.append(ordered_list_to_html_node(block))
            case BlockType.PARAGRAPH:
                block_nodes.append(paragraph_to_html_node(block))
            case _:
                raise Exception("Unknown BlockType")

    return ParentNode("div", block_nodes)

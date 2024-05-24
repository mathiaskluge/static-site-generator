import re
from enum import Enum


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
        raise Exception("Heading contains a line break")
        # ToDo: Deal with more than 6 #

    # Code Blocks
    if lines[0][:3] == "```" and lines[-1][-3:] == "```":
        return BlockType.CODE
    if lines[0][:3] == "```" and lines[-1][-3:] != "```":
        raise Exception(f"Code Block not closed: {lines[-1]}")

    # Quotes
    quotes_pattern = r"^>"
    matches = sum(1 for line in lines if re.match(quotes_pattern, line))

    if matches == len(lines):
        return BlockType.QUOTE
    elif matches and matches != len(lines):
        raise Exception("Quotes Block Syntax not correct")

    # Unordered List
    ul_pattern_star = r"^\*\s"
    ul_pattern_dash = r"^\-\s"
    matches_star = sum(1 for line in lines if re.match(ul_pattern_star, line))
    matches_dash = sum(1 for line in lines if re.match(ul_pattern_dash, line))

    if matches_star == len(lines) or matches_dash == len(lines):
        return BlockType.UNORDERED_LIST

    elif matches_star and matches_star != len(lines):
        raise Exception("Incorrect unordered list syntax")
    elif matches_dash and matches_dash != len(lines):
        raise Exception("Incorrect unordered list syntax")

    # Ordered List
    ol_pattern = r"^\.\s"
    matches = sum(1 for line in lines if re.match(ol_pattern, line))

    if matches == len(lines):
        return BlockType.ORDERED_LIST
    elif matches and matches != len(lines):
        raise Exception("Ordered List Syntax not correct")

    return BlockType.PARAGRAPH

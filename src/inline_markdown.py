from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_node_to_html_node(text_node):
    """Converts a TextNode into a HTMLNode (Leafnode) based on its TextType."""

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img", "", {"src": text_node.url, "alt": text_node.text}
                )
        case _:
            raise ValueError("Invalid TextType")


def split_nodes_delimiter(
        old_nodes: list, delimiter: str, text_type: TextType
        ):
    """Splits a list of TextNode by specified delimiter and TextType.

    It does not split TextNodes of TextTypes other than TextType.Text.
    It does not support nesting, hence single delimiter.

    Parameters
    ----------
    old_nodes: list
        List of TextNode
    delimiter: str
        Markdown Delimiter
    text_type: TextType
        TextType of Nodes split using the delimiter

    Returns
    -------
    list
        List of TextNodes
    """

    new_nodes = []

    for node in old_nodes:
        # skips processing of TextNodes with TextType other than TextType.TEXT
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        split_texts = node.text.split(delimiter)

        # if tags are set correctly, the len(split_texts) is always uneven.
        if len(split_texts) % 2 == 0:
            raise Exception(f'Invalid Markdown: "{node.text}"')

        for i in range(len(split_texts)):
            # handles splits at the beginning/end of the text
            if split_texts[i] == "":
                continue
            # TextNodes other than TextType.TEXT will always be
            # on odd indices
            if i % 2 != 0:
                new_nodes.append(TextNode(split_texts[i], text_type))
            else:
                new_nodes.append(TextNode(split_texts[i], TextType.TEXT))

    return new_nodes

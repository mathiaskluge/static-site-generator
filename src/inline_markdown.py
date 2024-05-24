import re

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
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid TextType")


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType):
    """Splits a list of TextNode by a delimiter and assigns TextTypes.

    Splits only TextNodes of TextType.TEXT.
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


def extract_markdown_images(text):
    """Extracxt markdown image tags into a list of tuples.

    Returns
    -------
    list
        list of tuples: [(alt, url), ...]
    """
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)

    return matches


def extract_markdown_links(text):
    """Extracxt markdown link tags into a list of tuples.

    Returns
    -------
    list
        list of tuples: [(label, url), ...]
    """
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)

    return matches


def split_nodes_image(old_nodes):
    """Splits TextNodes based on markdown image tags.

    Returns
    -------
    list
        list of TextNodes
    """
    new_nodes = []

    for node in old_nodes:
        # skip all non TextType.TEXT nodes and append as they are
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        # gets text and images
        text = node.text
        images = extract_markdown_images(text)
        # appends node if there are no images
        if len(images) == 0:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
            continue
        for image in images:
            # splits text in half at the point of the image
            halfs = text.split(f"![{image[0]}]({image[1]})", 1)
            # catches invalid markdown
            if len(halfs) != 2:
                raise ValueError("Image tag was not closed: ![{image[0]}]({image[1]})")
            # image not at the beggining -> append text first
            if halfs[0] != "":
                new_nodes.append(TextNode(halfs[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            # sets second half as new text to go over for the next image
            text = halfs[1]
        # -> image was not at the end, append remaining text
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """Splits TextNodes based on markdown link tags.

    Returns
    -------
    list
        list of TextNodes
    """
    new_nodes = []

    for node in old_nodes:
        # skip all non TextType.TEXT nodes and append as they are
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        # gets text and links
        text = node.text
        links = extract_markdown_links(text)
        # appends node if there are no links
        if len(links) == 0:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
            continue
        for link in links:
            # splits text in half at the point of the link
            halfs = text.split(f"[{link[0]}]({link[1]})", 1)
            # catches invalid markdown
            if len(halfs) != 2:
                raise ValueError(f"Link tag was not closed: [{link[0]}]({link[1]})")
            # link not at the beggining -> append text first
            if halfs[0] != "":
                new_nodes.append(TextNode(halfs[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            # sets second half as new text to go over for the next link
            text = halfs[1]
        # -> link was not at the end, append remaining text
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    """Converts text into a list of TextNodes."""
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def text_to_html_nodes(text):
    """Converts text into a list of Inline HTMLNodes"""
    children = []
    for textnode in text_to_textnodes(text):
        children.append(text_node_to_html_node(textnode))
    
    return children

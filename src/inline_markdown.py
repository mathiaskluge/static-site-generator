# regex to parse markdown images and links
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
            return LeafNode(
                "img",
                "",
                {"src": text_node.url, "alt": text_node.text}
                )
        case _:
            raise ValueError("Invalid TextType")


def split_nodes_delimiter(
        old_nodes: list,
        delimiter: str,
        text_type: TextType
        ):
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

    images = [(alt, url) for alt, url in matches]

    return images


def extract_markdown_links(text):
    """Extracxt markdown link tags into a list of tuples.

    Returns
    -------
    list
        list of tuples: [(label, url), ...]
    """
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)

    links = [(label, url) for label, url in matches]

    return links


def split_nodes_image(old_nodes):
    """Splits TextNodes based on markdown image tags.

    Returns
    -------
    list
        list of TextNodes
    """
    new_nodes = []

    for node in old_nodes:

        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(node.text)

        # appends node if there is no image
        if len(images) == 0:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
            continue

        for i in range(len(images)):

            split_text = text.split(f"![{images[i][0]}]({images[i][1]})", 1)

            # if there's at least one more ref in split_text[1]
            if i + 1 < len(images):
                # ref is right at the start
                if split_text[0] == "":
                    new_nodes.append(
                        TextNode(images[i][0], TextType.IMAGE, images[i][1])
                    )
                else:
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                    new_nodes.append(
                        TextNode(images[i][0], TextType.IMAGE, images[i][1])
                    )
                # next text to split is remainder (there is at least one more)
                text = split_text[1]
                continue
            # last ref or only one in total
            else:
                # ref is the entire thing
                if split_text[0] == "" and split_text[1] == "":
                    new_nodes.append(
                        TextNode(images[i][0], TextType.IMAGE, images[i][1])
                    )

                # ref is at the start, text afterwards
                elif split_text[0] == "":
                    new_nodes.append(
                        TextNode(images[i][0], TextType.IMAGE, images[i][1])
                    )
                    new_nodes.append(TextNode(split_text[1], TextType.TEXT))

                # ref is at the end, text before
                elif split_text[1] == "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                    new_nodes.append(
                        TextNode(images[i][0], TextType.IMAGE, images[i][1])
                    )

                # ref is in the middle, text before and after
                else:
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                    new_nodes.append(
                        TextNode(images[i][0], TextType.IMAGE, images[i][1])
                    )
                    new_nodes.append(TextNode(split_text[1], TextType.TEXT))

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
        
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(node.text)
        # appends node if there is no link
        if len(links) == 0:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
            continue

        for i in range(len(links)):
            split_text = text.split(f"[{links[i][0]}]({links[i][1]})", 1)

            # if there's at least one more link in split_text[1]
            if i + 1 < len(links):
                # link is right at the start
                if split_text[0] == "":
                    new_nodes.append(
                        TextNode(links[i][0], TextType.LINK, links[i][1])
                    )
                else:
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                    new_nodes.append(
                        TextNode(links[i][0], TextType.LINK, links[i][1])
                    )
                # next text to split is remainder (there is at least one more)
                text = split_text[1]
                continue
            # last link or only one in total
            else:
                # link is the entire thing
                if split_text[0] == "" and split_text[1] == "":
                    new_nodes.append(
                        TextNode(links[i][0], TextType.LINK, links[i][1])
                    )

                # link is at the start, text afterwards
                elif split_text[0] == "":
                    new_nodes.append(
                        TextNode(links[i][0], TextType.LINK, links[i][1])
                    )
                    new_nodes.append(TextNode(split_text[1], TextType.TEXT))

                # link is at the end, text before
                elif split_text[1] == "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                    new_nodes.append(
                        TextNode(links[i][0], TextType.LINK, links[i][1])
                    )

                # link is in the middle, text before and after
                else:
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                    new_nodes.append(
                        TextNode(links[i][0], TextType.LINK, links[i][1])
                    )
                    new_nodes.append(TextNode(split_text[1], TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

from enum import Enum

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


def main():

    test = TextNode("This is a text node", "bold", "https://github.com/mathiaskluge")
    print(test)

    node = HTMLNode(tag="a", props={"href": "https://www.example.com", "target": "_blank"})
    print(node.props_to_html()) 


def text_node_to_html_node(text_node):

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
            return LeafNode("a",text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid TextType")


if __name__ == "__main__":
    main()

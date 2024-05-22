from textnode import TextNode
from htmlnode import HTMLNode


def main():

    test = TextNode("This is a text node", "bold", "https://github.com/mathiaskluge")
    print(test)

    node = HTMLNode(tag="a", props={"href": "https://www.example.com", "target": "_blank"})
    print(node.props_to_html()) 


if __name__ == "__main__":
    main()

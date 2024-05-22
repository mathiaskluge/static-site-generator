import unittest

from htmlnode import HTMLNode

test_props = {
    "href": "https://www.example.com",
    "target": "_blank",
    "id": "link1",
}


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(None, None, None, test_props)
        self.assertEqual(
            ' href="https://www.example.com" target="_blank" id="link1"',
            node.props_to_html(),
        )

    def test_props_to_html_none(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual("", node.props_to_html())

    def test_repr(self):
        node = HTMLNode("a", "value", ["child1", "child2"], test_props)
        self.assertEqual(
            "HTMLNode(tag: a, value: value, children: ['child1', 'child2'], props: {'href': 'https://www.example.com', 'target': '_blank', 'id': 'link1'})",
            repr(node),
        )


if __name__ == "__main__":
    unittest.main()

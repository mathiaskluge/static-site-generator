import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.test.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.test.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode(
            "This is a text node", TextType.BOLD, "https://github.com/mathiaskluge"
        )
        self.assertEqual(
            "TextNode(This is a text node, BOLD, https://github.com/mathiaskluge)",
            repr(node),
        )


if __name__ == "__main__":
    unittest.main()

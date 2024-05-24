import unittest
from markdown_to_html import extract_title

class TestMarkdownToHTML(unittest.TestCase):

    def test_extract_heading(self):
        markdown = """
        # This is my h1 heading

        And some paragraph over
        multiple lines.

        # Another h1
        """
        result = "This is my h1 heading"
        self.assertEqual(result, extract_title(markdown))

import unittest

from page_generator import extract_title_markdown


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Title\nsome text\nanotherl line"
        self.assertEqual(extract_title_markdown(md), "Title")

    def test_extract_title_error(self):
        md = "## h2 header"
        with self.assertRaises(ValueError):
            extract_title_markdown(md)
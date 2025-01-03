import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        self.assertEqual(markdown_to_blocks(text),
                         [
                          "# This is a heading",
                          "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                          "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                         ])
    
    def test_markdown_to_blocks_whitespace(self):
        text = "# This is a heading\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n        * This is the first list item in a list block\n* This is a list item\n* This is another list item"
        self.assertEqual(markdown_to_blocks(text),
                         [
                          "# This is a heading",
                          "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                          "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                         ])
        

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "### some heading"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_block_to_block_type_code(self):
        block = "```some heading\n\nmore code```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_block_to_block_type_quote(self):
        block = ">a quote\n>continuation of quote"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_block_to_block_type_unordered_list(self):
        block = "* point\n* another point\n* last point"
        self.assertEqual(block_to_block_type(block), "unordered list")

    def test_block_to_block_type_ordered_list(self):
        block = "1. first point\n2. second point\n3. third point"
        self.assertEqual(block_to_block_type(block), "ordered list")

    def test_block_to_block_type_paragraph(self):
        block = ">partial quote\nno more quote"
        self.assertEqual(block_to_block_type(block), "paragraph")


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```This is some code
more code
even more code```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is some code\nmore code\neven more code</code></pre></div>"
        )



if __name__ == "__main__":
    unittest.main()
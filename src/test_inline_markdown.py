import unittest

from textnode import TextType, TextNode
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, 
                        [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" word", TextType.TEXT),
                        ]
                    )
    
    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word **another bold word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, 
                        [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("bold", TextType.BOLD),
                        TextNode(" word ", TextType.TEXT),
                        TextNode("another bold word", TextType.BOLD),
                        ]
                    )
        
    def test_split_italic(self):
        node = TextNode("This is text with a *italic* word *another italic word* *another word*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, 
                        [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word ", TextType.TEXT),
                        TextNode("another italic word", TextType.ITALIC),
                        TextNode(" ", TextType.TEXT),
                        TextNode("another word", TextType.ITALIC)
                        ]
                    )
        
    def test_split_different_delimiters(self):
        node = TextNode("This is text with an *italic* word **and a bold word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, 
                        [
                        TextNode("This is text with an *italic* word ", TextType.TEXT),
                        TextNode("and a bold word", TextType.BOLD),
                        ]
                    )
        
    def test_split_error(self):
        node = TextNode("Some text *wrong text* text text*", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)
    
    def test_split_node_error_2(self):
        node = TextNode("Some text *wrong text* text **", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)

    def test_split_node_error_3(self):
        node = TextNode("Some text *wrong text* text***", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_mixed(self):
        text = "Here's a ![valid image](url1) and a [random bracket] (random parenthesis)"
        self.assertEqual(extract_markdown_images(text), [("valid image", "url1")])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_extract_markdown_links_mixed(self):
        text = "Here's a [valid link](url1) and a [random bracket] (random parenthesis)"
        self.assertEqual(extract_markdown_links(text), [("valid link", "url1")])

    def test_extract_markdown_links_no_link(self):
        text = "Here's an invalid link and a [random bracket] (random parenthesis)"
        self.assertEqual(extract_markdown_links(text), [])


class TestSplitNodesImage(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(split_nodes_link([node]), 
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                    ),
            ])
        
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text),
                         [
                            TextNode("This is ", TextType.TEXT),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.TEXT),
                            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("link", TextType.LINK, "https://boot.dev"),
                        ]
                    )


if __name__ == "__main__":
    unittest.main()
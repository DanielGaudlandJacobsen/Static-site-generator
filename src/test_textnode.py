import unittest

from textnode import TextNode, TextType, LeafNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node_2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node_2)
    
    def test_eq_2(self):
        node = TextNode("Test node", TextType.CODE, None)
        node_2 = TextNode("Test node", TextType.CODE)
        self.assertEqual(node, node_2)

    def test_eq_url(self):
        node = TextNode("Test node", TextType.CODE, "url")
        node_2 = TextNode("Test node", TextType.CODE, "url")
        self.assertEqual(node, node_2)

    def test_eq_false(self):
        node = TextNode("Some text", TextType.ITALIC)
        node_2 = TextNode("Some text", TextType.TEXT)
        self.assertNotEqual(node, node_2)

    def test_eq_false_2(self):
        node = TextNode("Text", TextType.TEXT)
        node_2 = TextNode("Text2", TextType.TEXT)
        self.assertNotEqual(node, node_2)

    def test_eq_false_3(self):
        node = TextNode("Text", TextType.TEXT, "url1")
        node_2 = TextNode("Text", TextType.TEXT, "url2")
        self.assertNotEqual(node, node_2)

    def test_repr(self):
        node = TextNode("Testing text", TextType.IMAGE, "url")
        self.assertEqual(repr(node), "TextNode(Testing text, image, url)")


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node_2 = LeafNode("b", "This is a text node")
        self.assertEqual(repr(text_node_to_html_node(node)), repr(node_2))

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "someurl")
        self.assertEqual(repr(text_node_to_html_node(node)), "LeafNode(a, This is a text node, {'href': 'someurl'})")

    def test_img(self):
        node = TextNode("alt text", TextType.IMAGE, "img_url")
        self.assertEqual(repr(text_node_to_html_node(node)), "LeafNode(img, , {'src': 'img_url', 'alt': 'alt text'})")


if __name__ == "__main__":
    unittest.main()
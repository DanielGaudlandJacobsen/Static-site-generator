import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class HTMLNodeTest(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("a", "some text", None, {"href": "url", "prop": "some property"})
        self.assertEqual(repr(node), "HTMLNode(a, some text, None, {'href': 'url', 'prop': 'some property'})")

    def test_props_to_html(self):
        node = HTMLNode("p", "test text", None, {"src": "source", "prop1": "some property", "prop2": "another property"})
        self.assertEqual(node.props_to_html(), ' src="source" prop1="some property" prop2="another property"')

    def test_props_to_html_2(self):
        node = HTMLNode("p", "test text")
        self.assertEqual(node.props_to_html(), "")


class LeafNodeTests(unittest.TestCase):
    def test_repr(self):
        node = LeafNode("p", "a paragraph.", None)
        self.assertEqual(repr(node), "LeafNode(p, a paragraph., None)")

    def test_to_html(self):
        node = LeafNode("a", "A link.", {"href": "some url", "property": "another prop"})
        self.assertEqual(node.to_html(), '<a href="some url" property="another prop">A link.</a>')

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Plain text")
        self.assertEqual(node.to_html(), "Plain text")

    def test_to_html_no_value(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()


class ParentNodeTest(unittest.TestCase):
    def test_repr(self):
        pass

    def test_to_html(self):
        node = ParentNode(
            "div", 
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href": "some url", "property": "another prop"}
        )
        self.assertEqual(node.to_html(), '<div href="some url" property="another prop"><b>Bold text</b>Normal text<i>italic text</i>Normal text</div>')

    def test_to_html_nested_parent_node(self):
        node = ParentNode(
            "nav", 
            [
                ParentNode("div",
                           [
                            LeafNode("b", "Bold text"),
                            LeafNode(None, "Normal text"),
                            LeafNode("i", "italic text"),
                            LeafNode(None, "Normal text"),
                            ],
                            {"href": "some url", "property": "another prop"}
                        ),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href": "some url", "property": "another prop"}
        )
        self.assertEqual(node.to_html(), '<nav href="some url" property="another prop"><div href="some url" property="another prop"><b>Bold text</b>Normal text<i>italic text</i>Normal text</div><b>Bold text</b>Normal text<i>italic text</i>Normal text</nav>')

    def test_repr(self):
        node = ParentNode(
            "nav", 
            [
                ParentNode("div",
                           [
                            LeafNode(None, "Normal text"),
                            ],
                            {"href": "some url", "property": "another prop"}
                        ),
                LeafNode("b", "Bold text"),
            ],
            {"href": "some url", "property": "another prop"}
        )
        self.assertEqual(repr(node), "ParentNode(nav, children: [ParentNode(div, children: [LeafNode(None, Normal text, None)], {'href': 'some url', 'property': 'another prop'}), LeafNode(b, Bold text, None)], {'href': 'some url', 'property': 'another prop'})")

    
if __name__ == "__main__":
    unittest.main()
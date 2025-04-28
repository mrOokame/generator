import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):

    def test_to_html_raises(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "test html",
            None, 
            {
            "href": "https://www.google.com",
            "target": "_blank",
            }
        )

        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )  

        node2 = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node2.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_repr(self):
        node = HTMLNode("p","test html")   
        self.assertEqual(
            "HTMLNode(p, test html, None, None)", repr(node)
        )  

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(),"<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")      

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_leaf_with_no_value_in_parent_raises(self):
        bad_leaf = LeafNode("p", None)
        parent = ParentNode("div", [bad_leaf])
        
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        
        self.assertIn("must have a value", str(context.exception))

    def test_valid_parent_and_leaf_renders_html(self):
        leaf = LeafNode("p", "Hello")
        parent = ParentNode("div", [leaf])
        
        expected = "<div><p>Hello</p></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()
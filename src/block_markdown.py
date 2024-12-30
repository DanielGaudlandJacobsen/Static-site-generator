from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block != "":
            block = block.strip()
            filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    if is_heading(block):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    if is_quote(block):
        return "quote"
    if is_unordered_list(block):
        return "unordered list"
    if is_ordered_list(block):
        return "ordered list"
    return "paragraph"


def is_heading(block):
    if block.startswith("# "):
        return True
    elif block.startswith("## "):
        return True
    elif block.startswith("### "):
        return True
    elif block.startswith("#### "):
        return True
    elif block.startswith("##### "):
        return True
    elif block.startswith("###### "):
        return True
    else:
        return False


def is_quote(block):
    quote_check = block.split("\n")
    block_status = True
    for line in quote_check:
        if not line.startswith(">"):
            block_status = False
    return block_status


def is_unordered_list(block):
    lines = block.split("\n")
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return False
        return True
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return False
        return True


def is_ordered_list(block):
    list_check = block.split("\n")
    block_status = True
    for i in range(len(list_check)):
        if not list_check[i].startswith(f"{i+1}. "):
            block_status = False
    return block_status


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block):
    match block_to_block_type(block):
        case "paragraph":
            return  paragraph_to_html_node(block)
        case "heading":
            return heading_to_html_node(block)
        case "code":
            return code_to_html_node(block)
        case "ordered list":
            return ordered_list_to_html_node(block)
        case "unordered list":
            return unordered_list_to_html_node(block)
        case "quote":
            return quote_to_html_node(block)
        case _:
            raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for c in block:
        if c == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError("invalid heading level")
    text = block[level+1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    text = block[3:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def ordered_list_to_html_node(block):
    points = block.split("\n")
    html_items = []
    for point in points:
        text = point[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def unordered_list_to_html_node(block):
    points = block.split("\n")
    html_items = []
    for point in points:
        text = point[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    quote_lines = []
    for line in lines:
        quote_lines.append(line.lstrip(">").strip())
    quote = " ".join(quote_lines)
    children = text_to_children(quote)
    return ParentNode("blockquote", children)
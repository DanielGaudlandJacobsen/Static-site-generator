import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if node.text.count(delimiter) % 2 != 0:
                raise ValueError("Invalid markdown syntax")
            split_node = node.text.split(delimiter)
            for i in range(len(split_node)):
                if i % 2 == 0:
                    if split_node[i] == "":
                        continue
                    split_node_part = TextNode(split_node[i], TextType.TEXT)
                    new_nodes.append(split_node_part)
                else:
                    if split_node[i] == "":
                        raise ValueError("Invalid markdown syntax")
                    split_node_part = TextNode(split_node[i], text_type)
                    new_nodes.append(split_node_part)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        alt_img_lst = extract_markdown_images(original_text)
        if len(alt_img_lst) == 0:
            new_nodes.append(node)
            continue
        for img in alt_img_lst:
            split_node = original_text.split(f"![{img[0]}]({img[1]})", 1)
            if len(split_node) != 2:
                raise ValueError("Invalid markdown syntax")
            if split_node[0] != "":
                split_node_part = TextNode(split_node[0], TextType.TEXT)
                new_nodes.append(split_node_part)
            split_node_part = TextNode(img[0], TextType.IMAGE, img[1])
            new_nodes.append(split_node_part)
            original_text = split_node[1]
        if original_text != "":
            split_node_part = TextNode(original_text, TextType.TEXT)
            new_nodes.append(split_node_part)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        anchor_url_lst = extract_markdown_links(original_text)
        if len(anchor_url_lst) == 0:
            new_nodes.append(node)
            continue
        for link in anchor_url_lst:
            split_node = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_node) != 2:
                raise ValueError("Invalid markdown syntax")
            if split_node[0] != "":
                split_node_part = TextNode(split_node[0], TextType.TEXT)
                new_nodes.append(split_node_part)
            split_node_part = TextNode(link[0], TextType.LINK, link[1])
            new_nodes.append(split_node_part)
            original_text = split_node[1]
        if original_text != "":
            split_node_part = TextNode(original_text, TextType.TEXT)
            new_nodes.append(split_node_part)
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
from block_markdown import markdown_to_html_node
import os


def extract_title_markdown(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise ValueError("No title in document")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = open(os.path.join(from_path, "index.md")).read()
    template = open(os.path.join(template_path, "template.html")).read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title_markdown(md)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    index = open(os.path.join(dest_path, "index.html"), "w")
    index.write(template)

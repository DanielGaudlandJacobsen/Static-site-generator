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
    md = open(os.path.join(from_path)).read()
    template = open(os.path.join(template_path, "template.html")).read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title_markdown(md)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    index = open(os.path.join(dest_path, "index.html"), "w")
    index.write(template)
    index.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(file_path):
            os.makedirs(dest_dir_path, exist_ok=True)
            generate_page(file_path, template_path, dest_dir_path)
        elif os.path.isdir(file_path):
            generate_pages_recursive(file_path, template_path, dest_path)
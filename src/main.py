import os
import shutil
import sys

from static_mover import static_mover
from page_generator import generate_pages_recursive

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

current_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_path)
source = os.path.join(current_dir, "..", "static")
source_path = os.path.abspath(source)
destination = os.path.join(current_dir, "..", "docs")
destination_path = os.path.abspath(destination)
template = os.path.join(current_dir, "..")
template_path = os.path.abspath(template)
content = os.path.join(current_dir, "..", "content")
content_path = os.path.abspath(content)


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    static_mover(source_path, destination_path)
    generate_pages_recursive(content_path, template_path, destination_path, basepath)

main()
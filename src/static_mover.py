import os
import shutil


def static_mover():
    current_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_path)
    source = os.path.join(current_dir, "..", "static")
    source_path = os.path.abspath(source)
    destination = os.path.join(current_dir, "..", "public")
    destination_path = os.path.abspath(destination)
    if not os.path.exists(source_path):
        raise Exception("No source directory")
    if not os.path.exists(destination_path):
        os.mkdir(current_dir + "/../public")
    else:
        shutil.rmtree(current_dir + "/../public")
        os.mkdir(current_dir + "/../public")
    shutil.copytree(current_dir + "/../static", current_dir + "/../public", dirs_exist_ok=True)
import os
import shutil


def static_mover(src_path, dest_path):
    if not os.path.exists(src_path):
        raise Exception("No source directory")
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    else:
        shutil.rmtree(dest_path)
        os.mkdir(dest_path)
    shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
import os


def main():
    print(static_mover())


def static_mover():
    source = os.path.join("..", "static")
    destination = os.path.join("..", "public")
    print(os.path.exists())
    return source, destination


main()
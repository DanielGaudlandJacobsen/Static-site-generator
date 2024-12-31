def extract_title_markdown(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise ValueError("No title in document")
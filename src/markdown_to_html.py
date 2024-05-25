import re
import os

from pathlib import Path
from block_markdown import markdown_to_html_node


def extract_title(markdown):
    h1_pattern = r"^\s*#\s+(.*)$"
    matches = re.findall(h1_pattern, markdown, flags=re.MULTILINE)

    if matches:
        return matches[0]
    else:
        raise Exception("All pages need a single H1 heading")


def generate_page(
    src: str = "content/index.md",
    tmplt: str = "template/template.html",
    dst: str = "public/index.html",
):

    try:
        markdown = Path(f"{src}").read_text()
        template = Path(f"{tmplt}").read_text()

        title = extract_title(markdown)
        content = markdown_to_html_node(markdown).to_html()

        html = template.replace("{{ Title }}", f"{title}")
        html = html.replace("{{ Content }}", f"{content}")

        dir_fd = os.open("public/", os.O_RDONLY)

        def opener(path, flags):
            return os.open(path, flags, dir_fd=dir_fd)

        with open("index.html", "w", opener=opener) as f:
            print(html, file=f)

        os.close(dir_fd)

    except Exception as e:
        print("An error occurred:", e)

    # log success
    print(f"✅ {dst} (from '{src}' using '{tmplt}')")


def generate_pages_recursive(
    src: str = "content",
    dst: str = "public",
    fil_c: int = 0,
):
    """Generates pages recursivly"""
    src_path = f"{src}/"
    dst_path = f"{dst}/"

    if fil_c == 0:
        print(f"\n\nGenerating pages from '{src_path}' to")
        print("==================================")

    for src_file in os.listdir(src_path):
        src_file_path = f"{src_path}{src_file}"
        tmplt_file_path = "template/template.html"
        dst_file_path = f"{dst_path}{src_file}"

        if os.path.isfile(src_file_path):

            if src_file == ".DS_Store":
                continue
            if not src_file.endswith(".md"):
                print(f"✋ {src_file_path} (Skipped - Not a .md file)")
                continue
            fil_c += 1
            generate_page(src_file_path, tmplt_file_path, dst_file_path)

        else:
            generate_pages_recursive(src_file_path, dst_file_path, fil_c)
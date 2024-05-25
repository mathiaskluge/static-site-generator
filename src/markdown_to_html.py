import re
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
    src: Path = Path("content/index.md"),
    tmplt: Path = Path("template/template.html"),
    dst: Path = Path("public/index.html"),
):
    markdown = src.read_text()
    template = tmplt.read_text()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    html = template.replace("{{ Title }}", f"{title}")
    html = html.replace("{{ Content }}", f"{content}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w") as f:
        f.write(html)
    # log success
    print(f"✅ {dst} (from '{src}' using '{tmplt}')")


def generate_pages_recursive(
    src: Path = Path("content/"),
    dst: Path = Path("public/"),
    fil_c: int = 0,
):
    """Generates pages recursivly"""
    if fil_c == 0:
        print(f"\n\nGenerating pages from '{src}' to")
        print("==================================")

    for src_file in list(src.iterdir()):
        tmplt_file = Path("template/template.html")

        if not src_file.is_file():
            dst_file = dst / (src_file.stem + "/")
            generate_pages_recursive(src_file, dst_file, fil_c)

        elif src_file.is_file() and src_file.suffix == ".md":
            dst_file = dst / (src_file.stem + ".html")
            generate_page(src_file, tmplt_file, dst_file)
            fil_c += 1
        else:
            print(f"✋ {src_file} (Skipped - Not a .md file)")
            continue

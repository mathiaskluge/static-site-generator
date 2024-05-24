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
    # log
    print(f"\n* Generating page: '{src}' ==='{tmplt}'==> '{dst}'\n")

    try:
        markdown = Path(f"{src}").read_text()
        template = Path(f"{tmplt}").read_text()

        title = extract_title(markdown)
        content = markdown_to_html_node(markdown).to_html()

        html = template.replace('{{ Title }}', f'{title}')
        html = html.replace('{{ Content }}', f'{content}')

        dir_fd = os.open('public/', os.O_RDONLY)

        def opener(path, flags):
            return os.open(path, flags, dir_fd=dir_fd)

        with open('index.html', 'w', opener=opener) as f:
            print(html, file=f)

        os.close(dir_fd)

    except Exception as e:
        print("An error occurred:", e)

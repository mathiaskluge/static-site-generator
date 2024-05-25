import shutil
from pathlib import Path

from markdown_to_html import generate_pages_recursive


def copy_files(
    src: Path = Path("static/"),
    dst: Path = Path("public/"),
    fil_c: int = 0,
    fol_c: int = 0,
):
    """Copies files and folders from a src into a dst directory."""
    # log
    if fil_c == 0 and fol_c == 0:
        print(f"\nCopying static files from '{src}' to")
        print("====================================")
    # Remove old dst directory and create new
    shutil.rmtree(dst, ignore_errors=True)
    Path.mkdir(dst)
    # log folders
    if fol_c == 0:
        print(f"🗂️ {dst.name}")
    else:
        print(f"|{fol_c * "-"} 🗂️ {dst.name}")
    # Note: shutil.copytree is the better way. Focus here is learning
    for src_file in list(src.iterdir()):
        dst_file = dst / src_file.name

        if not src_file.is_file():
            fol_c += 1
            copy_files(src_file, dst_file, fil_c, fol_c,)
            fol_c -= 1
        elif src_file.is_file() and src_file.name != ".DS_Store":
            fil_c += 1
            shutil.copy(src_file, dst_file)
            # log files
            if fol_c == 0:
                print(f"|- 📄{src_file.name}")
            else:
                print(f"|-{fol_c * "---"} 📄{src_file.name}")
        else:
            continue


def main():
    copy_files()
    generate_pages_recursive()


if __name__ == "__main__":
    main()

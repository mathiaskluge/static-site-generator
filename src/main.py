import os
import shutil

from markdown_to_html import generate_pages_recursive


def copy_files(
        src: str = "static",
        dst: str = "public",
        fil_c: int = 0,
        fol_c: int = 0,
        ):
    """Copies files and folders from a src into a dst directory."""
    src_path = f"{src}/"
    dst_path = f"{dst}/"

    # log
    if fil_c == 0 and fol_c == 0:
        print(f"\nCopying static files from '{src_path}' to")
        print("====================================")

    # Remove old dst dir and all files
    shutil.rmtree(dst_path, ignore_errors=True)
    # Recreate the destination directory
    os.makedirs(dst_path)
    # log folders
    if fol_c == 0:
        print(f"🗂️ {dst_path}")
    else:
        print(f"|{fol_c * "-"} 🗂️ {dst_path}")

    # recursive copy
    # Note: shutil.copytree is the better way. Focus here is learning
    for src_file in os.listdir(src_path):
        src_file_path = f"{src_path}{src_file}"
        dst_file_path = f"{dst_path}{src_file}"
        # is file
        if os.path.isfile(src_file_path):
            # skipping .DS_Store
            if src_file == ".DS_Store":
                continue
            fil_c += 1
            shutil.copy(src_file_path, dst_file_path)
            # log files
            if fol_c == 0:
                print(f"|- 📄{src_file}")
            else:
                print(f"|-{fol_c * "---"} 📄{src_file}")
        # is folder
        else:
            fol_c += 1
            copy_files(
                src_file_path,
                dst_file_path,
                fil_c,
                fol_c,
                )
            fol_c -= 1


def main():
    copy_files()
    generate_pages_recursive()


if __name__ == "__main__":
    main()

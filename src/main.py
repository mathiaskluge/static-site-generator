import os
import shutil


def copy_files(src: str = "static", dst: str = "public",fil_c: int = 0, fol_c: int = 0):
    src_path = f"{src}/"
    dst_path = f"{dst}/"

    if fil_c == 0:
        print(f"Copying files from {src_path} to")
        print("=============================")
    try:
        # Remove old dst dir and all files
        shutil.rmtree(dst_path, ignore_errors=True)
        # Recreate the destination directory
        if fol_c == 0:
            print(f"🗂️ {dst_path}")
        else:
            print(f"|{fol_c * "-"} 🗂️ {dst_path}")
        os.makedirs(dst_path)

        for src_file in os.listdir(src_path):
            src_file_path = f"{src_path}{src_file}"
            dst_file_path = f"{dst_path}{src_file}"

            # is file
            if os.path.isfile(src_file_path):
                fil_c += 1
                shutil.copy(src_file_path, dst_file_path)
                if fol_c == 0:
                    print(f"|- 📄{src_file}")
                else:
                    print(f"|-{fol_c * "---"} 📄{src_file}")
            # is folder
            else:
                fol_c += 1
                copy_files(f"{src_file_path}", f"{dst_file_path}", fil_c, fol_c)
                fol_c -= 1

    except Exception as e:
        print("An error occurred:", e)


def main():
    copy_files()


if __name__ == "__main__":
    main()

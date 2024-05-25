from pathlib import Path

path = Path("content/")

print(f"Files with relativ path in {path} and File/Folder distinction")
files_with_rel_path = list(path.iterdir())
for file in files_with_rel_path:
    print(f"{file} {"---> is file" if file.is_file() else ""}")

print(f"\nFilenames with extension in {path}")
filenames_extension = [file.name for file in files_with_rel_path]
for file in filenames_extension:
    print(file)

print("\nOnly filenames")
only_filenames = [file.stem for file in files_with_rel_path]
for file in only_filenames:
    print(file)

print("----")
path = files_with_rel_path[2]
files_with_rel_path = list(path.iterdir())
for file in files_with_rel_path:
    print(f"{file} {"---> is file" if file.is_file() else ""}")



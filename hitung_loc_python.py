import os

folder_project = "."

excluded_dirs = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "env",
    ".idea",
    ".vscode",
    "build",
    "dist"
}

excluded_files = {
    "hitung_loc_python.py"
}

total_files = 0
total_lines = 0
blank_lines = 0
comment_lines = 0
code_lines = 0

in_block_comment = False
block_quote = None

for root, dirs, files in os.walk(folder_project):
    dirs[:] = [d for d in dirs if d not in excluded_dirs]

    for file in files:
        if file.endswith(".py") and file not in excluded_files:
            total_files += 1
            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    total_lines += 1
                    stripped = line.strip()

                    if stripped == "":
                        blank_lines += 1
                        continue

                    if in_block_comment:
                        comment_lines += 1
                        if block_quote in stripped:
                            in_block_comment = False
                            block_quote = None
                        continue

                    if stripped.startswith('"""') or stripped.startswith("'''"):
                        comment_lines += 1
                        block_quote = '"""' if stripped.startswith('"""') else "'''"

                        if stripped.count(block_quote) < 2:
                            in_block_comment = True

                        continue

                    if stripped.startswith("#"):
                        comment_lines += 1
                        continue

                    code_lines += 1

print("\nHASIL LOC PYTHON")
print("=" * 50)
print("Jumlah file Python   :", total_files)
print("Total baris          :", total_lines)
print("Baris kosong         :", blank_lines)
print("Baris komentar       :", comment_lines)
print("LOC kode aktif       :", code_lines)
print("=" * 50)
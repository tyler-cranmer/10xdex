import os


def print_directory_structure(start_path):
    for root, dirs, files in os.walk(start_path):
        # Skip __pycache__ directories
        if (
            "__pycache__" in root
            or ".pytest_cache" in root
            or "venv" in root
            or ".git" in root
            or "node_modules" in root
            or ".next" in root
        ):
            continue
        level = root.replace(start_path, "").count(os.sep)
        indent = "-" * 4 * level
        print(f"|{indent}{os.path.basename(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")


if __name__ == "__main__":
    start_path = "."  # Current directory
    # start_path = "/Users/tylercranmer/Dev/crypto/canto/mkt/fe-referral"
    print_directory_structure(start_path)

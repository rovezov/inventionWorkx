import os

def display_all_code(directory="."):
    # Lists of directories, files, and extensions to ignore
    ignore_dirs = ['node_modules', 'build', '.cache', '.next', '__pycache__', 'venv']
    ignore_files = ['package-lock.json', 'yarn.lock']
    ignore_extensions = ['.log', '.json', '.config.js', '.pyc']

    for root, dirs, files in os.walk(directory):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            # Exclude specific files and extensions
            if file in ignore_files or any(file.endswith(ext) for ext in ignore_extensions):
                continue

            file_path = os.path.join(root, file)
            print(f"\n--- Contents of {file_path} ---\n")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    print(f.read())
            except UnicodeDecodeError:
                print(f"Could not read {file_path} due to encoding issues.")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    display_all_code()

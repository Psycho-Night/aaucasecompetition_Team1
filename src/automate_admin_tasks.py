import subprocess

def run_linters():
    print("Running linting checks...")
    subprocess.run(["flake8", "--max-line-length=120", "src/"], check=True)
    print("Linting complete.")

def format_code():
    print("Auto-formatting code...")
    subprocess.run(["black", "src/"], check=True)
    print("Code formatted.")

if __name__ == "__main__":
    run_linters()
    format_code()

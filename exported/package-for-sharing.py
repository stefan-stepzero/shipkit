#!/usr/bin/env python3
"""
package-for-sharing.py - Package Shipkit for local distribution

Creates a distributable ZIP containing only the files needed for installation.
Excludes development files, git history, and working documents.
"""

import os
import sys
import zipfile
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        # Python < 3.7 fallback
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Folders to include (relative to repo root)
INCLUDE_FOLDERS = [
    "install",      # All installation source files
    "installers",   # Installer scripts
    "help",         # HTML documentation
]

# Files to include from root (relative to repo root)
INCLUDE_ROOT_FILES = [
    "README.md",
    "LICENSE",
]

# Patterns to always exclude (even within included folders)
EXCLUDE_PATTERNS = [
    "__pycache__",
    ".pyc",
    ".pyo",
    ".DS_Store",
    "Thumbs.db",
    ".git",
    "*.backup",
    "*.bak",
    "*.tmp",
]

# ═══════════════════════════════════════════════════════════════════════════════
# COLORS
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    MAGENTA = '\033[1;35m'

def print_success(msg):
    print(f"  {Colors.GREEN}✓{Colors.RESET} {msg}")

def print_info(msg):
    print(f"  {Colors.CYAN}→{Colors.RESET} {msg}")

def print_warning(msg):
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {msg}")

def print_error(msg):
    print(f"  {Colors.RED}✗{Colors.RESET} {msg}")

# ═══════════════════════════════════════════════════════════════════════════════
# PACKAGING LOGIC
# ═══════════════════════════════════════════════════════════════════════════════

def should_exclude(path: Path) -> bool:
    """Check if a path should be excluded based on patterns."""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*"):
            # Wildcard pattern
            if path_str.endswith(pattern[1:]):
                return True
        else:
            # Exact match in path
            if pattern in path_str.split(os.sep):
                return True
    return False


def get_files_to_package(repo_root: Path) -> list[tuple[Path, str]]:
    """
    Get list of (source_path, archive_name) tuples for all files to package.
    """
    files = []

    # Add folders
    for folder in INCLUDE_FOLDERS:
        folder_path = repo_root / folder
        if folder_path.exists():
            for file_path in folder_path.rglob("*"):
                if file_path.is_file() and not should_exclude(file_path):
                    # Archive path is relative to repo root
                    archive_name = str(file_path.relative_to(repo_root))
                    files.append((file_path, archive_name))
        else:
            print_warning(f"Folder not found: {folder}")

    # Add root files
    for filename in INCLUDE_ROOT_FILES:
        file_path = repo_root / filename
        if file_path.exists():
            files.append((file_path, filename))
        # Don't warn for missing optional files like LICENSE

    return files


def create_package(repo_root: Path, output_path: Path) -> tuple[int, int]:
    """
    Create the ZIP package.
    Returns (file_count, size_bytes).
    """
    files = get_files_to_package(repo_root)

    if not files:
        print_error("No files found to package!")
        return 0, 0

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for source_path, archive_name in files:
            zf.write(source_path, archive_name)

    return len(files), output_path.stat().st_size


def format_size(size_bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def show_summary(files: list[tuple[Path, str]]):
    """Show what will be packaged."""
    # Group by top-level folder
    folders = {}
    for _, archive_name in files:
        top_folder = archive_name.split(os.sep)[0]
        if top_folder not in folders:
            folders[top_folder] = 0
        folders[top_folder] += 1

    print()
    print(f"  {Colors.BOLD}Contents:{Colors.RESET}")
    print()
    for folder, count in sorted(folders.items()):
        print(f"    {Colors.CYAN}{folder}/{Colors.RESET} ({count} files)")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    # Determine paths
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent  # exported/ folder
    repo_root = script_dir.parent    # repo root (one level up from exported/)

    # Generate output filename with timestamp (output to same folder as script)
    timestamp = datetime.now().strftime("%Y%m%d")
    output_name = f"shipkit-{timestamp}.zip"
    output_path = script_dir / output_name

    # Header
    print()
    print(f"{Colors.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}Shipkit Packager{Colors.RESET}")
    print(f"{Colors.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()

    print_info(f"Source: {repo_root}")
    print_info(f"Output: {output_path}")

    # Get files and show summary
    files = get_files_to_package(repo_root)
    show_summary(files)

    # Create package
    print_info("Creating ZIP package...")
    file_count, size_bytes = create_package(repo_root, output_path)

    if file_count == 0:
        print_error("Packaging failed - no files were added")
        sys.exit(1)

    # Success
    print()
    print(f"{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print_success(f"Package created: {output_name}")
    print_success(f"Files: {file_count}")
    print_success(f"Size: {format_size(size_bytes)}")
    print(f"{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()

    print(f"  {Colors.BOLD}To install from this package:{Colors.RESET}")
    print()
    print(f"    1. Unzip to a temporary location")
    print(f"    2. Run: {Colors.CYAN}python installers/install.py{Colors.RESET}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_warning("Packaging cancelled.")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Packaging failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

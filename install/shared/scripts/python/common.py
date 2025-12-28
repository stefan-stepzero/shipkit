#!/usr/bin/env python3
"""
Common utilities for Shipkit Python scripts
"""

import os
import shutil
from pathlib import Path
from typing import Optional


def create_directory(path: str) -> None:
    """Create a directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created directory: {path}")


def copy_file(source: str, dest: str) -> None:
    """Copy a file from source to destination."""
    shutil.copy2(source, dest)
    print(f"✓ Copied: {source} → {dest}")


def copy_template(template_path: str, output_path: str) -> None:
    """Copy a template file to output location."""
    create_directory(str(Path(output_path).parent))
    copy_file(template_path, output_path)


def get_skill_root() -> Path:
    """Get the root .shipkit/skills directory."""
    return Path(".shipkit/skills")


def get_skill_path(skill_name: str) -> Path:
    """Get the path to a specific skill's directory."""
    return get_skill_root() / skill_name


def ensure_skill_structure(skill_name: str) -> None:
    """Ensure skill directory structure exists."""
    skill_path = get_skill_path(skill_name)
    create_directory(str(skill_path / "outputs"))
    create_directory(str(skill_path / "templates"))
    create_directory(str(skill_path / "scripts"))
    create_directory(str(skill_path / "references"))


def report_output_path(file_path: str, description: str = "Output") -> None:
    """Report the path of a created output file."""
    print(f"\n📁 {description}: {file_path}\n")

#!/usr/bin/env python3
"""
install.py - Shipkit Installer (Python)
Manifest-based installer with customizable skill/agent selection

Usage:
    python install.py                      # Interactive install from local repo
    python install.py --from-github        # Download and install from GitHub
    python install.py -y --all-skills      # Non-interactive install
    python -X utf8 install.py              # Windows: force UTF-8 encoding
"""

import os
import sys
import json
import shutil
import argparse
import platform
import tempfile
import zipfile
import io
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

# ═══════════════════════════════════════════════════════════════════════════════
# WINDOWS ENCODING FIX
# ═══════════════════════════════════════════════════════════════════════════════

def setup_encoding():
    """Setup UTF-8 encoding on Windows"""
    if platform.system() == "Windows":
        # Try to set console to UTF-8
        try:
            import subprocess
            subprocess.run(["chcp", "65001"], capture_output=True, shell=True)
        except Exception:
            pass
        # Set stdout/stderr encoding
        if hasattr(sys.stdout, 'reconfigure'):
            try:
                sys.stdout.reconfigure(encoding='utf-8', errors='replace')
                sys.stderr.reconfigure(encoding='utf-8', errors='replace')
            except Exception:
                pass

setup_encoding()

# ═══════════════════════════════════════════════════════════════════════════════
# COLORS & STYLING (with ASCII fallbacks for Windows)
# ═══════════════════════════════════════════════════════════════════════════════

def supports_unicode():
    """Check if terminal supports Unicode"""
    if platform.system() == "Windows":
        # Check if running in Windows Terminal or modern console
        return os.environ.get("WT_SESSION") or os.environ.get("TERM_PROGRAM")
    return True

class Colors:
    """ANSI color codes"""
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    MAGENTA = '\033[1;35m'
    BRIGHT_GREEN = '\033[1;32m'
    BRIGHT_CYAN = '\033[1;36m'
    BRIGHT_MAGENTA = '\033[1;35m'

class Symbols:
    """Unicode symbols with ASCII fallbacks"""
    if supports_unicode():
        CHECK = '✓'
        CROSS = '✗'
        WARN = '⚠'
        ARROW = '→'
        BULLET = '•'
    else:
        CHECK = '+'
        CROSS = 'x'
        WARN = '!'
        ARROW = '->'
        BULLET = '*'

def print_success(msg):
    print(f"  {Colors.GREEN}{Symbols.CHECK}{Colors.RESET} {msg}")

def print_info(msg):
    print(f"  {Colors.CYAN}{Symbols.ARROW}{Colors.RESET} {msg}")

def print_warning(msg):
    print(f"  {Colors.YELLOW}{Symbols.WARN}{Colors.RESET} {msg}")

def print_error(msg):
    print(f"  {Colors.RED}{Symbols.CROSS}{Colors.RESET} {msg}")

def print_bullet(msg):
    print(f"  {Colors.DIM}{Symbols.BULLET}{Colors.RESET} {msg}")

# ═══════════════════════════════════════════════════════════════════════════════
# LOGO
# ═══════════════════════════════════════════════════════════════════════════════

def show_logo(edition="default"):
    """Show Shipkit logo with edition-specific info"""
    print()
    print(f"{Colors.BRIGHT_MAGENTA}", end='')
    print(r"""
    ┌──────────────────────────────────────────────────────────────────────┐
    │                                                        /\            │
    │   ███████╗██╗  ██╗██╗██████╗ ██╗  ██╗██╗████████╗     /  \           │
    │   ██╔════╝██║  ██║██║██╔══██╗██║ ██╔╝██║╚══██╔══╝    / /| \          │
    │   ███████╗███████║██║██████╔╝█████╔╝ ██║   ██║      / / |  \         │
    │   ╚════██║██╔══██║██║██╔═══╝ ██╔═██╗ ██║   ██║     /_/__|___\        │
    │   ███████║██║  ██║██║██║     ██║  ██╗██║   ██║     \________/        │
    │   ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝  ╚═╝╚═╝   ╚═╝     ~~~~~~~~~~        │
    │                                                                      │
    └──────────────────────────────────────────────────────────────────────┘
    """)
    print(f"{Colors.RESET}")

    print(f"{Colors.DIM}         Solo Dev Product Development Framework{Colors.RESET}")
    print(f"{Colors.DIM}              Customizable Skills • Agents • Fast Iteration{Colors.RESET}")
    print()

# ═══════════════════════════════════════════════════════════════════════════════
# MANIFEST HANDLING
# ═══════════════════════════════════════════════════════════════════════════════

def load_manifest(repo_root, profile):
    """Load manifest file for the selected profile"""
    manifest_path = repo_root / "install" / "profiles" / f"{profile}.manifest.json"

    if not manifest_path.exists():
        print_error(f"Manifest not found: {manifest_path}")
        sys.exit(1)

    try:
        with open(manifest_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print_error(f"Invalid manifest JSON: {e}")
        sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

def prompt_for_profile():
    """Prompt user to select a profile"""
    print()
    print(f"  {Colors.BOLD}Select Profile:{Colors.RESET}")
    print()
    print(f"  {Colors.CYAN}[1]{Colors.RESET} Full        - All 23 skills + 6 agents (recommended)")
    print(f"  {Colors.CYAN}[2]{Colors.RESET} Discovery   - Vision & planning skills (11 skills)")
    print(f"  {Colors.CYAN}[3]{Colors.RESET} Minimal     - Core workflow only (5 skills)")
    print()

    while True:
        choice = input(f"  {Colors.BOLD}Select profile [1-3]:{Colors.RESET} ").strip()
        if choice == "1" or choice == "":
            return "shipkit"
        elif choice == "2":
            return "discovery"
        elif choice == "3":
            return "minimal"
        else:
            print_warning("Invalid choice. Please enter 1, 2, or 3.")

def prompt_for_language():
    """Prompt user to select scripting language"""
    print()
    print(f"  {Colors.BOLD}Select Scripting Language:{Colors.RESET}")
    print()
    print(f"  {Colors.CYAN}[1]{Colors.RESET} Bash      - Traditional shell scripts (cross-platform)")
    print(f"  {Colors.CYAN}[2]{Colors.RESET} Python    - Python scripts (recommended for Windows)")
    print()

    while True:
        choice = input(f"  {Colors.BOLD}Select language [1-2]:{Colors.RESET} ").strip()
        if choice == "1":
            return "bash"
        elif choice == "2":
            return "python"
        else:
            print_warning("Invalid choice. Please enter 1 or 2.")

def prompt_for_target_directory():
    """Prompt user for installation target directory"""
    print()
    print(f"  {Colors.BOLD}Where would you like to install Shipkit?{Colors.RESET}")
    print(f"  {Colors.DIM}(Press Enter for current directory: {Path.cwd()}){Colors.RESET}")
    print()

    user_input = input(f"  {Colors.CYAN}Install path:{Colors.RESET} ").strip()

    if not user_input:
        return Path.cwd()

    return Path(user_input).resolve()

def confirm(prompt, default=True):
    """Ask yes/no confirmation"""
    hint = "[Y/n]" if default else "[y/N]"
    response = input(f"  {Colors.BOLD}{prompt}{Colors.RESET} {Colors.DIM}{hint}{Colors.RESET} ").strip().lower()

    if not response:
        return default

    return response in ['y', 'yes']

# ═══════════════════════════════════════════════════════════════════════════════
# SKILL SELECTION
# ═══════════════════════════════════════════════════════════════════════════════

def prompt_for_skills(manifest):
    """Prompt user to select which skills to install"""
    mandatory = manifest["skills"]["mandatory"]
    optional = manifest["skills"]["optional"]

    print()
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}Skill Selection{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()
    print(f"  {Colors.DIM}Mandatory skills (always installed):{Colors.RESET}")
    for skill in mandatory:
        print(f"    {Colors.GREEN}✓{Colors.RESET} {skill}")
    print()

    # Flatten optional skills for selection
    all_optional = []
    category_indices = {}  # Track which indices belong to which category

    for category, skills in optional.items():
        start_idx = len(all_optional)
        for skill in skills:
            all_optional.append({"category": category, **skill})
        category_indices[category] = (start_idx, len(all_optional))

    # All selected by default
    selected = [True] * len(all_optional)

    while True:
        # Display by category
        idx = 0
        for category, skills in optional.items():
            print(f"  {Colors.BOLD}{category}:{Colors.RESET}")
            for skill in skills:
                marker = f"{Colors.GREEN}✓{Colors.RESET}" if selected[idx] else " "
                print(f"    [{idx+1:2}] {marker} {Colors.CYAN}{skill['name']:30}{Colors.RESET} {Colors.DIM}{skill['desc']}{Colors.RESET}")
                idx += 1
            print()

        print(f"  {Colors.DIM}Commands:{Colors.RESET}")
        print(f"  {Colors.DIM}  [numbers]  Toggle individual skills (e.g., 1 3 5){Colors.RESET}")
        print(f"  {Colors.DIM}  [a]        Select all{Colors.RESET}")
        print(f"  {Colors.DIM}  [n]        Select none (minimal install){Colors.RESET}")
        print(f"  {Colors.DIM}  [c:name]   Toggle category (e.g., c:Vision){Colors.RESET}")
        print(f"  {Colors.DIM}  [Enter]    Continue with selection{Colors.RESET}")
        print()

        choice = input(f"  {Colors.BOLD}Selection:{Colors.RESET} ").strip().lower()

        if choice == "":
            break
        elif choice == "a":
            selected = [True] * len(all_optional)
        elif choice == "n":
            selected = [False] * len(all_optional)
        elif choice.startswith("c:"):
            # Toggle category
            cat_search = choice[2:].strip().lower()
            for category, (start, end) in category_indices.items():
                if cat_search in category.lower():
                    # Toggle all in this category
                    current_state = all(selected[start:end])
                    for i in range(start, end):
                        selected[i] = not current_state
                    break
        else:
            # Parse numbers
            try:
                nums = [int(x.strip()) for x in choice.replace(",", " ").split()]
                for num in nums:
                    if 1 <= num <= len(all_optional):
                        selected[num-1] = not selected[num-1]
            except ValueError:
                print_warning("Invalid input.")

        # Clear and redraw
        print()

    # Build final skill list
    selected_skills = list(mandatory)  # Start with mandatory
    for i, skill in enumerate(all_optional):
        if selected[i]:
            selected_skills.append(skill["name"])

    return selected_skills

# ═══════════════════════════════════════════════════════════════════════════════
# AGENT SELECTION
# ═══════════════════════════════════════════════════════════════════════════════

def prompt_for_agents(manifest):
    """Prompt user to select which agents to install"""
    agents = manifest.get("agents", [])

    if not agents:
        return []

    print()
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}Agent Selection{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()
    print(f"  {Colors.DIM}Agents are specialized personas for different tasks.{Colors.RESET}")
    print(f"  {Colors.DIM}They're optional but helpful for focused work.{Colors.RESET}")
    print()

    # All selected by default
    selected = [True] * len(agents)

    while True:
        for i, agent in enumerate(agents):
            marker = f"{Colors.GREEN}✓{Colors.RESET}" if selected[i] else " "
            print(f"  [{i+1}] {marker} {Colors.CYAN}{agent['name']:32}{Colors.RESET} {Colors.DIM}{agent['desc']}{Colors.RESET}")

        print()
        print(f"  {Colors.DIM}Enter numbers to toggle, or:{Colors.RESET}")
        print(f"  {Colors.DIM}  [a] Select all  [n] Select none  [Enter] Continue{Colors.RESET}")
        print()

        choice = input(f"  {Colors.BOLD}Selection:{Colors.RESET} ").strip().lower()

        if choice == "":
            break
        elif choice == "a":
            selected = [True] * len(agents)
        elif choice == "n":
            selected = [False] * len(agents)
        else:
            try:
                nums = [int(x.strip()) for x in choice.replace(",", " ").split()]
                for num in nums:
                    if 1 <= num <= len(agents):
                        selected[num-1] = not selected[num-1]
            except ValueError:
                print_warning("Invalid input.")

        print()

    return [agent["name"] for i, agent in enumerate(agents) if selected[i]]

# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE.MD HANDLING
# ═══════════════════════════════════════════════════════════════════════════════

def prompt_for_claude_md_action(target_dir):
    """Prompt user for how to handle existing CLAUDE.md"""
    claude_md_path = target_dir / "CLAUDE.md"

    if not claude_md_path.exists():
        return "install"  # No existing file, just install

    print()
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}CLAUDE.md Already Exists{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()
    print(f"  {Colors.DIM}Found existing CLAUDE.md at {target_dir}{Colors.RESET}")
    print()
    print(f"  {Colors.CYAN}[1]{Colors.RESET} Skip       - Keep your existing CLAUDE.md unchanged")
    print(f"  {Colors.CYAN}[2]{Colors.RESET} Overwrite  - Replace with Shipkit template")
    print(f"  {Colors.CYAN}[3]{Colors.RESET} Merge      - Append Shipkit sections to existing file")
    print()

    while True:
        choice = input(f"  {Colors.BOLD}Select action [1-3]:{Colors.RESET} ").strip()
        if choice == "1":
            return "skip"
        elif choice == "2":
            return "overwrite"
        elif choice == "3":
            return "merge"
        else:
            print_warning("Invalid choice. Please enter 1, 2, or 3.")

def merge_claude_md(existing_path, template_path):
    """Merge Shipkit template into existing CLAUDE.md"""
    with open(existing_path, 'r', encoding='utf-8') as f:
        existing_content = f.read()

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Check if already merged
    if "## Skills Reference" in existing_content and "/shipkit-" in existing_content:
        return existing_content  # Already has Shipkit content

    # Find sections to append from template
    sections_to_add = []

    # Extract key sections from template
    template_sections = [
        ("## Context Files", "## Codebase Navigation"),
        ("## Codebase Navigation", "## Skills Reference"),
        ("## Skills Reference", "## Meta-Behavior"),
    ]

    for start_marker, end_marker in template_sections:
        if start_marker in template_content:
            start_idx = template_content.find(start_marker)
            if end_marker and end_marker in template_content:
                end_idx = template_content.find(end_marker)
                section = template_content[start_idx:end_idx].strip()
            else:
                section = template_content[start_idx:].strip()

            # Only add if not already present
            if start_marker not in existing_content:
                sections_to_add.append(section)

    # Append sections
    merged = existing_content.rstrip()
    if sections_to_add:
        merged += "\n\n---\n\n# Shipkit Integration\n\n"
        merged += "\n\n".join(sections_to_add)
        merged += "\n"

    return merged

# ═══════════════════════════════════════════════════════════════════════════════
# GITHUB DOWNLOAD
# ═══════════════════════════════════════════════════════════════════════════════

def download_from_github(repo, branch):
    """Download and extract Shipkit from GitHub, return temp directory path"""
    print()
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}Downloading from GitHub{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()

    zip_url = f"https://github.com/{repo}/archive/refs/heads/{branch}.zip"
    print_info(f"Downloading from: {repo} ({branch} branch)")
    print_info(f"URL: {zip_url}")

    try:
        # Download the zip file
        print_info("Fetching archive...")
        with urlopen(zip_url, timeout=60) as response:
            zip_data = response.read()
        print_success(f"Downloaded {len(zip_data) / 1024:.1f} KB")

        # Create temp directory
        temp_dir = Path(tempfile.mkdtemp(prefix="shipkit_"))
        print_info(f"Extracting to: {temp_dir}")

        # Extract zip
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
            zf.extractall(temp_dir)

        # Find the extracted folder (usually repo-branch format)
        extracted_dirs = [d for d in temp_dir.iterdir() if d.is_dir()]
        if not extracted_dirs:
            print_error("No directory found in archive")
            return None

        repo_root = extracted_dirs[0]
        print_success(f"Extracted to: {repo_root.name}")

        return repo_root

    except URLError as e:
        print_error(f"Failed to download: {e}")
        print()
        print_info("Check that:")
        print_bullet(f"Repository exists: github.com/{repo}")
        print_bullet(f"Branch exists: {branch}")
        print_bullet("You have internet access")
        return None
    except zipfile.BadZipFile:
        print_error("Downloaded file is not a valid zip archive")
        return None
    except Exception as e:
        print_error(f"Download failed: {e}")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def verify_source_files(repo_root):
    """Verify all required source files exist"""
    print(f"  {Colors.BOLD}Verifying source files...{Colors.RESET}")
    print()

    required_paths = [
        "install/shared",
        "install/skills",
        "install/agents",
        "install/settings",
        "install/claude-md",
        "install/profiles"
    ]

    missing = 0
    for path in required_paths:
        full_path = repo_root / path
        if full_path.exists():
            print_success(path)
        else:
            print_error(f"{path} (missing)")
            missing += 1

    print()

    if missing > 0:
        print_error("Source directory is incomplete!")
        print()
        print(f"  {Colors.DIM}Expected shipkit structure at: {repo_root}{Colors.RESET}")
        return False

    return True

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALLATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def install_shared_core(repo_root, target_dir, language, edition):
    """Install shared core files (hooks, scripts, git files)"""
    print()
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}Installing shared core{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()

    shared_dir = repo_root / "install" / "shared"

    # Hooks (edition-specific)
    print_info("Installing hooks...")
    hooks_src = shared_dir / "hooks"
    hooks_dest = target_dir / ".claude" / "hooks"
    hooks_dest.mkdir(parents=True, exist_ok=True)

    # Install shipkit hooks
    shutil.copy2(hooks_src / "shipkit-session-start.py", hooks_dest / "session-start.py")
    shutil.copy2(hooks_src / "shipkit-after-skill-router.py", hooks_dest / "after-skill-router.py")
    shutil.copy2(hooks_src / "shipkit-track-skill-usage.py", hooks_dest / "shipkit-track-skill-usage.py")
    shutil.copy2(hooks_src / "shipkit-relentless-stop-hook.py", hooks_dest / "shipkit-relentless-stop-hook.py")
    print_success("Hooks installed")

    # Scripts (language-specific)
    print_info(f"Installing {language} scripts...")
    scripts_src = shared_dir / "scripts" / language
    if language == "bash":
        scripts_dest = target_dir / ".shipkit" / "scripts" / "bash"
    else:
        scripts_dest = target_dir / ".shipkit" / "scripts"
    scripts_dest.mkdir(parents=True, exist_ok=True)
    shutil.copytree(scripts_src, scripts_dest, dirs_exist_ok=True)
    print_success(f"{language.capitalize()} scripts installed")

    # Git files
    print_info("Installing git configuration files...")
    filename = ".gitignore"
    src = shared_dir / filename
    dest = target_dir / filename
    if not dest.exists():
        shutil.copy2(src, dest)
        print_success(f"{filename} installed")
    else:
        print_warning(f"{filename} already exists, skipping")

def install_edition_files(repo_root, target_dir, manifest, language, selected_skills, claude_md_action, skip_prompts=False):
    """Install edition-specific settings and CLAUDE.md"""
    print()
    print(f"  {Colors.BOLD}Installing edition-specific files{Colors.RESET}")
    print()

    # Settings - generate dynamically based on selected skills
    settings_dest = target_dir / ".claude" / "settings.json"
    settings_dest.parent.mkdir(parents=True, exist_ok=True)

    if not settings_dest.exists():
        settings = generate_settings(manifest, language, selected_skills)
        with open(settings_dest, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
        print_success(f"Settings installed with {len(selected_skills)} skill permissions")
    else:
        print_warning("settings.json exists, preserving your custom config")
        # Still update skill permissions (auto-yes if skip_prompts)
        if skip_prompts or confirm("Update skill permissions in existing settings?", default=True):
            update_skill_permissions(settings_dest, selected_skills)
            print_success("Skill permissions updated")

    # CLAUDE.md
    claude_md_file = manifest["claudeMdFile"]
    claude_md_src = repo_root / "install" / "claude-md" / claude_md_file
    claude_md_dest = target_dir / "CLAUDE.md"

    if claude_md_action == "install":
        shutil.copy2(claude_md_src, claude_md_dest)
        print_success(f"CLAUDE.md installed")
    elif claude_md_action == "skip":
        print_info("CLAUDE.md skipped (keeping existing)")
    elif claude_md_action == "overwrite":
        shutil.copy2(claude_md_src, claude_md_dest)
        print_success("CLAUDE.md overwritten with Shipkit template")
    elif claude_md_action == "merge":
        # Fix: Check if file exists before attempting merge
        if not claude_md_dest.exists():
            # No existing file to merge with, just install
            shutil.copy2(claude_md_src, claude_md_dest)
            print_success("CLAUDE.md installed (no existing file to merge)")
        else:
            merged_content = merge_claude_md(claude_md_dest, claude_md_src)
            with open(claude_md_dest, 'w', encoding='utf-8') as f:
                f.write(merged_content)
            print_success("CLAUDE.md merged with Shipkit sections")

def generate_settings(manifest, language, selected_skills):
    """Generate settings.json with only selected skill permissions"""
    # Base settings template
    settings = {
        "permissions": {
            "allow": [
                "Read",
                "Read(.env.example)",
                "Read(**/.env.example)",
                "Read(.env.*.example)",
                "Read(**/.env.*.example)",

                "Write(src/**)",
                "Write(app/**)",
                "Write(components/**)",
                "Write(lib/**)",
                "Write(utils/**)",
                "Write(tests/**)",
                "Write(__tests__/**)",
                "Write(*.ts)",
                "Write(*.tsx)",
                "Write(*.js)",
                "Write(*.jsx)",
                "Write(*.py)",
                "Write(*.json)",
                "Write(*.md)",
                "Write(*.yaml)",
                "Write(*.yml)",
                "Write(*.toml)",
                "Write(*.html)",
                "Write(*.css)",
                "Write(*.scss)",
                "Write(*.sass)",
                "Write(*.sh)",
                "Write(*.sql)",
                "Write(*.xml)",
                "Write(*.txt)",
                "Write(package.json)",
                "Write(pyproject.toml)",
                "Write(requirements.txt)",

                "Bash(git:*)",
                "Bash(python:*)",
                "Bash(pip:*)",
                "Bash(poetry:*)",
                "Bash(pytest:*)",
                "Bash(black:*)",
                "Bash(ruff:*)",
                "Bash(mypy:*)",
                "Bash(uvicorn:*)",
                "Bash(node:*)",
                "Bash(npm:*)",
                "Bash(npx:*)",
                "Bash(pnpm:*)",
                "Bash(yarn:*)",
                "Bash(tsc:*)",
                "Bash(eslint:*)",
                "Bash(prettier:*)",
                "Bash(vercel:*)",
                "Bash(docker:*)",
                "Bash(docker-compose:*)",
                "Bash(ls:*)",
                "Bash(cat:*)",
                "Bash(grep:*)",
                "Bash(find:*)",
                "Bash(wc:*)",
                "Bash(chmod:*)",
                "Bash(pwd:*)",
                "Bash(cd:*)",
                "Bash(echo:*)",
                "Bash(mkdir:*)",
                "Bash(touch:*)",
                "Bash(mv:*)",
                "Bash(cp:*)",
                "Bash(rm:*)",
                "Bash(curl:*)",
                "Bash(wget:*)",
                "Bash(sed:*)",
                "Bash(awk:*)",
                "Bash(sort:*)",
                "Bash(uniq:*)",
                "Bash(diff:*)",
                "Bash(tree:*)",

                "WebFetch(domain:github.com)",
                "WebFetch(domain:raw.githubusercontent.com)",
                "WebFetch(domain:docs.anthropic.com)",
                "WebFetch(domain:nextjs.org)",
                "WebFetch(domain:python.org)",
                "WebFetch(domain:fastapi.tiangolo.com)",
                "WebFetch(domain:pypi.org)",
                "WebFetch(domain:npmjs.com)",
                "WebFetch(domain:stackoverflow.com)",
                "WebFetch(domain:developer.mozilla.org)",
            ],
            "deny": [
                "Bash(sudo:*)",
                "Bash(su:*)",
                "Bash(ssh:*)"
            ]
        },
        "defaultMode": "acceptEdits",
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "startup|resume|clear|compact",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python -X utf8 .claude/hooks/session-start.py"
                        }
                    ]
                }
            ],
            "PostToolUse": [
                {
                    "matcher": "Skill",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python -X utf8 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/shipkit-track-skill-usage.py"
                        }
                    ]
                }
            ],
            "Stop": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python -X utf8 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/shipkit-after-skill-router.py"
                        }
                    ]
                },
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python -X utf8 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/shipkit-relentless-stop-hook.py",
                            "timeout": 180
                        }
                    ]
                }
            ]
        },
        "skills": {
            "description": "Skill configuration and defaults",
            "autoLoadConstitutions": False
        },
        "workspace": {
            "description": "Workspace paths and conventions",
            "contextPath": ".shipkit",
            "specsPath": ".shipkit/specs",
            "plansPath": ".shipkit/plans"
        },
        "shipkit": {
            "edition": manifest["edition"],
            "language": language,
            "installedSkills": selected_skills
        }
    }

    # Add skill permissions for selected skills only
    for skill in selected_skills:
        settings["permissions"]["allow"].append(f"Skill({skill})")

    return settings

def update_skill_permissions(settings_path, selected_skills):
    """Update skill permissions in existing settings.json"""
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = json.load(f)

    # Remove existing Skill() permissions
    allow_list = settings.get("permissions", {}).get("allow", [])
    allow_list = [p for p in allow_list if not p.startswith("Skill(")]

    # Add new skill permissions
    for skill in selected_skills:
        allow_list.append(f"Skill({skill})")

    settings["permissions"]["allow"] = allow_list

    # Update installed skills list
    if "shipkit" not in settings:
        settings["shipkit"] = {}
    settings["shipkit"]["installedSkills"] = selected_skills

    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2)

def install_skills(repo_root, target_dir, selected_skills):
    """Install selected skill definitions"""
    print()
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}Installing skills{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()

    print_info(f"Installing {len(selected_skills)} skill definitions...")

    installed = 0
    for skill_name in selected_skills:
        skill_src = repo_root / "install" / "skills" / skill_name
        skill_dest = target_dir / ".claude" / "skills" / skill_name

        if skill_src.exists():
            skill_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(skill_src, skill_dest, dirs_exist_ok=True)
            installed += 1
        else:
            print_warning(f"Skill not found: {skill_name}")

    print_success(f"Installed {installed} skill definitions")

def install_agents(repo_root, target_dir, selected_agents):
    """Install selected agent personas"""
    print()
    print(f"  {Colors.BOLD}Installing agent personas{Colors.RESET}")
    print()

    if not selected_agents:
        print_info("No agents selected")
        return

    agents_dir = target_dir / ".claude" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for agent_name in selected_agents:
        agent_file = f"{agent_name}.md"
        agent_src = repo_root / "install" / "agents" / agent_file
        agent_dest = agents_dir / agent_file

        if agent_src.exists():
            shutil.copy2(agent_src, agent_dest)
            count += 1
        else:
            print_warning(f"Agent not found: {agent_file}")

    print_success(f"Installed {count} agent personas")

def delete_unused_language(target_dir, language):
    """Delete scripts for the language not selected"""
    print()
    print(f"  {Colors.BOLD}Cleaning up unused language files{Colors.RESET}")
    print()

    if language == "python":
        delete_ext = ".sh"
        keep_lang = "Python"
    else:
        delete_ext = ".py"
        keep_lang = "Bash"

    print_info(f"Keeping {keep_lang} scripts, removing others...")

    # Delete from .claude/skills
    skills_dir = target_dir / ".claude" / "skills"
    if skills_dir.exists():
        for script in skills_dir.rglob(f"*{delete_ext}"):
            script.unlink()

    # Delete from .claude/hooks
    hooks_dir = target_dir / ".claude" / "hooks"
    if hooks_dir.exists():
        for script in hooks_dir.rglob(f"*{delete_ext}"):
            script.unlink()

    # Delete from .shipkit/skills
    shipkit_skills_dir = target_dir / ".shipkit" / "skills"
    if shipkit_skills_dir.exists():
        for script in shipkit_skills_dir.rglob(f"*{delete_ext}"):
            script.unlink()

    print_success(f"Removed {delete_ext} files, kept {keep_lang} scripts")

def make_scripts_executable(target_dir, language):
    """Make scripts executable (Unix-like systems)"""
    if platform.system() == "Windows":
        return

    print()
    print_info("Making scripts executable...")

    if language == "bash":
        for script in target_dir.rglob("*.sh"):
            script.chmod(0o755)
        print_success("Bash scripts are now executable")
    else:
        for script in target_dir.rglob("*.py"):
            script.chmod(0o755)
        print_success("Python scripts are now executable")

# ═══════════════════════════════════════════════════════════════════════════════
# MCP CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

def prompt_for_mcps(manifest):
    """Prompt user to select which MCP servers to install"""
    mcps = manifest.get("mcps", {}).get("recommended", [])

    if not mcps:
        return []

    print()
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}MCP Servers (Model Context Protocol){Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()
    print(f"  {Colors.DIM}MCPs extend Claude with external tools and APIs.{Colors.RESET}")
    print(f"  {Colors.DIM}Token cost shown = context used when MCP is active.{Colors.RESET}")
    print()

    selected = [True] * len(mcps)

    while True:
        for i, mcp in enumerate(mcps):
            marker = f"{Colors.GREEN}✓{Colors.RESET}" if selected[i] else " "
            name = mcp["name"]
            purpose = mcp["purpose"]
            tokens = mcp.get("tokens", "")
            prereq = f" {Colors.YELLOW}(requires: {mcp['prereq']}){Colors.RESET}" if mcp.get("prereq") else ""

            print(f"  [{i+1}] {marker} {Colors.CYAN}{name:16}{Colors.RESET} - {purpose} {Colors.DIM}({tokens}){Colors.RESET}{prereq}")

        print()
        print(f"  {Colors.DIM}Enter numbers to toggle, or:{Colors.RESET}")
        print(f"  {Colors.DIM}  [a] Select all  [n] Select none  [Enter] Continue{Colors.RESET}")
        print()

        choice = input(f"  {Colors.BOLD}Selection:{Colors.RESET} ").strip().lower()

        if choice == "":
            break
        elif choice == "a":
            selected = [True] * len(mcps)
        elif choice == "n":
            selected = [False] * len(mcps)
        else:
            try:
                nums = [int(x.strip()) for x in choice.replace(",", " ").split()]
                for num in nums:
                    if 1 <= num <= len(mcps):
                        selected[num-1] = not selected[num-1]
            except ValueError:
                print_warning("Invalid input. Enter numbers, 'a', 'n', or press Enter.")

        print()

    return [mcp for i, mcp in enumerate(mcps) if selected[i]]

def install_mcp_config(target_dir, selected_mcps):
    """Install MCP server configuration for selected MCPs"""
    if not selected_mcps:
        print_info("No MCP servers selected, skipping .mcp.json")
        return

    mcp_config_path = target_dir / ".mcp.json"

    if mcp_config_path.exists():
        print_warning(f".mcp.json already exists at {target_dir}")
        if not confirm("Overwrite with new MCP configuration?", default=False):
            print_info("Keeping existing .mcp.json")
            return

    try:
        mcp_servers = {}
        prereqs = []

        for mcp in selected_mcps:
            name = mcp["name"]
            command = mcp["command"]
            args = mcp["args"]

            if platform.system() == "Windows" and command == "npx":
                mcp_servers[name] = {
                    "command": "cmd",
                    "args": ["/c", "npx"] + args
                }
            else:
                mcp_servers[name] = {
                    "command": command,
                    "args": args
                }

            if mcp.get("prereq"):
                prereqs.append((name, mcp["prereq"]))

        mcp_config = {"mcpServers": mcp_servers}

        with open(mcp_config_path, 'w', encoding='utf-8') as f:
            json.dump(mcp_config, f, indent=2)
            f.write('\n')

        print_success(f"MCP configuration installed ({len(selected_mcps)} servers)")

        if prereqs:
            print()
            print_warning("Some MCPs require setup before use:")
            for name, prereq in prereqs:
                print(f"    {Colors.CYAN}{name}{Colors.RESET}: {Colors.YELLOW}{prereq}{Colors.RESET}")

    except Exception as e:
        print_error(f"Failed to install MCP config: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETION
# ═══════════════════════════════════════════════════════════════════════════════

def install_html_docs(repo_root, target_dir):
    """Copy HTML overview to target project for easy reference"""
    html_dir = repo_root / "docs" / "generated"
    overview_file = html_dir / "shipkit-overview.html"

    if not overview_file.exists():
        return None

    # Copy to .shipkit/ for easy access
    dest_file = target_dir / ".shipkit" / "shipkit-overview.html"
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(overview_file, dest_file)
    return dest_file

def open_html_docs(repo_root, target_dir, edition):
    """Copy HTML overview to project and open in browser"""
    import webbrowser

    # First, copy to target project
    installed_file = install_html_docs(repo_root, target_dir)

    if installed_file and installed_file.exists():
        print()
        print(f"  {Colors.BRIGHT_CYAN}📖 Opening documentation...{Colors.RESET}")
        print()
        print_success(f"HTML overview installed to .shipkit/shipkit-overview.html")

        try:
            webbrowser.open(f"file://{installed_file}")
            print_success(f"Opened in browser")
        except Exception as e:
            print_warning(f"Could not open in browser: {e}")
            print_info(f"Open manually: {installed_file}")
    else:
        print_warning("HTML overview not found in source")

def show_completion(target_dir, selected_skills, selected_agents, language):
    """Show completion message"""
    print()
    print()
    print(f"{Colors.BRIGHT_GREEN}")
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ✓  Installation Complete!                               ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    print(f"{Colors.RESET}")

    print(f"  {Colors.BOLD}What was installed:{Colors.RESET}")
    print()
    print_success(f"{len(selected_skills)} skill definitions (.claude/skills/)")
    print_success(f"{len(selected_agents)} agent personas (.claude/agents/)")
    print_success(f"Shared scripts (.shipkit/scripts/)")
    print_success("Session hooks (.claude/hooks/)")
    print_success(f"Settings (.claude/settings.json)")
    print_success(f"Project instructions (CLAUDE.md)")
    print_success("Git configuration (.gitignore)")
    print_success("HTML skill reference (.shipkit/shipkit-overview.html)")

    print()
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}Next Steps{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()

    print(f"  {Colors.CYAN}1.{Colors.RESET} Start Claude Code in {Colors.CYAN}{target_dir}{Colors.RESET}")
    print()

    print(f"  {Colors.CYAN}2.{Colors.RESET} Quick start workflow:")
    print()
    print(f"     {Colors.GREEN}/shipkit-project-context{Colors.RESET} → {Colors.GREEN}/shipkit-spec{Colors.RESET}")
    print(f"     → {Colors.GREEN}/shipkit-plan{Colors.RESET} → implement")

    print()
    print(f"  {Colors.CYAN}3.{Colors.RESET} Type {Colors.GREEN}/shipkit-project-status{Colors.RESET} to see current state")
    print()
    print(f"  {Colors.DIM}Happy shipping! 🚀{Colors.RESET}")
    print()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main installation process"""
    parser = argparse.ArgumentParser(description="Shipkit Installer")
    parser.add_argument("--from-github", action="store_true",
                        help="Download and install from GitHub (no local repo needed)")
    parser.add_argument("--repo", default="stefan-stepzero/shipkit",
                        help="GitHub repo to install from (default: stefan-stepzero/shipkit)")
    parser.add_argument("--branch", default="main",
                        help="Git branch to install from (default: main)")
    parser.add_argument("--profile", choices=["shipkit", "minimal", "discovery"], default="shipkit",
                        help="Edition profile: shipkit (full), minimal (core only), discovery (planning focused)")
    parser.add_argument("--language", choices=["bash", "python"], help="Scripting language")
    parser.add_argument("--target", help="Target directory")
    parser.add_argument("--all-skills", action="store_true", help="Install all skills without prompting")
    parser.add_argument("--all-agents", action="store_true", help="Install all agents without prompting")
    parser.add_argument("--no-agents", action="store_true", help="Skip agent installation")
    parser.add_argument("--all-mcps", action="store_true", help="Install all MCP servers without prompting")
    parser.add_argument("--no-mcps", action="store_true", help="Skip MCP server installation")
    parser.add_argument("--claude-md", choices=["skip", "overwrite", "merge"], help="CLAUDE.md handling")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip all confirmations (non-interactive mode)")

    args = parser.parse_args()

    # Show logo early
    show_logo(args.profile or "shipkit")

    # Determine repo root (local or GitHub download)
    temp_dir_to_cleanup = None

    if args.from_github:
        # Download from GitHub
        repo_root = download_from_github(args.repo, args.branch)
        if repo_root is None:
            print_error("Could not download from GitHub. Aborting.")
            sys.exit(1)
        temp_dir_to_cleanup = repo_root.parent  # The temp directory containing the extracted repo
    else:
        # Use local repo
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent

    # Profile
    profile = args.profile or prompt_for_profile()

    # Language
    language = args.language or prompt_for_language()

    # Target directory
    if args.target:
        target_dir = Path(args.target).resolve()
    else:
        target_dir = prompt_for_target_directory()

    # Verify source files
    if not verify_source_files(repo_root):
        sys.exit(1)

    # Load manifest
    print_info(f"Loading manifest: {profile}.manifest.json")
    manifest = load_manifest(repo_root, profile)
    print_success(f"Manifest loaded: {manifest['description']}")
    print()

    # Skill selection
    if args.all_skills:
        # Get all skills
        selected_skills = list(manifest["skills"]["mandatory"])
        for category, skills in manifest["skills"]["optional"].items():
            for skill in skills:
                selected_skills.append(skill["name"])
    else:
        selected_skills = prompt_for_skills(manifest)

    # Agent selection
    if args.no_agents:
        selected_agents = []
    elif args.all_agents:
        selected_agents = [a["name"] for a in manifest.get("agents", [])]
    else:
        selected_agents = prompt_for_agents(manifest)

    # CLAUDE.md handling
    if args.claude_md:
        claude_md_action = args.claude_md
    else:
        claude_md_action = prompt_for_claude_md_action(target_dir)

    # Confirm installation
    if not args.yes:
        print()
        print(f"  {Colors.BOLD}Installation Summary:{Colors.RESET}")
        print()
        print(f"  Edition:   {Colors.CYAN}{profile}{Colors.RESET}")
        print(f"  Language:  {Colors.CYAN}{language}{Colors.RESET}")
        print(f"  Target:    {Colors.CYAN}{target_dir}{Colors.RESET}")
        print(f"  Skills:    {Colors.CYAN}{len(selected_skills)}{Colors.RESET}")
        print(f"  Agents:    {Colors.CYAN}{len(selected_agents)}{Colors.RESET}")
        print(f"  CLAUDE.md: {Colors.CYAN}{claude_md_action}{Colors.RESET}")
        print()

        if not confirm(f"Install Shipkit to {target_dir}?"):
            print_info("Installation cancelled.")
            sys.exit(0)

    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)

    # Perform installation
    print()
    print_info("Installing Shipkit framework...")

    install_shared_core(repo_root, target_dir, language, manifest["edition"])
    install_edition_files(repo_root, target_dir, manifest, language, selected_skills, claude_md_action, skip_prompts=args.yes)
    install_skills(repo_root, target_dir, selected_skills)
    install_agents(repo_root, target_dir, selected_agents)
    delete_unused_language(target_dir, language)
    make_scripts_executable(target_dir, language)

    # MCP selection (respect --no-mcps and --all-mcps flags)
    if args.no_mcps:
        selected_mcps = []
    elif args.all_mcps:
        selected_mcps = manifest.get("mcps", {}).get("recommended", [])
    elif args.yes:
        # Non-interactive mode: skip MCP selection (default to none)
        selected_mcps = []
        print_info("MCP selection skipped (non-interactive mode)")
    else:
        selected_mcps = prompt_for_mcps(manifest)
    install_mcp_config(target_dir, selected_mcps)

    # Show completion
    show_completion(target_dir, selected_skills, selected_agents, language)

    # Install and open docs
    open_html_docs(repo_root, target_dir, manifest["edition"])

    # Cleanup temp directory if we downloaded from GitHub
    if temp_dir_to_cleanup:
        try:
            shutil.rmtree(temp_dir_to_cleanup)
            print_info("Cleaned up temporary download files")
        except Exception:
            pass  # Best effort cleanup

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_warning("Installation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Installation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

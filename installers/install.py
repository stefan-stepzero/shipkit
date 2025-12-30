#!/usr/bin/env python3
"""
install.py - Shipkit Installer (Python)
Manifest-based installer supporting multiple editions and languages
"""

import os
import sys
import json
import shutil
import argparse
import platform
from pathlib import Path
import subprocess

# ═══════════════════════════════════════════════════════════════════════════════
# COLORS & STYLING
# ═══════════════════════════════════════════════════════════════════════════════

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

def print_success(msg):
    print(f"  {Colors.GREEN}✓{Colors.RESET} {msg}")

def print_info(msg):
    print(f"  {Colors.CYAN}→{Colors.RESET} {msg}")

def print_warning(msg):
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {msg}")

def print_error(msg):
    print(f"  {Colors.RED}✗{Colors.RESET} {msg}")

def print_bullet(msg):
    print(f"  {Colors.DIM}•{Colors.RESET} {msg}")

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

    if edition == "lite":
        print(f"{Colors.DIM}         Lightweight Product Development Framework{Colors.RESET}")
        print(f"{Colors.DIM}              7 Skills • 3 Agents • Fast Iteration{Colors.RESET}")
    else:
        print(f"{Colors.DIM}         Complete Product Development Framework{Colors.RESET}")
        print(f"{Colors.DIM}              24 Skills • 6 Agents • Constitution-Driven{Colors.RESET}")
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
    """Prompt user to select edition/profile"""
    print()
    print(f"  {Colors.BOLD}Select Edition:{Colors.RESET}")
    print()
    print(f"  {Colors.CYAN}[1]{Colors.RESET} Lite      - Fast, minimal (7 skills, POCs and side projects)")
    print(f"  {Colors.CYAN}[2]{Colors.RESET} Default   - Complete (24 skills, full product development)")
    print()

    while True:
        choice = input(f"  {Colors.BOLD}Select edition [1-2]:{Colors.RESET} ").strip()
        if choice == "1":
            return "lite"
        elif choice == "2":
            return "default"
        else:
            print_warning("Invalid choice. Please enter 1 or 2.")

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
        "install/workspace/skills",
        "install/settings",
        "install/claude-md",
        "install/profiles",
        "help"
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

    if edition == "lite":
        # Install lite-specific hooks
        shutil.copy2(hooks_src / "lite-session-start.py", hooks_dest / "session-start.py")
        shutil.copy2(hooks_src / "lite-suggest-next-skill.py", hooks_dest / "suggest-next-skill.py")
        print_success("Hooks installed (lite edition)")
    else:
        # Install full Shipkit hooks
        shutil.copy2(hooks_src / "session-start.py", hooks_dest / "session-start.py")
        shutil.copy2(hooks_src / "suggest-next-skill.py", hooks_dest / "suggest-next-skill.py")
        print_success("Hooks installed (full edition)")

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
    # Only install .gitignore (no longer need .gitattributes - hooks are Python now)
    filename = ".gitignore"
    src = shared_dir / filename
    dest = target_dir / filename
    if not dest.exists():  # Don't overwrite existing
        shutil.copy2(src, dest)
        print_success(f"{filename} installed")
    else:
        print_warning(f"{filename} already exists, skipping")

def install_edition_files(repo_root, target_dir, manifest, language):
    """Install edition-specific settings and CLAUDE.md"""
    print()
    print(f"  {Colors.BOLD}Installing edition-specific files{Colors.RESET}")
    print()

    # Settings
    settings_file = manifest["settingsFile"]
    settings_src = repo_root / "install" / "settings" / settings_file
    settings_dest = target_dir / ".claude" / "settings.json"
    settings_dest.parent.mkdir(parents=True, exist_ok=True)

    if not settings_dest.exists():
        shutil.copy2(settings_src, settings_dest)
        print_success(f"Settings installed: {settings_file}")
    else:
        print_warning("settings.json exists, preserving your custom config")

    # CLAUDE.md
    claude_md_file = manifest["claudeMdFile"]
    claude_md_src = repo_root / "install" / "claude-md" / claude_md_file
    claude_md_dest = target_dir / "CLAUDE.md"

    if not claude_md_dest.exists():
        shutil.copy2(claude_md_src, claude_md_dest)
        print_success(f"CLAUDE.md installed: {claude_md_file}")
    else:
        print_warning("CLAUDE.md exists, skipping")

    # Update settings.json with edition and language metadata
    if settings_dest.exists():
        try:
            with open(settings_dest, 'r') as f:
                settings = json.load(f)

            settings["shipkit"] = {
                "edition": manifest["edition"],
                "language": language
            }

            with open(settings_dest, 'w') as f:
                json.dump(settings, f, indent=2)

            print_success(f"Added shipkit metadata (edition: {manifest['edition']}, language: {language})")
        except Exception as e:
            print_warning(f"Could not update settings metadata: {e}")

def install_skills(repo_root, target_dir, manifest):
    """Install skill definitions and workspace implementations from manifest"""
    print()
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}Installing skills{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()

    skills_definitions = manifest["skills"]["definitions"]
    skills_workspace = manifest["skills"]["workspace"]

    # Install skill definitions (.claude/skills/)
    print_info(f"Installing {len(skills_definitions)} skill definitions...")
    for skill_name in skills_definitions:
        skill_src = repo_root / "install" / "skills" / skill_name
        skill_dest = target_dir / ".claude" / "skills" / skill_name

        if skill_src.exists():
            skill_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(skill_src, skill_dest, dirs_exist_ok=True)
        else:
            print_warning(f"Skill not found: {skill_name}")

    print_success(f"Installed {len(skills_definitions)} skill definitions")

    # Install workspace implementations (.shipkit/skills/)
    print_info(f"Installing {len(skills_workspace)} skill implementations...")
    for skill_name in skills_workspace:
        skill_src = repo_root / "install" / "workspace" / "skills" / skill_name
        skill_dest = target_dir / ".shipkit" / "skills" / skill_name

        if skill_src.exists():
            skill_dest.mkdir(parents=True, exist_ok=True)

            # Copy scripts, templates, references
            for subdir in ["scripts", "templates", "references"]:
                src_subdir = skill_src / subdir
                if src_subdir.exists():
                    dest_subdir = skill_dest / subdir
                    shutil.copytree(src_subdir, dest_subdir, dirs_exist_ok=True)

            # Create empty outputs
            (skill_dest / "outputs").mkdir(exist_ok=True)
        else:
            print_warning(f"Workspace for skill not found: {skill_name}")

    print_success(f"Installed {len(skills_workspace)} skill implementations")

def install_agents(repo_root, target_dir, manifest):
    """Install agent personas from manifest"""
    print()
    print(f"  {Colors.BOLD}Installing agent personas{Colors.RESET}")
    print()

    agents = manifest.get("agents", [])

    if not agents:
        print_info("No agents specified in manifest (lite edition)")
        return

    agents_dir = target_dir / ".claude" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for agent_name in agents:
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

    # Determine which extension to delete
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
        return  # Not needed on Windows

    print()
    print_info("Making scripts executable...")

    if language == "bash":
        # Make .sh files executable
        for script in target_dir.rglob("*.sh"):
            script.chmod(0o755)
        print_success("Bash scripts are now executable")
    else:
        # Make .py files executable
        for script in target_dir.rglob("*.py"):
            script.chmod(0o755)
        print_success("Python scripts are now executable")

# ═══════════════════════════════════════════════════════════════════════════════
# MCP CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

def install_mcp_config(repo_root, target_dir):
    """Install MCP server configuration (Context7)"""
    mcp_config_path = target_dir / ".mcp.json"
    template_path = repo_root / "install" / "templates" / ".mcp.json"

    # Check if .mcp.json already exists
    if mcp_config_path.exists():
        print_warning(f".mcp.json already exists at {target_dir}")
        print_info("Skipping MCP configuration (keeping existing)")
        return

    # Check if template exists
    if not template_path.exists():
        print_warning("MCP template not found - skipping Context7 setup")
        print_info(f"Expected: {template_path}")
        return

    try:
        # Copy template to target
        shutil.copy2(template_path, mcp_config_path)
        print_success("MCP configuration installed (.mcp.json)")
        print_info("Context7 server configured (use 'use context7' in prompts)")
    except Exception as e:
        print_error(f"Failed to install MCP config: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETION
# ═══════════════════════════════════════════════════════════════════════════════

def open_html_docs(repo_root, edition):
    """Open appropriate HTML overview based on edition"""
    import webbrowser
    import platform

    html_dir = repo_root / "help"

    if not html_dir.exists():
        print_warning(f"Documentation files not found in {html_dir}")
        return

    # Choose appropriate overview based on edition
    if edition == "lite":
        overview_file = html_dir / "shipkit-lite-overview.html"
    else:
        overview_file = html_dir / "system-overview.html"

    if not overview_file.exists():
        print_warning(f"Overview not found: {overview_file}")
        return

    print()
    print(f"  {Colors.BRIGHT_CYAN}📖 Opening documentation...{Colors.RESET}")
    print()

    try:
        webbrowser.open(f"file://{overview_file}")
        overview_name = overview_file.name
        print_success(f"Opened {overview_name}")
    except Exception as e:
        overview_name = overview_file.name
        print_warning(f"Could not open {overview_name}: {e}")

def show_completion(target_dir, manifest, language):
    """Show completion message"""
    edition = manifest["edition"]
    skill_count = len(manifest["skills"]["definitions"])
    agent_count = len(manifest.get("agents", []))

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
    print_success(f"{skill_count} skill definitions (.claude/skills/)")
    print_success(f"{skill_count} skill implementations (.shipkit/skills/)")
    print_success(f"{agent_count} agent personas (.claude/agents/)")
    print_success(f"Shared scripts (.shipkit/scripts/)")
    print_success("Session hooks (.claude/hooks/)")
    print_success(f"Settings ({edition} edition) (.claude/settings.json)")
    print_success(f"Project instructions ({edition}) (CLAUDE.md)")
    print_success("Git configuration (.gitignore)")
    print_success("MCP configuration - Context7 (.mcp.json)")

    print()
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}Next Steps{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()

    print(f"  {Colors.CYAN}1.{Colors.RESET} Start Claude Code in {Colors.CYAN}{target_dir}{Colors.RESET}")
    print()

    if edition == "lite":
        print(f"  {Colors.CYAN}2.{Colors.RESET} Quick start workflow:")
        print()
        print(f"     {Colors.GREEN}/lite-project-context{Colors.RESET} → {Colors.GREEN}/lite-spec{Colors.RESET}")
        print(f"     → {Colors.GREEN}/lite-plan{Colors.RESET} → {Colors.GREEN}/lite-implement{Colors.RESET}")
    else:
        print(f"  {Colors.CYAN}2.{Colors.RESET} Choose your workflow:")
        print()
        print(f"     {Colors.DIM}Full product development (Greenfield):{Colors.RESET}")
        print(f"     {Colors.GREEN}/prod-strategic-thinking{Colors.RESET} → {Colors.GREEN}/prod-constitution-builder{Colors.RESET}")
        print(f"     → {Colors.GREEN}/prod-personas{Colors.RESET} → {Colors.GREEN}/prod-user-stories{Colors.RESET}")
        print()
        print(f"     {Colors.DIM}Quick POC (Fast validation):{Colors.RESET}")
        print(f"     {Colors.GREEN}/prod-constitution-builder{Colors.RESET} {Colors.DIM}(choose POC){Colors.RESET} → {Colors.GREEN}/dev-specify{Colors.RESET}")

    print()
    if edition == "lite":
        print(f"  {Colors.CYAN}3.{Colors.RESET} Type {Colors.GREEN}/lite-project-status{Colors.RESET} to see current state")
    else:
        print(f"  {Colors.CYAN}3.{Colors.RESET} Type {Colors.GREEN}/shipkit-status{Colors.RESET} to see current state")
    print()
    print(f"  {Colors.DIM}Happy shipping! 🚀{Colors.RESET}")
    print()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main installation process"""
    parser = argparse.ArgumentParser(description="Shipkit Installer")
    parser.add_argument("--profile", choices=["lite", "default"], help="Edition profile (lite or default)")
    parser.add_argument("--language", choices=["bash", "python"], help="Scripting language (bash or python)")
    parser.add_argument("--target", help="Target directory (default: current directory)")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmations")

    args = parser.parse_args()

    # Determine profile and language (from args or interactive)
    if args.profile:
        profile = args.profile
    else:
        profile = prompt_for_profile()

    if args.language:
        language = args.language
    else:
        language = prompt_for_language()

    # Target directory (from args or interactive)
    if args.target:
        target_dir = Path(args.target).resolve()
    else:
        target_dir = prompt_for_target_directory()

    # Repo root (where this script lives)
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Show logo
    show_logo(profile)

    # Verify source files
    if not verify_source_files(repo_root):
        sys.exit(1)

    # Load manifest
    print_info(f"Loading manifest: {profile}.manifest.json")
    manifest = load_manifest(repo_root, profile)
    print_success(f"Manifest loaded: {manifest['description']}")
    print()

    # Confirm installation
    if not args.yes:
        print(f"  {Colors.BOLD}Installation Summary:{Colors.RESET}")
        print()
        print(f"  Edition:  {Colors.CYAN}{profile}{Colors.RESET}")
        print(f"  Language: {Colors.CYAN}{language}{Colors.RESET}")
        print(f"  Target:   {Colors.CYAN}{target_dir}{Colors.RESET}")
        print(f"  Skills:   {Colors.CYAN}{len(manifest['skills']['definitions'])}{Colors.RESET}")
        print(f"  Agents:   {Colors.CYAN}{len(manifest.get('agents', []))}{Colors.RESET}")
        print()

        if not confirm(f"Install Shipkit to {target_dir}?"):
            print_info("Installation cancelled.")
            sys.exit(0)

    # Create target directory if needed
    target_dir.mkdir(parents=True, exist_ok=True)

    # Perform installation
    print()
    print_info("Installing Shipkit framework...")

    install_shared_core(repo_root, target_dir, language, manifest["edition"])
    install_edition_files(repo_root, target_dir, manifest, language)
    install_skills(repo_root, target_dir, manifest)
    install_agents(repo_root, target_dir, manifest)
    delete_unused_language(target_dir, language)
    make_scripts_executable(target_dir, language)
    install_mcp_config(repo_root, target_dir)

    # Show completion
    show_completion(target_dir, manifest, language)

    # Open HTML documentation
    open_html_docs(repo_root, manifest["edition"])

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

#!/usr/bin/env python3
"""
install.py - Shipkit Installer (Python)
Cross-platform installer for the Shipkit framework
"""

import os
import sys
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
    GRAY = '\033[90m'

def print_success(msg):
    print(f"  {Colors.GREEN}[OK]{Colors.RESET} {msg}")

def print_info(msg):
    print(f"  {Colors.CYAN}[>]{Colors.RESET} {msg}")

def print_warning(msg):
    print(f"  {Colors.YELLOW}[!]{Colors.RESET} {msg}")

def print_error(msg):
    print(f"  {Colors.RED}[X]{Colors.RESET} {msg}")

def print_bullet(msg):
    print(f"  {Colors.DIM}*{Colors.RESET} {msg}")

# ═══════════════════════════════════════════════════════════════════════════════
# LOGO
# ═══════════════════════════════════════════════════════════════════════════════

def show_logo():
    print()
    print(f"{Colors.MAGENTA}", end='')
    # Using simple ASCII to avoid encoding issues on Windows
    print("""
    ========================================================================
                                                        /\\
       SHIPKIT - Product Development Framework          /  \\
                                                       / /| \\
       24 Skills • 6 Agents • Constitution-Driven     / / |  \\
                                                     /_/__|___\\
                                                     \\________/
                                                     ~~~~~~~~~~
    ========================================================================
    """)
    print(f"{Colors.RESET}")
    print(f"{Colors.DIM}         Complete Product Development Framework{Colors.RESET}")
    print(f"{Colors.DIM}              24 Skills • 6 Agents • Constitution-Driven{Colors.RESET}")
    print()

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def verify_source_files(repo_root):
    """Verify all required source files exist"""
    print(f"  {Colors.BOLD}Verifying source files...{Colors.RESET}")
    print()

    required_paths = [
        "install/skills",
        "install/agents",
        "install/workspace/skills",
        "install/workspace/scripts",
        "install/hooks",
        "install/settings.json",
        "install/CLAUDE.md",
        "install/.gitignore",
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
        print()
        return False

    return True

def check_project_root(target_dir):
    """Check if target is a git repository"""
    return (target_dir / ".git").exists()

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALLATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def install_skills(repo_root, target_dir):
    """Install skill definitions"""
    print()
    print(f"  {Colors.MAGENTA}{'='*60}{Colors.RESET}")
    print(f"  {Colors.BOLD}Installing skills{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{'='*60}{Colors.RESET}")
    print()

    skills_dir = target_dir / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    print_info("Installing skill definitions...")
    source_skills = repo_root / "install" / "skills"

    for skill_dir in source_skills.iterdir():
        if skill_dir.is_dir():
            shutil.copytree(skill_dir, skills_dir / skill_dir.name, dirs_exist_ok=True)

    skill_count = len(list(skills_dir.iterdir()))
    print_success(f"Installed {skill_count} skill definitions")
    print_bullet("12 product skills (prod-*)")
    print_bullet("9 development skills (dev-*)")
    print_bullet("3 meta skills (shipkit-master, dev-discussion, dev-writing-skills)")

def install_agents(repo_root, target_dir):
    """Install agent personas"""
    print()
    print(f"  {Colors.BOLD}Installing agent personas{Colors.RESET}")
    print()

    agents_dir = target_dir / ".claude" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    print_info(f"Creating .claude/agents directory...")

    count = 0
    source_agents = repo_root / "install" / "agents"
    print_info(f"Copying agent files from {source_agents}...")

    for agent_file in source_agents.glob("*.md"):
        # Skip README.md - it's documentation, not an agent definition
        if agent_file.name == "README.md":
            print_info("  Skipping README.md (documentation only)")
            continue
        dest_file = agents_dir / agent_file.name
        print_info(f"  Checking {agent_file.name}...")
        if not dest_file.exists():
            print_info(f"    Copying {agent_file.name}...")
            shutil.copy2(agent_file, dest_file)
            count += 1
        else:
            print_info(f"    Skipping {agent_file.name} (already exists)")

    print_success(f"Installed {count} agent personas")
    print_bullet("prod-product-manager, prod-product-designer")
    print_bullet("dev-architect, dev-implementer, dev-reviewer")
    print_bullet("any-researcher")

def install_hooks(repo_root, target_dir):
    """Install session hooks"""
    print()
    print(f"  {Colors.BOLD}Installing session hooks{Colors.RESET}")
    print()

    hooks_dir = target_dir / ".claude" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)

    print_info("Creating .claude/hooks directory...")

    source_hooks = repo_root / "install" / "hooks"
    print_info(f"Copying hook files from {source_hooks}...")

    for hook_file in source_hooks.iterdir():
        if hook_file.is_file():
            print_info(f"  Copying {hook_file.name}...")
            shutil.copy2(hook_file, hooks_dir / hook_file.name)

    print_success("Installed session hooks")
    print_bullet("SessionStart hook loads shipkit-master")

def install_settings(repo_root, target_dir):
    """Install settings.json"""
    print()
    print(f"  {Colors.BOLD}Installing settings.json{Colors.RESET}")
    print()

    settings_file = target_dir / ".claude" / "settings.json"

    print_info("Checking if settings.json already exists...")
    if not settings_file.exists():
        print_info("No existing settings.json found")
        source_settings = repo_root / "install" / "settings.json"
        if source_settings.exists():
            print_info(f"Copying settings.json from {source_settings}...")
            shutil.copy2(source_settings, settings_file)
            print_success("Installed settings.json")
            print_bullet("File protections: .claude/* and .shipkit/skills/*/outputs|templates|scripts")
            print_bullet("SessionStart hook configured")
            print_bullet("SkillComplete prompts enabled")
        else:
            print_error("Source settings.json not found!")
            return False
    else:
        print_warning("settings.json exists, preserving your custom config")
        print_info("Backup your settings before re-installing if needed")

    return True

def install_workspace(repo_root, target_dir):
    """Install workspace (.shipkit/)"""
    print()
    print(f"  {Colors.MAGENTA}{'='*60}{Colors.RESET}")
    print(f"  {Colors.BOLD}Setting up workspace{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{'='*60}{Colors.RESET}")
    print()

    print_info("Creating .shipkit/ workspace structure...")

    # Create base directories
    (target_dir / ".shipkit" / "scripts").mkdir(parents=True, exist_ok=True)
    (target_dir / ".shipkit" / "skills").mkdir(parents=True, exist_ok=True)
    print_success("Created .shipkit base directories")

    # Copy shared scripts
    source_scripts = repo_root / "install" / "workspace" / "scripts" / "bash"
    print_info(f"Copying shared scripts from {source_scripts}...")
    if source_scripts.exists():
        shutil.copytree(source_scripts, target_dir / ".shipkit" / "scripts" / "bash", dirs_exist_ok=True)
        print_success("Installed shared scripts (common.sh)")
    else:
        print_warning("Shared scripts directory not found, skipping")

    # Copy all skill implementations
    print_info("Installing skill implementations (scripts, templates, references)...")

    skill_impl_count = 0
    source_skills = repo_root / "install" / "workspace" / "skills"
    if source_skills.exists():
        for skill_dir in source_skills.iterdir():
            if skill_dir.is_dir():
                skill_name = skill_dir.name
                print_info(f"  Processing skill: {skill_name}...")

                dest_skill_dir = target_dir / ".shipkit" / "skills" / skill_name
                dest_skill_dir.mkdir(parents=True, exist_ok=True)

                # Copy scripts, templates, references
                for subdir in ["scripts", "templates", "references"]:
                    source_subdir = skill_dir / subdir
                    if source_subdir.exists():
                        print_info(f"    Copying {subdir}...")
                        shutil.copytree(source_subdir, dest_skill_dir / subdir, dirs_exist_ok=True)

                # Create empty outputs folder
                print_info("    Creating outputs directory...")
                (dest_skill_dir / "outputs").mkdir(exist_ok=True)

                skill_impl_count += 1
                print_info(f"    [OK] {skill_name} complete")
    else:
        print_error("Workspace skills directory not found!")
        return False

    print_success(f"Installed {skill_impl_count} skill implementations")
    print_bullet("Scripts: Automation for each skill")
    print_bullet("Templates: Single adaptive template per skill")
    print_bullet("References: Extended docs, examples, patterns")
    print_bullet("Outputs: Empty (populated when skills run)")

    print()
    print_success("Shipkit workspace ready")
    print_bullet("Unified .shipkit/ structure for all skills")

    return True

def install_claude_md(repo_root, target_dir):
    """Install CLAUDE.md"""
    print()
    print(f"  {Colors.BOLD}Installing CLAUDE.md{Colors.RESET}")
    print()

    claude_md = target_dir / "CLAUDE.md"

    print_info("Checking if CLAUDE.md already exists...")
    if not claude_md.exists():
        print_info("No existing CLAUDE.md found")
        source_claude_md = repo_root / "install" / "CLAUDE.md"
        if source_claude_md.exists():
            print_info(f"Copying CLAUDE.md from {source_claude_md}...")
            shutil.copy2(source_claude_md, claude_md)
            print_success("Installed CLAUDE.md (project instructions)")
            print_bullet("24 skill routing guide")
            print_bullet("Constitution-driven workflows")
            print_bullet("Product ->Development integration")
        else:
            print_error(f"Source CLAUDE.md not found at {source_claude_md}!")
            return False
    else:
        print_warning("CLAUDE.md exists, skipping")
        print_info("Delete existing CLAUDE.md if you want to reinstall")

    return True

def install_gitignore(repo_root, target_dir):
    """Install .gitignore"""
    print()
    print(f"  {Colors.BOLD}Installing .gitignore{Colors.RESET}")
    print()

    gitignore = target_dir / ".gitignore"

    print_info("Checking if .gitignore already exists...")
    if not gitignore.exists():
        print_info("No existing .gitignore found")
        source_gitignore = repo_root / "install" / ".gitignore"
        if source_gitignore.exists():
            print_info(f"Copying .gitignore from {source_gitignore}...")
            shutil.copy2(source_gitignore, gitignore)
            print_success("Installed .gitignore")
            print_bullet("Excludes .claude/, .shipkit/, CLAUDE.md")
            print_bullet("Excludes env files and common IDE folders")
        else:
            print_warning("Source .gitignore not found, skipping")
    else:
        print_warning(".gitignore exists, skipping automatic install")
        print_info("Add these entries to your .gitignore manually:")
        print_bullet(".claude/")
        print_bullet(".shipkit/")
        print_bullet("CLAUDE.md")

    return True

def open_html_docs(repo_root):
    """Open documentation in browser"""
    html_dir = repo_root / "help"

    print()
    print(f"  {Colors.CYAN}📖 Opening documentation...{Colors.RESET}")
    print()

    if not html_dir.exists():
        print_warning(f"Documentation files not found in {html_dir}")
        return

    system_overview = html_dir / "system-overview.html"
    skills_summary = html_dir / "skills-summary.html"

    # Open files based on platform
    if platform.system() == "Darwin":  # macOS
        if system_overview.exists():
            subprocess.run(["open", str(system_overview)], check=False)
            print_success("Opened system-overview.html")
        if skills_summary.exists():
            subprocess.run(["open", str(skills_summary)], check=False)
            print_success("Opened skills-summary.html")
    elif platform.system() == "Windows":
        if system_overview.exists():
            os.startfile(str(system_overview))
            print_success("Opened system-overview.html")
        if skills_summary.exists():
            os.startfile(str(skills_summary))
            print_success("Opened skills-summary.html")
    else:  # Linux
        try:
            if system_overview.exists():
                subprocess.run(["xdg-open", str(system_overview)], check=False)
                print_success("Opened system-overview.html")
            if skills_summary.exists():
                subprocess.run(["xdg-open", str(skills_summary)], check=False)
                print_success("Opened skills-summary.html")
        except FileNotFoundError:
            print_warning(f"xdg-open not found. View docs at: {html_dir}")

def show_completion(target_dir):
    """Show completion screen"""
    skill_count = len(list((target_dir / ".claude" / "skills").iterdir()))
    agent_count = len(list((target_dir / ".claude" / "agents").glob("*.md")))
    skill_impl_count = len(list((target_dir / ".shipkit" / "skills").iterdir()))

    print()
    print()
    print(f"{Colors.GREEN}")
    print("""
    ===============================================================

         [OK]  Installation Complete!

    ===============================================================
    """)
    print(f"{Colors.RESET}")

    print(f"  {Colors.BOLD}What was installed:{Colors.RESET}")
    print()
    print_success(f"{skill_count} skill definitions (.claude/skills/)")
    print_success(f"{skill_impl_count} skill implementations (.shipkit/skills/)")
    print_success(f"{agent_count} agent personas (.claude/agents/)")
    print_success("Shared scripts (.shipkit/scripts/bash/common.sh)")
    print_success("Session hooks (.claude/hooks/)")
    print_success("Settings with file protections (.claude/settings.json)")
    print_success("Project instructions (CLAUDE.md)")
    print_success("Git ignore file (.gitignore)")

    print()
    print(f"  {Colors.MAGENTA}{'='*60}{Colors.RESET}")
    print(f"  {Colors.BOLD}Next Steps{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{'='*60}{Colors.RESET}")
    print()

    print(f"  {Colors.CYAN}1.{Colors.RESET} Start Claude Code in {Colors.CYAN}{target_dir}{Colors.RESET}")
    print()
    print(f"  {Colors.CYAN}2.{Colors.RESET} Choose your workflow:")
    print()
    print(f"     {Colors.DIM}Full product development (Greenfield):{Colors.RESET}")
    print(f"     {Colors.GREEN}/prod-strategic-thinking{Colors.RESET} ->{Colors.GREEN}/prod-constitution-builder{Colors.RESET}")
    print(f"     ->{Colors.GREEN}/prod-personas{Colors.RESET} ->{Colors.GREEN}/prod-user-stories{Colors.RESET} ->{Colors.GREEN}/dev-specify{Colors.RESET}")
    print()
    print(f"     {Colors.DIM}Quick POC (Fast validation):{Colors.RESET}")
    print(f"     {Colors.GREEN}/prod-constitution-builder{Colors.RESET} {Colors.DIM}(choose POC){Colors.RESET} ->{Colors.GREEN}/dev-specify{Colors.RESET} ->{Colors.GREEN}/dev-implement{Colors.RESET}")
    print()
    print(f"     {Colors.DIM}Existing codebase (Add feature):{Colors.RESET}")
    print(f"     {Colors.GREEN}/dev-constitution{Colors.RESET} ->{Colors.GREEN}/dev-specify{Colors.RESET} ->{Colors.GREEN}/dev-implement{Colors.RESET}")
    print()
    print(f"  {Colors.CYAN}3.{Colors.RESET} Type {Colors.GREEN}/help{Colors.RESET} to see all 24 skills")
    print()
    print(f"  {Colors.CYAN}💡 Constitution-Driven Development:{Colors.RESET}")
    print(f"     Run {Colors.GREEN}/prod-constitution-builder{Colors.RESET} to choose project type:")
    print(f"     {Colors.DIM}• B2B/B2C Greenfield (comprehensive){Colors.RESET}")
    print(f"     {Colors.DIM}• Side Project MVP/POC (minimal){Colors.RESET}")
    print(f"     {Colors.DIM}• Experimental (learning-focused){Colors.RESET}")
    print(f"     {Colors.DIM}• Existing Project (document current state){Colors.RESET}")
    print()
    print(f"  {Colors.DIM}Happy shipping! 🚀{Colors.RESET}")
    print()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='Install Shipkit framework into a target directory',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode in current directory
  python install.py

  # Install to specific directory
  python install.py /path/to/project

  # Non-interactive installation
  python install.py /path/to/project -y
        """
    )

    parser.add_argument('target', nargs='?', help='Target directory (defaults to current directory)')
    parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmations')

    args = parser.parse_args()

    # Determine paths
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent

    if args.target:
        target_dir = Path(args.target).resolve()
    else:
        if args.yes:
            target_dir = Path.cwd()
        else:
            print()
            print(f"  {Colors.BOLD}Where would you like to install Shipkit?{Colors.RESET}")
            print(f"  {Colors.DIM}(Press Enter for current directory: {Path.cwd()}){Colors.RESET}")
            print()
            user_input = input(f"  {Colors.CYAN}Install path:{Colors.RESET} ").strip()
            target_dir = Path(user_input).resolve() if user_input else Path.cwd()

    # Show logo
    show_logo()

    # Detect and verify
    print(f"  {Colors.BOLD}Detecting installation context...{Colors.RESET}")
    print()
    print_info(f"Source: {Colors.CYAN}{repo_root}{Colors.RESET}")
    print_info(f"Target: {Colors.CYAN}{target_dir}{Colors.RESET}")
    print()

    if not verify_source_files(repo_root):
        sys.exit(1)

    # Check project root
    if not check_project_root(target_dir):
        print()
        print_warning("No .git directory found. This might not be a project root.")
        if not args.yes:
            response = input(f"  {Colors.BOLD}Continue anyway?{Colors.RESET} {Colors.DIM}[Y/n]{Colors.RESET} ").strip().lower()
            if response and not response.startswith('y'):
                print_info("Installation cancelled.")
                sys.exit(0)

    # Create target directory if needed
    if not target_dir.exists():
        if not args.yes:
            response = input(f"  {Colors.BOLD}Target directory {target_dir} doesn't exist. Create it?{Colors.RESET} {Colors.DIM}[Y/n]{Colors.RESET} ").strip().lower()
            if response and not response.startswith('y'):
                print_info("Installation cancelled.")
                sys.exit(0)
        target_dir.mkdir(parents=True)

    # Confirm installation
    if not args.yes:
        print()
        response = input(f"  {Colors.BOLD}Install Shipkit to {target_dir}?{Colors.RESET} {Colors.DIM}[Y/n]{Colors.RESET} ").strip().lower()
        if response and not response.startswith('y'):
            print_info("Installation cancelled.")
            sys.exit(0)

    # Perform installation
    print()
    print_info("Installing Shipkit framework...")

    install_skills(repo_root, target_dir)
    install_agents(repo_root, target_dir)
    install_hooks(repo_root, target_dir)
    if not install_settings(repo_root, target_dir):
        sys.exit(1)
    if not install_workspace(repo_root, target_dir):
        sys.exit(1)
    if not install_claude_md(repo_root, target_dir):
        sys.exit(1)
    if not install_gitignore(repo_root, target_dir):
        sys.exit(1)

    # Show completion
    show_completion(target_dir)

    # Open documentation
    open_html_docs(repo_root)

if __name__ == '__main__':
    main()

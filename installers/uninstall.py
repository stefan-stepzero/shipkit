#!/usr/bin/env python3
"""
uninstall.py - Shipkit Uninstaller
Cleanly removes Shipkit from a project while preserving user data.
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path

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

def print_success(msg):
    print(f"  {Colors.GREEN}✓{Colors.RESET} {msg}")

def print_info(msg):
    print(f"  {Colors.CYAN}→{Colors.RESET} {msg}")

def print_warning(msg):
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {msg}")

def print_error(msg):
    print(f"  {Colors.RED}✗{Colors.RESET} {msg}")

# ═══════════════════════════════════════════════════════════════════════════════
# UNINSTALL FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def detect_shipkit(target_dir):
    """Detect if Shipkit is installed in target directory"""
    indicators = {
        "skills": target_dir / ".claude" / "skills",
        "agents": target_dir / ".claude" / "agents",
        "hooks": target_dir / ".claude" / "hooks",
        "settings": target_dir / ".claude" / "settings.json",
        "workspace": target_dir / ".shipkit",
        "claude_md": target_dir / "CLAUDE.md",
    }

    found = {k: v.exists() for k, v in indicators.items()}
    return found, any(found.values())

def show_what_will_be_removed(target_dir, found, keep_context):
    """Show what will be removed"""
    print()
    print(f"  {Colors.BOLD}Will be removed:{Colors.RESET}")
    print()

    if found["skills"]:
        print_info(".claude/skills/ (skill definitions)")
    if found["agents"]:
        print_info(".claude/agents/ (agent personas)")
    if found["hooks"]:
        print_info(".claude/hooks/ (session hooks)")
    if found["settings"]:
        print_info(".claude/settings.json (permissions & config)")

    if not keep_context and found["workspace"]:
        print_info(".shipkit/ (workspace and context)")

    print()
    print(f"  {Colors.BOLD}Will be preserved:{Colors.RESET}")
    print()

    if keep_context and found["workspace"]:
        print_success(".shipkit/ (your context files)")

    if found["claude_md"]:
        print_success("CLAUDE.md (your project instructions)")

    print_success("All your source code and other files")

def remove_directory(path, description):
    """Safely remove a directory"""
    if path.exists():
        try:
            shutil.rmtree(path)
            print_success(f"Removed {description}")
            return True
        except Exception as e:
            print_error(f"Failed to remove {description}: {e}")
            return False
    return True

def remove_file(path, description):
    """Safely remove a file"""
    if path.exists():
        try:
            path.unlink()
            print_success(f"Removed {description}")
            return True
        except Exception as e:
            print_error(f"Failed to remove {description}: {e}")
            return False
    return True

def clean_empty_directories(target_dir):
    """Remove empty .claude directory if nothing left"""
    claude_dir = target_dir / ".claude"

    if claude_dir.exists():
        # Check if directory is empty or only has empty subdirs
        remaining = list(claude_dir.rglob("*"))
        if not remaining or all(p.is_dir() for p in remaining):
            try:
                shutil.rmtree(claude_dir)
                print_success("Removed empty .claude/ directory")
            except:
                pass

def uninstall(target_dir, keep_context=True, keep_claude_md=True, force=False):
    """Perform uninstallation"""
    print()
    print(f"  {Colors.BOLD}Uninstalling Shipkit...{Colors.RESET}")
    print()

    success = True

    # Remove .claude/skills/
    skills_dir = target_dir / ".claude" / "skills"
    if skills_dir.exists():
        # Only remove shipkit-* skills
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and skill_dir.name.startswith("shipkit-"):
                success &= remove_directory(skill_dir, f"skill: {skill_dir.name}")

        # Remove skills dir if empty
        if skills_dir.exists() and not any(skills_dir.iterdir()):
            skills_dir.rmdir()
            print_success("Removed empty skills/ directory")

    # Remove .claude/agents/
    agents_dir = target_dir / ".claude" / "agents"
    if agents_dir.exists():
        # Only remove shipkit-* agents
        for agent_file in agents_dir.iterdir():
            if agent_file.is_file() and agent_file.name.startswith("shipkit-"):
                success &= remove_file(agent_file, f"agent: {agent_file.name}")

        # Remove agents dir if empty
        if agents_dir.exists() and not any(agents_dir.iterdir()):
            agents_dir.rmdir()
            print_success("Removed empty agents/ directory")

    # Remove .claude/hooks/
    hooks_dir = target_dir / ".claude" / "hooks"
    success &= remove_directory(hooks_dir, ".claude/hooks/")

    # Remove or clean settings.json
    settings_path = target_dir / ".claude" / "settings.json"
    if settings_path.exists():
        if force:
            success &= remove_file(settings_path, ".claude/settings.json")
        else:
            # Try to remove only Shipkit-specific settings
            try:
                with open(settings_path, 'r') as f:
                    settings = json.load(f)

                # Remove shipkit-specific entries
                if "shipkit" in settings:
                    del settings["shipkit"]

                # Remove Skill() permissions
                if "permissions" in settings and "allow" in settings["permissions"]:
                    settings["permissions"]["allow"] = [
                        p for p in settings["permissions"]["allow"]
                        if not p.startswith("Skill(shipkit-")
                    ]

                # Remove hooks
                if "hooks" in settings:
                    del settings["hooks"]

                with open(settings_path, 'w') as f:
                    json.dump(settings, f, indent=2)

                print_success("Cleaned Shipkit entries from settings.json")
            except Exception as e:
                print_warning(f"Could not clean settings.json: {e}")

    # Remove .shipkit/ workspace (optional)
    if not keep_context:
        workspace_dir = target_dir / ".shipkit"
        success &= remove_directory(workspace_dir, ".shipkit/ workspace")
    else:
        print_info("Preserved .shipkit/ (use --remove-context to delete)")

    # Remove CLAUDE.md (optional)
    if not keep_claude_md:
        claude_md = target_dir / "CLAUDE.md"
        success &= remove_file(claude_md, "CLAUDE.md")
    else:
        print_info("Preserved CLAUDE.md (use --remove-claude-md to delete)")

    # Remove .mcp.json if it exists and only has Shipkit MCPs
    mcp_path = target_dir / ".mcp.json"
    if mcp_path.exists():
        print_info("Preserved .mcp.json (remove manually if not needed)")

    # Clean up empty directories
    clean_empty_directories(target_dir)

    return success

def confirm(prompt, default=False):
    """Ask yes/no confirmation"""
    hint = "[y/N]" if not default else "[Y/n]"
    response = input(f"  {Colors.BOLD}{prompt}{Colors.RESET} {Colors.DIM}{hint}{Colors.RESET} ").strip().lower()

    if not response:
        return default

    return response in ['y', 'yes']

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Uninstall Shipkit from a project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python uninstall.py                    # Uninstall from current directory
  python uninstall.py --target /my/proj  # Uninstall from specific directory
  python uninstall.py --remove-context   # Also remove .shipkit/ workspace
  python uninstall.py -y                 # Skip confirmation
        """
    )
    parser.add_argument("--target", help="Target directory (default: current)")
    parser.add_argument("--remove-context", action="store_true",
                        help="Also remove .shipkit/ workspace (your context files)")
    parser.add_argument("--remove-claude-md", action="store_true",
                        help="Also remove CLAUDE.md")
    parser.add_argument("--force", action="store_true",
                        help="Force removal of all .claude/ contents")
    parser.add_argument("-y", "--yes", action="store_true",
                        help="Skip confirmation prompts")

    args = parser.parse_args()

    # Target directory
    target_dir = Path(args.target).resolve() if args.target else Path.cwd()

    print()
    print(f"  {Colors.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}Shipkit Uninstaller{Colors.RESET}")
    print(f"  {Colors.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()
    print(f"  Target: {Colors.CYAN}{target_dir}{Colors.RESET}")

    # Detect Shipkit
    found, is_installed = detect_shipkit(target_dir)

    if not is_installed:
        print()
        print_warning("Shipkit does not appear to be installed in this directory.")
        print()
        sys.exit(0)

    # Show what will be removed
    keep_context = not args.remove_context
    keep_claude_md = not args.remove_claude_md
    show_what_will_be_removed(target_dir, found, keep_context)

    # Confirm
    if not args.yes:
        print()
        if not confirm("Proceed with uninstallation?"):
            print_info("Uninstallation cancelled.")
            sys.exit(0)

    # Uninstall
    success = uninstall(
        target_dir,
        keep_context=keep_context,
        keep_claude_md=keep_claude_md,
        force=args.force
    )

    # Completion
    print()
    if success:
        print(f"  {Colors.GREEN}✓ Shipkit uninstalled successfully{Colors.RESET}")
        print()
        if keep_context:
            print(f"  {Colors.DIM}Your context files in .shipkit/ were preserved.{Colors.RESET}")
            print(f"  {Colors.DIM}To reinstall: python path/to/sg-shipkit/installers/install.py{Colors.RESET}")
    else:
        print(f"  {Colors.YELLOW}⚠ Uninstallation completed with some errors{Colors.RESET}")

    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_warning("Uninstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Uninstallation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

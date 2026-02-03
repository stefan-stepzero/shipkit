#!/usr/bin/env python3
"""
list-skills.py - List installed Shipkit skills
Shows all installed skills with their descriptions and status.
"""

import os
import sys
import json
from pathlib import Path

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
    MAGENTA = '\033[1;35m'

# ═══════════════════════════════════════════════════════════════════════════════
# SKILL DISCOVERY
# ═══════════════════════════════════════════════════════════════════════════════

def find_project_root():
    """Find project root by looking for .claude directory"""
    current = Path.cwd()

    while current != current.parent:
        if (current / ".claude").exists():
            return current
        current = current.parent

    # Fall back to current directory
    return Path.cwd()

def parse_skill_frontmatter(skill_path):
    """Parse YAML frontmatter from SKILL.md"""
    skill_file = skill_path / "SKILL.md"

    if not skill_file.exists():
        return None

    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for YAML frontmatter
        if not content.startswith('---'):
            return {"name": skill_path.name, "description": "No description"}

        # Find end of frontmatter
        end_idx = content.find('---', 3)
        if end_idx == -1:
            return {"name": skill_path.name, "description": "No description"}

        frontmatter = content[3:end_idx].strip()

        # Simple YAML parsing
        result = {"name": skill_path.name}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                result[key] = value

        return result

    except Exception as e:
        return {"name": skill_path.name, "description": f"Error reading: {e}"}

def get_installed_skills(project_root):
    """Get list of installed skills"""
    skills_dir = project_root / ".claude" / "skills"

    if not skills_dir.exists():
        return []

    skills = []
    for skill_path in sorted(skills_dir.iterdir()):
        if skill_path.is_dir() and skill_path.name.startswith("shipkit-"):
            info = parse_skill_frontmatter(skill_path)
            if info:
                skills.append(info)

    return skills

def get_settings_info(project_root):
    """Get skill info from settings.json"""
    settings_path = project_root / ".claude" / "settings.json"

    if not settings_path.exists():
        return {}

    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)

        return settings.get("shipkit", {})
    except:
        return {}

# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

def categorize_skills(skills):
    """Categorize skills by type"""
    categories = {
        "Core Workflow": [],
        "Discovery & Planning": [],
        "Implementation": [],
        "Quality & Documentation": [],
        "Ecosystem": [],
        "System": [],
        "Other": []
    }

    category_keywords = {
        "Core Workflow": ["master", "project-status", "project-context", "codebase-index", "claude-md"],
        "Discovery & Planning": ["why-project", "product-discovery", "spec", "plan", "prototyping", "prototype-to-spec"],
        "Implementation": ["architecture-memory", "data-contracts", "integration-docs"],
        "Quality & Documentation": ["verify", "preflight", "ux-audit", "user-instructions", "communications", "work-memory"],
        "Ecosystem": ["get-skills", "get-mcps"],
        "System": ["detect"]
    }

    for skill in skills:
        name = skill.get("name", "").replace("shipkit-", "")
        categorized = False

        for category, keywords in category_keywords.items():
            if any(kw in name for kw in keywords):
                categories[category].append(skill)
                categorized = True
                break

        if not categorized:
            categories["Other"].append(skill)

    return categories

def print_skills(skills, settings_info):
    """Print skills in formatted output"""
    print()
    print(f"  {Colors.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}Installed Shipkit Skills{Colors.RESET}")
    print(f"  {Colors.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print()

    if not skills:
        print(f"  {Colors.YELLOW}No Shipkit skills installed.{Colors.RESET}")
        print()
        print(f"  {Colors.DIM}Install with: python path/to/sg-shipkit/installers/install.py{Colors.RESET}")
        print()
        return

    # Show edition info
    edition = settings_info.get("edition", "unknown")
    language = settings_info.get("language", "unknown")
    print(f"  {Colors.DIM}Edition: {edition} | Language: {language}{Colors.RESET}")
    print()

    # Categorize and display
    categories = categorize_skills(skills)

    for category, cat_skills in categories.items():
        if not cat_skills:
            continue

        print(f"  {Colors.BOLD}{category} ({len(cat_skills)}){Colors.RESET}")
        print()

        for skill in cat_skills:
            name = skill.get("name", "unknown")
            desc = skill.get("description", "No description")

            # Truncate description if too long
            if len(desc) > 60:
                desc = desc[:57] + "..."

            print(f"    {Colors.GREEN}/{name}{Colors.RESET}")
            print(f"    {Colors.DIM}{desc}{Colors.RESET}")
            print()

    # Summary
    print(f"  {Colors.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.BOLD}Total: {len(skills)} skills installed{Colors.RESET}")
    print()

def print_compact(skills):
    """Print skills in compact format"""
    print()
    for skill in skills:
        name = skill.get("name", "unknown")
        print(f"/{name}")
    print()
    print(f"Total: {len(skills)} skills")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(description="List installed Shipkit skills")
    parser.add_argument("--compact", "-c", action="store_true",
                        help="Compact output (names only)")
    parser.add_argument("--json", "-j", action="store_true",
                        help="JSON output")

    args = parser.parse_args()

    # Find project root
    project_root = find_project_root()

    # Get installed skills
    skills = get_installed_skills(project_root)
    settings_info = get_settings_info(project_root)

    # Output
    if args.json:
        print(json.dumps({"skills": skills, "settings": settings_info}, indent=2))
    elif args.compact:
        print_compact(skills)
    else:
        print_skills(skills, settings_info)

if __name__ == "__main__":
    main()

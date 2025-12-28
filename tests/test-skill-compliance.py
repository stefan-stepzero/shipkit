#!/usr/bin/env python3
"""
Skill Compliance Tests

Validates that lite skills follow the patterns in LITE-SKILLS-GUIDE.md:
1. File structure (no references/ folder, examples.md at root)
2. SKILL.md structure (< 300 lines target, required sections)
3. Both bash and python scripts exist
4. Templates are simple (1-page)
5. Examples.md has 2-3 examples
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(msg: str):
    print(f"  {Colors.BLUE}→{Colors.RESET} {msg}")

def print_pass(msg: str):
    print(f"  {Colors.GREEN}✓{Colors.RESET} {msg}")

def print_fail(msg: str):
    print(f"  {Colors.RED}✗{Colors.RESET} {msg}")

def print_warn(msg: str):
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {msg}")

def print_section(msg: str):
    print(f"\n{Colors.BOLD}{msg}{Colors.RESET}")

# Get repo root
REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "install" / "skills"
WORKSPACE_DIR = REPO_ROOT / "install" / "workspace" / "skills"

# Track results
passed = 0
failed = 0
warnings = 0

def test_file_structure(skill_name: str) -> bool:
    """Test that lite skill follows correct file structure"""
    global passed, failed, warnings

    print_test(f"Checking file structure for {skill_name}")

    workspace = WORKSPACE_DIR / skill_name

    # Should have examples.md at root
    examples_root = workspace / "examples.md"
    if not examples_root.exists():
        print_fail(f"Missing examples.md at root")
        failed += 1
        return False
    else:
        print_pass("examples.md at root")
        passed += 1

    # Should NOT have references/ folder
    references = workspace / "references"
    if references.exists():
        print_warn(f"Has references/ folder (lite should use root examples.md)")
        warnings += 1

    return True

def test_skill_md_length(skill_name: str) -> bool:
    """Test that SKILL.md is within recommended length"""
    global passed, failed, warnings

    skill_md = SKILLS_DIR / skill_name / "SKILL.md"

    with open(skill_md) as f:
        lines = f.readlines()

    line_count = len(lines)

    print_test(f"Checking SKILL.md length ({line_count} lines)")

    if line_count <= 300:
        print_pass(f"Within lite target (≤300 lines)")
        passed += 1
        return True
    elif line_count <= 500:
        print_warn(f"Above lite target but acceptable (≤500 lines)")
        warnings += 1
        return True
    else:
        print_fail(f"Too long for lite skill (>{500} lines)")
        failed += 1
        return False

def test_skill_md_sections(skill_name: str) -> bool:
    """Test that SKILL.md has required sections for lite"""
    global passed, failed, warnings

    skill_md = SKILLS_DIR / skill_name / "SKILL.md"

    with open(skill_md) as f:
        content = f.read()

    required_sections = [
        "What's Different from Full Version",
        "When to Use This Skill",
        "Quick Start",
        "Output Location",
        "Examples",
        "Next Steps"
    ]

    missing_sections = []
    for section in required_sections:
        if f"## {section}" not in content and f"### {section}" not in content:
            missing_sections.append(section)

    if missing_sections:
        print_fail(f"Missing sections: {', '.join(missing_sections)}")
        failed += 1
        return False
    else:
        print_pass("All required sections present")
        passed += 1
        return True

def test_scripts_exist(skill_name: str) -> bool:
    """Test that both bash and python scripts exist (if applicable)"""
    global passed, failed, warnings

    # dev-implement-lite has no scripts (it's guidance only)
    if skill_name == "dev-implement-lite":
        return True

    workspace = WORKSPACE_DIR / skill_name
    scripts_dir = workspace / "scripts"

    if not scripts_dir.exists():
        print_warn(f"No scripts directory")
        warnings += 1
        return True

    print_test(f"Checking for bash and python scripts")

    scripts = list(scripts_dir.iterdir())
    sh_scripts = [s for s in scripts if s.suffix == ".sh"]
    py_scripts = [s for s in scripts if s.suffix == ".py"]

    has_bash = len(sh_scripts) > 0
    has_python = len(py_scripts) > 0

    if has_bash and has_python:
        print_pass(f"Has both bash ({len(sh_scripts)}) and python ({len(py_scripts)}) scripts")
        passed += 1
        return True
    elif has_bash:
        print_warn(f"Has bash scripts but missing python")
        warnings += 1
        return False
    elif has_python:
        print_warn(f"Has python scripts but missing bash")
        warnings += 1
        return False
    else:
        print_fail(f"No scripts found")
        failed += 1
        return False

def test_template_simplicity(skill_name: str) -> bool:
    """Test that templates are simple (rough check for 1-page)"""
    global passed, failed, warnings

    # Not all skills have templates
    workspace = WORKSPACE_DIR / skill_name
    templates_dir = workspace / "templates"

    if not templates_dir.exists():
        return True

    print_test(f"Checking template simplicity")

    templates = list(templates_dir.glob("*.md"))

    if not templates:
        print_warn("templates/ directory exists but is empty")
        warnings += 1
        return True

    for template in templates:
        with open(template) as f:
            lines = f.readlines()

        # Rough heuristic: 1-page template should be < 150 lines
        if len(lines) > 150:
            print_warn(f"{template.name} is long ({len(lines)} lines) - should be 1-page for lite")
            warnings += 1
        else:
            passed += 1

    return True

def test_examples_count(skill_name: str) -> bool:
    """Test that examples.md has 2-3 examples"""
    global passed, failed, warnings

    workspace = WORKSPACE_DIR / skill_name
    examples = workspace / "examples.md"

    if not examples.exists():
        print_fail("examples.md missing")
        failed += 1
        return False

    print_test("Checking examples.md has 2-3 examples")

    with open(examples) as f:
        content = f.read()

    # Count "## Example" headings
    example_count = content.count("## Example")

    if 2 <= example_count <= 3:
        print_pass(f"Has {example_count} examples (recommended 2-3)")
        passed += 1
        return True
    elif example_count < 2:
        print_warn(f"Only {example_count} example(s) (recommended 2-3)")
        warnings += 1
        return True
    else:
        print_warn(f"Has {example_count} examples (recommended 2-3, may be too many)")
        warnings += 1
        return True

def test_examples_length(skill_name: str) -> bool:
    """Test that examples.md is within recommended length"""
    global passed, failed, warnings

    workspace = WORKSPACE_DIR / skill_name
    examples = workspace / "examples.md"

    with open(examples) as f:
        lines = f.readlines()

    line_count = len(lines)

    print_test(f"Checking examples.md length ({line_count} lines)")

    # Lite examples should be < 150 lines total (much shorter than full version)
    if line_count <= 150:
        print_pass("Within lite target (≤150 lines)")
        passed += 1
        return True
    elif line_count <= 300:
        print_warn("Longer than lite target but acceptable (≤300 lines)")
        warnings += 1
        return True
    else:
        print_fail("Too long for lite skill (>300 lines)")
        failed += 1
        return False

def test_next_skill_suggestion(skill_name: str) -> bool:
    """Test that SKILL.md suggests next skill"""
    global passed, failed, warnings

    skill_md = SKILLS_DIR / skill_name / "SKILL.md"

    with open(skill_md) as f:
        content = f.read()

    print_test("Checking for next skill suggestion")

    # Look for common patterns
    has_suggested = "**Suggested next skill:**" in content
    has_next_steps = "## Next Steps" in content
    has_ready = "**Ready to" in content

    if has_suggested or (has_next_steps and has_ready):
        print_pass("Suggests next skill")
        passed += 1
        return True
    else:
        print_warn("Missing clear next skill suggestion")
        warnings += 1
        return True

def test_skill(skill_name: str):
    """Run all tests for a single skill"""
    print_section(f"Testing {skill_name}")

    test_file_structure(skill_name)
    test_skill_md_length(skill_name)
    test_skill_md_sections(skill_name)
    test_scripts_exist(skill_name)
    test_template_simplicity(skill_name)
    test_examples_count(skill_name)
    test_examples_length(skill_name)
    test_next_skill_suggestion(skill_name)

def main():
    global passed, failed, warnings

    print(f"\n{Colors.BOLD}Skill Compliance Tests (Lite Edition){Colors.RESET}")
    print(f"Repo: {REPO_ROOT}\n")

    # Lite skills to test
    lite_skills = [
        "prod-strategic-thinking-lite",
        "prod-personas-lite",
        "prod-user-stories-lite",
        "dev-specify-lite",
        "dev-plan-lite",
        "dev-tasks-lite",
        "dev-implement-lite"
    ]

    for skill in lite_skills:
        test_skill(skill)

    # Summary
    print_section("Compliance Summary")
    print(f"  {Colors.GREEN}✓{Colors.RESET} Passed:  {passed}")
    print(f"  {Colors.RED}✗{Colors.RESET} Failed:  {failed}")
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} Warnings: {warnings}")

    total = passed + failed
    if total > 0:
        pass_rate = (passed / total) * 100
        print(f"\n  Compliance Rate: {pass_rate:.1f}%")

    # Exit code
    if failed > 0:
        print(f"\n{Colors.RED}Compliance checks FAILED{Colors.RESET}")
        sys.exit(1)
    elif warnings > 0:
        print(f"\n{Colors.YELLOW}Compliance checks PASSED with warnings{Colors.RESET}")
        sys.exit(0)
    else:
        print(f"\n{Colors.GREEN}All compliance checks PASSED{Colors.RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()

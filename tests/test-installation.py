#!/usr/bin/env python3
"""
Shipkit Installation Tests

Validates that:
1. Manifest files are valid and complete
2. All referenced skills exist
3. File structures are correct
4. Installation can run successfully
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Colors for output
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
INSTALL_DIR = REPO_ROOT / "install"
PROFILES_DIR = INSTALL_DIR / "profiles"
SKILLS_DIR = INSTALL_DIR / "skills"
WORKSPACE_DIR = INSTALL_DIR / "workspace" / "skills"

# Track test results
passed_tests = 0
failed_tests = 0
warnings = 0

def test_manifest_exists(profile: str) -> bool:
    """Test that manifest file exists and is valid JSON"""
    global passed_tests, failed_tests

    print_test(f"Checking {profile}.manifest.json exists")
    manifest_path = PROFILES_DIR / f"{profile}.manifest.json"

    if not manifest_path.exists():
        print_fail(f"Manifest not found: {manifest_path}")
        failed_tests += 1
        return False

    try:
        with open(manifest_path) as f:
            manifest = json.load(f)
        print_pass(f"Manifest is valid JSON")
        passed_tests += 1
        return True
    except json.JSONDecodeError as e:
        print_fail(f"Invalid JSON: {e}")
        failed_tests += 1
        return False

def test_manifest_structure(profile: str) -> Tuple[bool, Dict]:
    """Test that manifest has required fields"""
    global passed_tests, failed_tests

    manifest_path = PROFILES_DIR / f"{profile}.manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)

    required_fields = ["edition", "description", "settingsFile", "claudeMdFile", "skills", "agents"]
    missing = [f for f in required_fields if f not in manifest]

    if missing:
        print_fail(f"Missing fields: {', '.join(missing)}")
        failed_tests += 1
        return False, manifest

    print_pass("All required fields present")
    passed_tests += 1

    # Check skills structure
    if "definitions" not in manifest["skills"] or "workspace" not in manifest["skills"]:
        print_fail("Skills must have 'definitions' and 'workspace' arrays")
        failed_tests += 1
        return False, manifest

    print_pass("Skills structure is valid")
    passed_tests += 1

    return True, manifest

def test_skill_files_exist(profile: str, manifest: Dict) -> bool:
    """Test that all skills referenced in manifest actually exist"""
    global passed_tests, failed_tests, warnings

    all_exist = True

    # Check skill definitions
    print_test("Checking skill definitions exist")
    for skill_name in manifest["skills"]["definitions"]:
        skill_path = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_path.exists():
            print_fail(f"Skill definition missing: {skill_name}/SKILL.md")
            failed_tests += 1
            all_exist = False
        else:
            passed_tests += 1

    if all_exist:
        print_pass(f"All {len(manifest['skills']['definitions'])} skill definitions exist")

    # Check workspace implementations
    all_workspace_exist = True
    print_test("Checking workspace implementations exist")
    for skill_name in manifest["skills"]["workspace"]:
        # shipkit-master has no workspace implementation (it's just a definition)
        if skill_name == "shipkit-master":
            continue

        skill_path = WORKSPACE_DIR / skill_name
        if not skill_path.exists():
            print_fail(f"Workspace implementation missing: {skill_name}/")
            failed_tests += 1
            all_workspace_exist = False
        else:
            passed_tests += 1

    if all_workspace_exist:
        workspace_count = len([s for s in manifest["skills"]["workspace"] if s != "shipkit-master"])
        print_pass(f"All {workspace_count} workspace implementations exist")

    return all_exist and all_workspace_exist

def test_skill_structure(skill_name: str) -> bool:
    """Test that a skill has proper structure"""
    global passed_tests, failed_tests, warnings

    print_test(f"Validating {skill_name} structure")

    # Check SKILL.md exists
    skill_md = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_md.exists():
        print_fail(f"SKILL.md missing")
        failed_tests += 1
        return False

    # Read SKILL.md and check for YAML frontmatter
    with open(skill_md) as f:
        content = f.read()

    if not content.startswith("---\n"):
        print_fail(f"SKILL.md missing YAML frontmatter")
        failed_tests += 1
        return False

    # Extract frontmatter
    try:
        frontmatter_end = content.index("\n---\n", 4)
        frontmatter = content[4:frontmatter_end]

        # Check for required fields
        if "name:" not in frontmatter:
            print_fail("YAML frontmatter missing 'name' field")
            failed_tests += 1
            return False

        if "description:" not in frontmatter:
            print_fail("YAML frontmatter missing 'description' field")
            failed_tests += 1
            return False

        print_pass("SKILL.md has valid frontmatter")
        passed_tests += 1

    except ValueError:
        print_fail("SKILL.md has malformed YAML frontmatter")
        failed_tests += 1
        return False

    return True

def test_lite_skill_structure(skill_name: str) -> bool:
    """Test that a lite skill follows lite conventions"""
    global passed_tests, failed_tests, warnings

    workspace_path = WORKSPACE_DIR / skill_name

    # Lite skills should have examples.md at root (not references/)
    examples_root = workspace_path / "examples.md"
    examples_refs = workspace_path / "references" / "examples.md"

    if examples_refs.exists() and not examples_root.exists():
        print_warn(f"{skill_name}: examples.md should be at root, not in references/")
        warnings += 1
        return False

    if examples_root.exists():
        print_pass(f"{skill_name}: examples.md at root (correct for lite)")
        passed_tests += 1

    # Check for references/ folder (lite skills shouldn't have it)
    references_dir = workspace_path / "references"
    if references_dir.exists() and skill_name.endswith("-lite"):
        # Check if it only contains examples.md (which should be moved)
        refs_contents = list(references_dir.iterdir())
        if refs_contents:
            print_warn(f"{skill_name}: Has references/ folder (lite skills should use root examples.md)")
            warnings += 1

    return True

def test_workspace_structure(skill_name: str) -> bool:
    """Test that workspace implementation has expected structure"""
    global passed_tests, failed_tests, warnings

    # shipkit-master has no workspace
    if skill_name == "shipkit-master":
        return True

    workspace_path = WORKSPACE_DIR / skill_name

    if not workspace_path.exists():
        print_fail(f"Workspace missing: {skill_name}")
        failed_tests += 1
        return False

    # Check for common directories
    has_scripts = (workspace_path / "scripts").exists()
    has_templates = (workspace_path / "templates").exists()
    has_examples = (workspace_path / "examples.md").exists()
    has_references = (workspace_path / "references").exists()

    # Lite skills should have examples.md, not references/
    if skill_name.endswith("-lite"):
        if has_examples:
            print_pass(f"{skill_name}: Has examples.md (correct)")
            passed_tests += 1
        else:
            print_warn(f"{skill_name}: Missing examples.md")
            warnings += 1

        # Check scripts if they should exist
        if has_scripts:
            # Verify both bash and python scripts exist
            scripts_dir = workspace_path / "scripts"
            scripts = list(scripts_dir.glob("*"))
            has_sh = any(s.suffix == ".sh" for s in scripts)
            has_py = any(s.suffix == ".py" for s in scripts)

            if has_sh and has_py:
                print_pass(f"{skill_name}: Has both bash and python scripts")
                passed_tests += 1
            elif has_sh or has_py:
                print_warn(f"{skill_name}: Has only {'bash' if has_sh else 'python'} scripts")
                warnings += 1

    return True

def test_config_files_exist(profile: str, manifest: Dict) -> bool:
    """Test that settings and CLAUDE.md files exist"""
    global passed_tests, failed_tests

    settings_file = INSTALL_DIR / "settings" / manifest["settingsFile"]
    claude_md_file = INSTALL_DIR / "claude-md" / manifest["claudeMdFile"]

    all_exist = True

    print_test(f"Checking {manifest['settingsFile']} exists")
    if not settings_file.exists():
        print_fail(f"Settings file not found: {settings_file}")
        failed_tests += 1
        all_exist = False
    else:
        # Validate JSON
        try:
            with open(settings_file) as f:
                json.load(f)
            print_pass("Settings file is valid JSON")
            passed_tests += 1
        except json.JSONDecodeError as e:
            print_fail(f"Invalid settings JSON: {e}")
            failed_tests += 1
            all_exist = False

    print_test(f"Checking {manifest['claudeMdFile']} exists")
    if not claude_md_file.exists():
        print_fail(f"CLAUDE.md file not found: {claude_md_file}")
        failed_tests += 1
        all_exist = False
    else:
        print_pass("CLAUDE.md file exists")
        passed_tests += 1

    return all_exist

def test_skill_count(profile: str, manifest: Dict):
    """Test that skill counts match expectations"""
    global passed_tests, failed_tests, warnings

    definitions_count = len(manifest["skills"]["definitions"])
    workspace_count = len(manifest["skills"]["workspace"])

    print_test(f"Checking skill counts for {profile} edition")

    if profile == "lite":
        # Lite should have: 2 meta (master, status) + 3 prod + 4 dev = 9 total
        expected_definitions = 9
        expected_workspace = 8  # master has no workspace

        if definitions_count == expected_definitions:
            print_pass(f"Lite has {definitions_count} skill definitions (expected)")
            passed_tests += 1
        else:
            print_warn(f"Lite has {definitions_count} skill definitions (expected {expected_definitions})")
            warnings += 1

        if workspace_count == expected_workspace:
            print_pass(f"Lite has {workspace_count} workspace implementations (expected)")
            passed_tests += 1
        else:
            print_warn(f"Lite has {workspace_count} workspace implementations (expected {expected_workspace})")
            warnings += 1

    # Check for -lite suffix on lite skills
    if profile == "lite":
        non_lite = [s for s in manifest["skills"]["definitions"]
                   if not s.endswith("-lite") and s not in ["shipkit-master", "shipkit-status"]]
        if non_lite:
            print_warn(f"Lite manifest has non-lite skills: {', '.join(non_lite)}")
            warnings += 1
        else:
            print_pass("All lite skills have -lite suffix")
            passed_tests += 1

def run_tests_for_profile(profile: str):
    """Run all tests for a given profile"""
    print_section(f"Testing {profile.upper()} Profile")

    # Test 1: Manifest exists and is valid JSON
    if not test_manifest_exists(profile):
        print_fail(f"Skipping remaining tests for {profile}")
        return

    # Test 2: Manifest structure
    valid, manifest = test_manifest_structure(profile)
    if not valid:
        print_fail(f"Skipping remaining tests for {profile}")
        return

    # Test 3: All referenced skills exist
    test_skill_files_exist(profile, manifest)

    # Test 4: Config files exist
    test_config_files_exist(profile, manifest)

    # Test 5: Skill structure
    print_section(f"Testing Skill Structures ({profile})")
    for skill_name in manifest["skills"]["definitions"]:
        test_skill_structure(skill_name)

    # Test 6: Workspace structure
    print_section(f"Testing Workspace Structures ({profile})")
    for skill_name in manifest["skills"]["workspace"]:
        test_workspace_structure(skill_name)

    # Test 7: Lite-specific tests
    if profile == "lite":
        print_section("Testing Lite-Specific Conventions")
        for skill_name in manifest["skills"]["workspace"]:
            if skill_name.endswith("-lite"):
                test_lite_skill_structure(skill_name)

    # Test 8: Skill counts
    test_skill_count(profile, manifest)

def main():
    global passed_tests, failed_tests, warnings

    print(f"\n{Colors.BOLD}Shipkit Installation Tests{Colors.RESET}")
    print(f"Repo: {REPO_ROOT}\n")

    # Test each profile
    profiles = ["lite"]  # Add "default" when ready

    for profile in profiles:
        run_tests_for_profile(profile)

    # Summary
    print_section("Test Summary")
    print(f"  {Colors.GREEN}✓{Colors.RESET} Passed:  {passed_tests}")
    print(f"  {Colors.RED}✗{Colors.RESET} Failed:  {failed_tests}")
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} Warnings: {warnings}")

    total = passed_tests + failed_tests
    if total > 0:
        pass_rate = (passed_tests / total) * 100
        print(f"\n  Pass Rate: {pass_rate:.1f}%")

    # Exit code
    if failed_tests > 0:
        print(f"\n{Colors.RED}Tests FAILED{Colors.RESET}")
        sys.exit(1)
    elif warnings > 0:
        print(f"\n{Colors.YELLOW}Tests PASSED with warnings{Colors.RESET}")
        sys.exit(0)
    else:
        print(f"\n{Colors.GREEN}All tests PASSED{Colors.RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()

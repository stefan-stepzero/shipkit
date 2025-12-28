#!/usr/bin/env bash
# Integration test - actually runs installation and validates result

set -euo pipefail

# Colors
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BLUE='\033[94m'
BOLD='\033[1m'
RESET='\033[0m'

print_section() {
    echo -e "\n${BOLD}$1${RESET}"
}

print_test() {
    echo -e "  ${BLUE}→${RESET} $1"
}

print_pass() {
    echo -e "  ${GREEN}✓${RESET} $1"
}

print_fail() {
    echo -e "  ${RED}✗${RESET} $1"
}

# Track results
PASSED=0
FAILED=0

# Get repo root (assuming tests/ is one level down)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Create temp directory for test installation
TEST_DIR=$(mktemp -d)
trap "rm -rf $TEST_DIR" EXIT

print_section "Shipkit Integration Test"
echo "Repo: $REPO_ROOT"
echo "Test target: $TEST_DIR"

# Test 1: Run installation (lite profile, bash)
print_section "Test: Install Lite Edition (bash scripts)"

print_test "Running installer..."
cd "$TEST_DIR"

# Use bash installer for this test
if bash "$REPO_ROOT/installers/install.sh" lite bash "$TEST_DIR" -y > /tmp/install.log 2>&1; then
    print_pass "Installation completed without errors"
    ((PASSED++))
else
    print_fail "Installation failed (exit code $?)"
    cat /tmp/install.log
    ((FAILED++))
    exit 1
fi

# Test 2: Verify directory structure
print_section "Test: Directory Structure"

check_dir() {
    if [ -d "$1" ]; then
        print_pass "Directory exists: $1"
        ((PASSED++))
        return 0
    else
        print_fail "Directory missing: $1"
        ((FAILED++))
        return 1
    fi
}

check_file() {
    if [ -f "$1" ]; then
        print_pass "File exists: $1"
        ((PASSED++))
        return 0
    else
        print_fail "File missing: $1"
        ((FAILED++))
        return 1
    fi
}

check_dir "$TEST_DIR/.claude"
check_dir "$TEST_DIR/.claude/skills"
check_dir "$TEST_DIR/.shipkit"
check_dir "$TEST_DIR/.shipkit/skills"

check_file "$TEST_DIR/.claude/settings.json"
check_file "$TEST_DIR/CLAUDE.md"

# Test 3: Verify skill definitions installed
print_section "Test: Skill Definitions Installed"

EXPECTED_SKILLS=(
    "shipkit-master"
    "shipkit-status"
    "prod-strategic-thinking-lite"
    "prod-personas-lite"
    "prod-user-stories-lite"
    "dev-specify-lite"
    "dev-plan-lite"
    "dev-tasks-lite"
    "dev-implement-lite"
)

for skill in "${EXPECTED_SKILLS[@]}"; do
    check_dir "$TEST_DIR/.claude/skills/$skill"
    check_file "$TEST_DIR/.claude/skills/$skill/SKILL.md"
done

# Test 4: Verify workspace implementations installed
print_section "Test: Workspace Implementations Installed"

# shipkit-master has no workspace implementation
WORKSPACE_SKILLS=(
    "shipkit-status"
    "prod-strategic-thinking-lite"
    "prod-personas-lite"
    "prod-user-stories-lite"
    "dev-specify-lite"
    "dev-plan-lite"
    "dev-tasks-lite"
    "dev-implement-lite"
)

for skill in "${WORKSPACE_SKILLS[@]}"; do
    check_dir "$TEST_DIR/.shipkit/skills/$skill"
done

# Test 5: Verify settings.json is valid
print_section "Test: Settings File Validation"

print_test "Checking settings.json is valid JSON..."
if python3 -c "import json; json.load(open('$TEST_DIR/.claude/settings.json'))" 2>/dev/null; then
    print_pass "settings.json is valid JSON"
    ((PASSED++))
else
    print_fail "settings.json is invalid JSON"
    ((FAILED++))
fi

# Test 6: Verify settings contain lite edition markers
print_test "Checking settings.json contains lite edition markers..."
if grep -q '"edition": "lite"' "$TEST_DIR/.claude/settings.json"; then
    print_pass "Settings marked as lite edition"
    ((PASSED++))
else
    print_fail "Settings not marked as lite edition"
    ((FAILED++))
fi

# Test 7: Verify CLAUDE.md mentions lite
print_test "Checking CLAUDE.md mentions Shipkit Lite..."
if grep -q "Shipkit Lite" "$TEST_DIR/CLAUDE.md"; then
    print_pass "CLAUDE.md contains Shipkit Lite reference"
    ((PASSED++))
else
    print_fail "CLAUDE.md missing Shipkit Lite reference"
    ((FAILED++))
fi

# Test 8: Verify scripts are executable
print_section "Test: Script Executability"

SKILL_WITH_SCRIPTS="prod-strategic-thinking-lite"
SCRIPT_PATH="$TEST_DIR/.shipkit/skills/$SKILL_WITH_SCRIPTS/scripts"

if [ -d "$SCRIPT_PATH" ]; then
    for script in "$SCRIPT_PATH"/*.sh; do
        if [ -x "$script" ]; then
            print_pass "Script is executable: $(basename $script)"
            ((PASSED++))
        else
            print_fail "Script not executable: $(basename $script)"
            ((FAILED++))
        fi
    done
fi

# Test 9: Verify templates exist
print_section "Test: Templates Installed"

SKILL_WITH_TEMPLATE="prod-strategic-thinking-lite"
TEMPLATE_PATH="$TEST_DIR/.shipkit/skills/$SKILL_WITH_TEMPLATE/templates"

if [ -d "$TEMPLATE_PATH" ]; then
    template_count=$(find "$TEMPLATE_PATH" -name "*.md" | wc -l)
    if [ "$template_count" -gt 0 ]; then
        print_pass "Found $template_count template(s) in $SKILL_WITH_TEMPLATE"
        ((PASSED++))
    else
        print_fail "No templates found in $SKILL_WITH_TEMPLATE"
        ((FAILED++))
    fi
fi

# Test 10: Verify examples.md at root (lite convention)
print_section "Test: Lite Convention - examples.md at root"

LITE_SKILL="prod-strategic-thinking-lite"
EXAMPLES_PATH="$TEST_DIR/.shipkit/skills/$LITE_SKILL/examples.md"

if [ -f "$EXAMPLES_PATH" ]; then
    print_pass "examples.md at root for $LITE_SKILL (correct for lite)"
    ((PASSED++))
else
    print_fail "examples.md missing at root for $LITE_SKILL"
    ((FAILED++))
fi

# Test 11: Count installed skills
print_section "Test: Skill Count"

INSTALLED_DEFINITIONS=$(find "$TEST_DIR/.claude/skills" -mindepth 1 -maxdepth 1 -type d | wc -l)
INSTALLED_WORKSPACE=$(find "$TEST_DIR/.shipkit/skills" -mindepth 1 -maxdepth 1 -type d | wc -l)

print_test "Counting installed skills..."
echo "  Definitions: $INSTALLED_DEFINITIONS"
echo "  Workspace: $INSTALLED_WORKSPACE"

EXPECTED_DEFINITIONS=9
EXPECTED_WORKSPACE=8  # master has no workspace

if [ "$INSTALLED_DEFINITIONS" -eq "$EXPECTED_DEFINITIONS" ]; then
    print_pass "Correct number of skill definitions ($EXPECTED_DEFINITIONS)"
    ((PASSED++))
else
    print_fail "Wrong number of skill definitions (expected $EXPECTED_DEFINITIONS, got $INSTALLED_DEFINITIONS)"
    ((FAILED++))
fi

if [ "$INSTALLED_WORKSPACE" -eq "$EXPECTED_WORKSPACE" ]; then
    print_pass "Correct number of workspace implementations ($EXPECTED_WORKSPACE)"
    ((PASSED++))
else
    print_fail "Wrong number of workspace implementations (expected $EXPECTED_WORKSPACE, got $INSTALLED_WORKSPACE)"
    ((FAILED++))
fi

# Summary
print_section "Test Summary"
TOTAL=$((PASSED + FAILED))
echo -e "  ${GREEN}✓${RESET} Passed:  $PASSED"
echo -e "  ${RED}✗${RESET} Failed:  $FAILED"

if [ $TOTAL -gt 0 ]; then
    PASS_RATE=$(( (PASSED * 100) / TOTAL ))
    echo ""
    echo "  Pass Rate: ${PASS_RATE}%"
fi

# Exit code
if [ $FAILED -gt 0 ]; then
    echo -e "\n${RED}Tests FAILED${RESET}"
    exit 1
else
    echo -e "\n${GREEN}All tests PASSED${RESET}"
    exit 0
fi

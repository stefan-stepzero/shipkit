#!/usr/bin/env bash
# Master test runner - runs all test suites

set -euo pipefail

# Colors
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BLUE='\033[94m'
BOLD='\033[1m'
RESET='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BOLD}Shipkit Test Suite${RESET}"
echo "=================="
echo ""

# Track overall results
SUITES_PASSED=0
SUITES_FAILED=0

run_suite() {
    local name="$1"
    local command="$2"

    echo -e "\n${BOLD}Running: $name${RESET}"
    echo "----------------------------------------"

    if eval "$command"; then
        echo -e "${GREEN}✓${RESET} $name PASSED"
        ((SUITES_PASSED++))
        return 0
    else
        echo -e "${RED}✗${RESET} $name FAILED"
        ((SUITES_FAILED++))
        return 1
    fi
}

# Test Suite 1: Installation validation
run_suite "Installation Validation" "python3 $SCRIPT_DIR/test-installation.py"

# Test Suite 2: Skill compliance
run_suite "Skill Compliance" "python3 $SCRIPT_DIR/test-skill-compliance.py"

# Test Suite 3: Integration test (actual installation)
# Note: This is slower, so run it last
echo -e "\n${YELLOW}Note: Integration test will install to temp directory (this may take a minute)${RESET}"
run_suite "Integration Test" "bash $SCRIPT_DIR/test-integration.sh"

# Summary
echo ""
echo "========================================"
echo -e "${BOLD}Overall Test Results${RESET}"
echo "========================================"
echo -e "  ${GREEN}✓${RESET} Suites Passed: $SUITES_PASSED"
echo -e "  ${RED}✗${RESET} Suites Failed: $SUITES_FAILED"

if [ $SUITES_FAILED -gt 0 ]; then
    echo ""
    echo -e "${RED}TESTS FAILED${RESET}"
    exit 1
else
    echo ""
    echo -e "${GREEN}ALL TESTS PASSED${RESET}"
    exit 0
fi

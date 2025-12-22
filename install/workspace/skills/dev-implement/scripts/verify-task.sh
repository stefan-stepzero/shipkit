#!/usr/bin/env bash
# verify-task.sh - Evidence-based task completion verification
# Part of shipkit dev-implement skill

set -e

# =============================================================================
# SETUP
# =============================================================================

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# =============================================================================
# PARSE ARGUMENTS
# =============================================================================

TASK_NUMBER=""
SPEC_PATH=""
TEST_COMMAND=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --task=*)
      TASK_NUMBER="${1#*=}"
      shift
      ;;
    --spec-path=*)
      SPEC_PATH="${1#*=}"
      shift
      ;;
    --test-command=*)
      TEST_COMMAND="${1#*=}"
      shift
      ;;
    --help|-h)
      echo "Usage: $0 --task=N --spec-path=PATH --test-command=CMD"
      echo ""
      echo "Flags:"
      echo "  --task=N              Task number to verify"
      echo "  --spec-path=PATH      Path to spec directory"
      echo "  --test-command=CMD    Test command to run (e.g., 'npm test')"
      echo "  --help, -h            Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

# =============================================================================
# VALIDATE INPUTS
# =============================================================================

if [[ -z "$TASK_NUMBER" ]]; then
  echo -e "${RED}✗${NC} Task number required (--task=N)"
  exit 1
fi

if [[ -z "$SPEC_PATH" ]]; then
  echo -e "${RED}✗${NC} Spec path required (--spec-path=PATH)"
  exit 1
fi

if [[ -z "$TEST_COMMAND" ]]; then
  echo -e "${YELLOW}⚠${NC} No test command provided. Skipping test verification."
  echo "Provide --test-command='npm test' for full verification."
fi

# Normalize to absolute path
if [[ ! "$SPEC_PATH" = /* ]]; then
  SPEC_PATH="$REPO_ROOT/.shipkit/skills/dev-tasks/outputs/$SPEC_PATH"
fi

TASKS_FILE="$SPEC_PATH/tasks.md"

if [[ ! -f "$TASKS_FILE" ]]; then
  echo -e "${RED}✗${NC} Tasks file not found: $TASKS_FILE"
  exit 1
fi

# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================

echo ""
echo -e "${CYAN}Task $TASK_NUMBER Verification Checklist${NC}"
echo ""

VERIFICATION_PASSED=true

# Check 1: Tests run
if [[ -n "$TEST_COMMAND" ]]; then
  echo -e "${CYAN}[1/4]${NC} Running test suite..."
  echo "Command: $TEST_COMMAND"
  echo ""

  if eval "$TEST_COMMAND"; then
    echo ""
    echo -e "  ${GREEN}✓${NC} Tests passed"
  else
    echo ""
    echo -e "  ${RED}✗${NC} Tests failed"
    VERIFICATION_PASSED=false
  fi
else
  echo -e "${YELLOW}[1/4]${NC} Test verification skipped (no test command provided)"
fi

echo ""

# Check 2: Git status clean (no uncommitted changes in src)
echo -e "${CYAN}[2/4]${NC} Checking git status..."
if has_git; then
  UNCOMMITTED=$(git status --porcelain 2>/dev/null | grep -v "^??" || true)
  if [[ -z "$UNCOMMITTED" ]]; then
    echo -e "  ${GREEN}✓${NC} All changes committed"
  else
    echo -e "  ${YELLOW}⚠${NC} Uncommitted changes:"
    echo "$UNCOMMITTED" | sed 's/^/    /'
    echo ""
    echo "  Commit your changes before marking task complete."
    VERIFICATION_PASSED=false
  fi
else
  echo -e "  ${YELLOW}⚠${NC} Not a git repository (skipping check)"
fi

echo ""

# Check 3: Task marked complete in tasks.md
echo -e "${CYAN}[3/4]${NC} Checking task completion status..."

# Extract the task line (simplified - looks for task number pattern)
TASK_LINE=$(grep -n "Task $TASK_NUMBER:" "$TASKS_FILE" | head -1 || echo "")

if [[ -z "$TASK_LINE" ]]; then
  echo -e "  ${YELLOW}⚠${NC} Could not find Task $TASK_NUMBER in tasks.md"
  echo "  Manual verification required"
else
  LINE_NUM=$(echo "$TASK_LINE" | cut -d: -f1)
  TASK_TEXT=$(sed -n "${LINE_NUM}p" "$TASKS_FILE")

  if [[ "$TASK_TEXT" =~ ^\s*-\s*\[X\] ]] || [[ "$TASK_TEXT" =~ ^\s*-\s*\[x\] ]]; then
    echo -e "  ${GREEN}✓${NC} Task marked complete in tasks.md"
  else
    echo -e "  ${YELLOW}⚠${NC} Task not yet marked complete"
    echo "  Mark with [X] after verification passes"
  fi
fi

echo ""

# Check 4: Evidence provided
echo -e "${CYAN}[4/4]${NC} Evidence requirements:"
echo ""
echo "  Required evidence before claiming completion:"
echo "  • Fresh test output (not cached/remembered)"
echo "  • Complete output (not partial/summarized)"
echo "  • Relevant to claim (tests pass = show passing tests)"
echo ""

if [[ -n "$TEST_COMMAND" ]]; then
  echo -e "  ${GREEN}✓${NC} Test command executed (see output above)"
else
  echo -e "  ${YELLOW}⚠${NC} No test command run (evidence not captured)"
fi

echo ""

# =============================================================================
# VERIFICATION RESULT
# =============================================================================

echo -e "${CYAN}════════════════════════════════════════${NC}"
echo ""

if [[ "$VERIFICATION_PASSED" == "true" ]]; then
  echo -e "${GREEN}✓ VERIFICATION PASSED${NC}"
  echo ""
  echo "Task $TASK_NUMBER is ready to be marked complete."
  echo "All tests passing, changes committed, evidence captured."
  exit 0
else
  echo -e "${RED}✗ VERIFICATION FAILED${NC}"
  echo ""
  echo "Task $TASK_NUMBER cannot be marked complete yet."
  echo "Fix the issues above and re-run verification."
  exit 1
fi

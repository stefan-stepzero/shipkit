#!/usr/bin/env bash
# start-implementation.sh - Start implementation with mode selection and task tracking
# Part of shipkit dev-implement skill

set -e

# =============================================================================
# SETUP
# =============================================================================

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# Get skill directory
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REFERENCES_DIR="$SKILL_DIR/references"

# =============================================================================
# PARSE ARGUMENTS
# =============================================================================

SPEC_PATH=""
MODE=""
SKIP_PREREQS=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --mode=*)
      MODE="${1#*=}"
      shift
      ;;
    --skip-prereqs)
      SKIP_PREREQS=true
      shift
      ;;
    --cancel)
      echo "Cancelled."
      exit 0
      ;;
    --help|-h)
      echo "Usage: $0 [spec-path] [--mode=direct|subagent] [--skip-prereqs] [--cancel]"
      echo ""
      echo "Arguments:"
      echo "  spec-path       Path to spec directory (e.g., specs/1-feature-name)"
      echo ""
      echo "Flags:"
      echo "  --mode=MODE     Force execution mode (direct or subagent)"
      echo "  --skip-prereqs  Skip prerequisite checks"
      echo "  --cancel        Cancel operation"
      echo "  --help, -h      Show this help message"
      exit 0
      ;;
    *)
      if [[ -z "$SPEC_PATH" ]]; then
        SPEC_PATH="$1"
      else
        echo "Unknown argument: $1" >&2
        exit 1
      fi
      shift
      ;;
  esac
done

# =============================================================================
# DETERMINE SPEC PATH
# =============================================================================

# If no spec path provided, try to find from current branch
if [[ -z "$SPEC_PATH" ]]; then
  CURRENT_BRANCH=$(get_current_branch)

  # Extract numeric prefix if branch follows NNN- pattern
  if [[ "$CURRENT_BRANCH" =~ ^([0-9]{3})- ]]; then
    PREFIX="${BASH_REMATCH[1]}"
    SPEC_PATH=$(find_feature_dir_by_prefix "$REPO_ROOT" "$CURRENT_BRANCH")
  else
    echo -e "${RED}✗${NC} Could not determine spec path from branch: $CURRENT_BRANCH"
    echo "Please provide spec path explicitly: $0 specs/N-feature-name"
    exit 1
  fi
fi

# Normalize to absolute path
if [[ ! "$SPEC_PATH" = /* ]]; then
  SPEC_PATH="$REPO_ROOT/.shipkit/skills/dev-tasks/outputs/$SPEC_PATH"
fi

# =============================================================================
# CHECK PREREQUISITES
# =============================================================================

if [[ "$SKIP_PREREQS" == "false" ]]; then
  check_skill_prerequisites "dev-implement" "$SKIP_PREREQS"
fi

# =============================================================================
# VERIFY REQUIRED FILES EXIST
# =============================================================================

TASKS_FILE="$SPEC_PATH/tasks.md"
CONSTITUTION_FILE="$REPO_ROOT/.shipkit/skills/dev-constitution/outputs/constitution.md"

if [[ ! -f "$TASKS_FILE" ]]; then
  echo -e "${RED}✗${NC} Tasks file not found: $TASKS_FILE"
  echo "Run /dev-tasks first to create task breakdown."
  exit 1
fi

if [[ ! -f "$CONSTITUTION_FILE" ]]; then
  echo -e "${YELLOW}⚠${NC} Constitution not found: $CONSTITUTION_FILE"
  echo "It's strongly recommended to run /dev-constitution first."
  echo ""
  echo "Continue anyway? (yes/no)"
  read -r response
  if [[ "$response" != "yes" ]]; then
    exit 1
  fi
fi

echo -e "${GREEN}✓${NC} Tasks file: $TASKS_FILE"
if [[ -f "$CONSTITUTION_FILE" ]]; then
  echo -e "${GREEN}✓${NC} Constitution: $CONSTITUTION_FILE"
fi

# =============================================================================
# COUNT TASKS
# =============================================================================

echo ""
echo -e "${CYAN}Analyzing task complexity...${NC}"
echo ""

# Count tasks (lines starting with "- [ ]" or "- [X]" or "- [x]")
TOTAL_TASKS=$(grep -cE '^\s*- \[[Xx ]\]' "$TASKS_FILE" 2>/dev/null || echo "0")

# Count incomplete tasks (lines starting with "- [ ]")
INCOMPLETE_TASKS=$(grep -cE '^\s*- \[ \]' "$TASKS_FILE" 2>/dev/null || echo "0")

# Count completed tasks
COMPLETED_TASKS=$((TOTAL_TASKS - INCOMPLETE_TASKS))

echo "  Total tasks: $TOTAL_TASKS"
echo "  Completed: $COMPLETED_TASKS"
echo "  Remaining: $INCOMPLETE_TASKS"
echo ""

if [[ $INCOMPLETE_TASKS -eq 0 ]]; then
  echo -e "${GREEN}✓${NC} All tasks already complete!"
  echo ""
  echo "Next: Run /dev-finish to complete the development branch."
  exit 0
fi

# =============================================================================
# DETERMINE EXECUTION MODE
# =============================================================================

RECOMMENDED_MODE="direct"
if [[ $INCOMPLETE_TASKS -ge 6 ]]; then
  RECOMMENDED_MODE="subagent"
fi

if [[ -z "$MODE" ]]; then
  # No mode specified, recommend based on task count
  echo -e "${CYAN}Execution Mode Recommendation:${NC}"
  echo ""

  if [[ "$RECOMMENDED_MODE" == "direct" ]]; then
    echo "  Recommended: DIRECT mode"
    echo "  Reason: $INCOMPLETE_TASKS tasks (low overhead, faster)"
    echo ""
    echo "  Direct mode:"
    echo "  • Single context execution"
    echo "  • Faster for small implementations"
    echo "  • Best when tasks are tightly coupled"
  else
    echo "  Recommended: SUBAGENT mode"
    echo "  Reason: $INCOMPLETE_TASKS tasks (fresh context per task)"
    echo ""
    echo "  Subagent mode:"
    echo "  • Fresh context per task"
    echo "  • Controller maintains overview"
    echo "  • Better for large implementations"
  fi

  echo ""
  MODE="$RECOMMENDED_MODE"
else
  # Mode was specified via flag
  echo -e "${CYAN}Execution Mode:${NC} $MODE (forced by --mode flag)"
fi

echo ""
echo -e "${CYAN}Selected mode:${NC} $MODE"
echo ""

# =============================================================================
# CHECK FOR OPTIONAL CONTEXT FILES
# =============================================================================

echo -e "${CYAN}Available context files:${NC}"

SPEC_FILE="$SPEC_PATH/spec.md"
PLAN_FILE="$SPEC_PATH/plan.md"
DATA_MODEL_FILE="$SPEC_PATH/data-model.md"
CONTRACTS_DIR="$SPEC_PATH/contracts"

if [[ -f "$SPEC_FILE" ]]; then
  echo -e "  ${GREEN}✓${NC} $SPEC_FILE"
else
  echo -e "  ${YELLOW}⚠${NC} $SPEC_FILE (missing)"
fi

if [[ -f "$PLAN_FILE" ]]; then
  echo -e "  ${GREEN}✓${NC} $PLAN_FILE"
else
  echo -e "  ${YELLOW}⚠${NC} $PLAN_FILE (missing)"
fi

if [[ -f "$DATA_MODEL_FILE" ]]; then
  echo -e "  ${GREEN}✓${NC} $DATA_MODEL_FILE"
else
  echo -e "  ${YELLOW}⚠${NC} $DATA_MODEL_FILE (optional)"
fi

if [[ -d "$CONTRACTS_DIR" ]] && [[ -n $(ls -A "$CONTRACTS_DIR" 2>/dev/null) ]]; then
  echo -e "  ${GREEN}✓${NC} $CONTRACTS_DIR/ (contains files)"
else
  echo -e "  ${YELLOW}⚠${NC} $CONTRACTS_DIR/ (optional)"
fi

echo ""

# =============================================================================
# REFERENCE FILES
# =============================================================================

echo -e "${CYAN}Available references:${NC}"

if [[ -f "$REFERENCES_DIR/tdd-reference.md" ]]; then
  echo -e "  ${GREEN}✓${NC} $REFERENCES_DIR/tdd-reference.md (RED-GREEN-REFACTOR)"
else
  echo -e "  ${YELLOW}⚠${NC} $REFERENCES_DIR/tdd-reference.md (missing)"
fi

if [[ -f "$REFERENCES_DIR/verification-reference.md" ]]; then
  echo -e "  ${GREEN}✓${NC} $REFERENCES_DIR/verification-reference.md (evidence gates)"
else
  echo -e "  ${YELLOW}⚠${NC} $REFERENCES_DIR/verification-reference.md (missing)"
fi

if [[ -f "$REFERENCES_DIR/debugging-reference.md" ]]; then
  echo -e "  ${GREEN}✓${NC} $REFERENCES_DIR/debugging-reference.md (root cause)"
else
  echo -e "  ${YELLOW}⚠${NC} $REFERENCES_DIR/debugging-reference.md (missing)"
fi

echo ""

# =============================================================================
# READY FOR CLAUDE
# =============================================================================

echo -e "${GREEN}✓${NC} Ready for implementation"
echo ""
echo -e "${CYAN}Next Steps for Claude:${NC}"
echo ""
echo "  1. Read constitution FIRST: $CONSTITUTION_FILE"
echo "  2. Read task context:"
echo "     • $TASKS_FILE (required)"
if [[ -f "$SPEC_FILE" ]]; then
  echo "     • $SPEC_FILE"
fi
if [[ -f "$PLAN_FILE" ]]; then
  echo "     • $PLAN_FILE"
fi
echo "  3. Read references:"
echo "     • $REFERENCES_DIR/tdd-reference.md"
echo "     • $REFERENCES_DIR/verification-reference.md"
echo "     • $REFERENCES_DIR/debugging-reference.md"
echo ""

if [[ "$MODE" == "direct" ]]; then
  echo "  4. Execute in DIRECT mode:"
  echo "     • Process all tasks in single context"
  echo "     • For each task:"
  echo "       - 🔴 RED: Write failing test"
  echo "       - 🟢 GREEN: Implement to pass"
  echo "       - 🔵 REFACTOR: Clean up"
  echo "       - ✓ Spec compliance review"
  echo "       - ✓ Code quality review"
  echo "       - ✓ Verification (evidence required)"
  echo "       - Mark task [X] in tasks.md"
else
  echo "  4. Execute in SUBAGENT mode:"
  echo "     • Dispatch fresh context per task"
  echo "     • Controller (you) maintains overview"
  echo "     • For each task:"
  echo "       - Extract task + context"
  echo "       - Dispatch implementation subagent"
  echo "       - Review subagent's work"
  echo "       - Verify and mark complete"
fi

echo ""
echo -e "${YELLOW}Remember:${NC}"
echo "  • Constitution guides ALL decisions (read FIRST, reference THROUGHOUT)"
echo "  • TDD is mandatory (RED-GREEN-REFACTOR, no shortcuts)"
echo "  • Two-stage review required (spec compliance + code quality)"
echo "  • Evidence before completion (run tests, show output)"
echo "  • When tests fail → systematic debugging (find root cause)"
echo ""

exit 0

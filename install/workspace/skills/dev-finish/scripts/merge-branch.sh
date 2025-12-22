#!/usr/bin/env bash
# merge-branch.sh - Execute chosen merge option
# Part of shipkit dev-finish skill

set -e

# =============================================================================
# SETUP
# =============================================================================

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# =============================================================================
# PARSE FLAGS
# =============================================================================

OPTION=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --option=*)
      OPTION="${1#*=}"
      shift
      ;;
    --help|-h)
      echo "Usage: $0 --option=N"
      echo ""
      echo "Options:"
      echo "  --option=1   Merge to main/master locally"
      echo "  --option=2   Keep branch as-is"
      echo "  --option=3   Discard branch"
      echo "  --help, -h   Show this help message"
      exit 0
      ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$OPTION" ]]; then
  echo -e "${RED}✗${NC} Missing --option flag"
  echo "Usage: $0 --option=N (where N is 1, 2, or 3)"
  exit 1
fi

# =============================================================================
# VALIDATE GIT STATE
# =============================================================================

# Check if we're in a git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo -e "${RED}✗${NC} Not in a git repository"
  exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ -z "$CURRENT_BRANCH" ]]; then
  echo -e "${RED}✗${NC} Not on a branch (detached HEAD)"
  exit 1
fi

# Determine base branch
BASE_BRANCH=""
for branch in main master develop; do
  if git rev-parse --verify "$branch" > /dev/null 2>&1; then
    if git merge-base HEAD "$branch" > /dev/null 2>&1; then
      BASE_BRANCH="$branch"
      break
    fi
  fi
done

if [[ -z "$BASE_BRANCH" ]]; then
  echo -e "${YELLOW}⚠${NC} Could not determine base branch automatically"
  echo ""
  read -p "Which branch should I merge to? " BASE_BRANCH
fi

# =============================================================================
# EXECUTE OPTION
# =============================================================================

case $OPTION in
  1)
    # Option 1: Merge to main/master locally
    echo ""
    echo -e "${CYAN}Option 1: Merging to $BASE_BRANCH locally${NC}"
    echo ""

    # Switch to base branch
    echo "Switching to $BASE_BRANCH..."
    git checkout "$BASE_BRANCH"

    # Pull latest
    echo "Pulling latest changes..."
    git pull

    # Merge feature branch
    echo "Merging $CURRENT_BRANCH..."
    git merge "$CURRENT_BRANCH"

    # Verify tests on merged result
    echo ""
    echo -e "${CYAN}Verifying tests after merge...${NC}"

    # Try to detect test command
    TEST_COMMAND=""
    if [[ -f "package.json" ]]; then
      TEST_COMMAND="npm test"
    elif [[ -f "Cargo.toml" ]]; then
      TEST_COMMAND="cargo test"
    elif [[ -f "pytest.ini" ]] || [[ -f "pyproject.toml" ]]; then
      TEST_COMMAND="pytest"
    elif [[ -f "go.mod" ]]; then
      TEST_COMMAND="go test ./..."
    elif [[ -f "Gemfile" ]]; then
      TEST_COMMAND="bundle exec rspec"
    fi

    if [[ -n "$TEST_COMMAND" ]]; then
      if $TEST_COMMAND; then
        echo ""
        echo -e "${GREEN}✓${NC} Tests pass after merge"
      else
        echo ""
        echo -e "${RED}✗${NC} Tests failing after merge!"
        echo "Fix tests before completing merge."
        exit 1
      fi
    else
      echo -e "${YELLOW}⚠${NC} Could not detect test command"
      read -p "Run tests manually, then press Enter when ready to continue..."
    fi

    # Delete feature branch
    echo ""
    echo "Deleting branch $CURRENT_BRANCH..."
    git branch -d "$CURRENT_BRANCH"

    echo ""
    echo -e "${GREEN}✓${NC} Merge complete!"
    echo -e "  Branch: $CURRENT_BRANCH → $BASE_BRANCH"
    echo -e "  Status: Merged and cleaned up"
    ;;

  2)
    # Option 2: Keep branch as-is
    echo ""
    echo -e "${CYAN}Option 2: Keeping branch as-is${NC}"
    echo ""
    echo -e "${GREEN}✓${NC} Branch $CURRENT_BRANCH preserved"
    echo "  You can merge or handle it later."
    ;;

  3)
    # Option 3: Discard work
    echo ""
    echo -e "${CYAN}Option 3: Discard work${NC}"
    echo ""
    echo -e "${RED}⚠ WARNING: This will permanently delete:${NC}"
    echo "  - Branch: $CURRENT_BRANCH"
    echo "  - All commits not in $BASE_BRANCH"
    echo ""

    # Show commits to be deleted
    echo "Commits to be deleted:"
    git log "$BASE_BRANCH..$CURRENT_BRANCH" --oneline
    echo ""

    # Confirm
    read -p "Type 'discard' to confirm deletion: " CONFIRMATION

    if [[ "$CONFIRMATION" != "discard" ]]; then
      echo ""
      echo -e "${YELLOW}Cancelled.${NC} Branch preserved."
      exit 0
    fi

    # Switch to base branch
    echo ""
    echo "Switching to $BASE_BRANCH..."
    git checkout "$BASE_BRANCH"

    # Force delete feature branch
    echo "Deleting branch $CURRENT_BRANCH..."
    git branch -D "$CURRENT_BRANCH"

    echo ""
    echo -e "${GREEN}✓${NC} Branch discarded"
    ;;

  *)
    echo -e "${RED}✗${NC} Invalid option: $OPTION"
    echo "Valid options: 1, 2, 3"
    exit 1
    ;;
esac

echo ""
exit 0

#!/usr/bin/env bash
# Common functions and variables for all scripts

# =============================================================================
# SKILL PREREQUISITE CHAIN (Declarative)
# =============================================================================

# Map: skill-name -> prerequisite-skill-name
declare -A SKILL_PREREQUISITES=(
  # Prod Skills (Sequential)
  ["prod-strategic-thinking"]=""                              # No prereq (first)
  ["prod-constitution-builder"]="prod-strategic-thinking"     # Reads strategy context
  ["prod-personas"]="prod-strategic-thinking"                 # Needs business context
  ["prod-jobs-to-be-done"]="prod-personas"                    # Needs user definition
  ["prod-market-analysis"]="prod-jobs-to-be-done"            # Needs JTBD context
  ["prod-brand-guidelines"]="prod-market-analysis"            # Needs market positioning
  ["prod-interaction-design"]="prod-brand-guidelines"         # Needs brand identity
  ["prod-user-stories"]="prod-interaction-design"             # Needs journey mapping
  ["prod-assumptions-and-risks"]="prod-user-stories"         # Needs requirements
  ["prod-success-metrics"]="prod-user-stories"               # Needs requirements

  # Prod Skills (Async - no strict prereqs but benefit from having context)
  ["prod-communicator"]=""                                    # Checks for any available artifacts
  ["prod-discussion"]=""                                      # Conversational trade-off facilitation

  # Dev Skills
  ["dev-constitution"]="prod-user-stories"                    # Needs product context (recommended)
  ["dev-specify"]="dev-constitution"                          # Needs technical standards
  # ["dev-plan"]="dev-specify"
  # ["dev-tasks"]="dev-plan"
  # ["dev-implement"]="dev-tasks"
)

# Map: skill-name -> output-file-path (relative to .shipkit/skills/)
declare -A SKILL_OUTPUT_FILES=(
  ["prod-strategic-thinking"]="prod-strategic-thinking/outputs/business-canvas.md"
  ["prod-constitution-builder"]="prod-constitution-builder/outputs/product-constitution.md"
  ["prod-personas"]="prod-personas/outputs/personas.md"
  ["prod-jobs-to-be-done"]="prod-jobs-to-be-done/outputs/jobs-to-be-done.md"
  ["prod-market-analysis"]="prod-market-analysis/outputs/market-analysis.md"
  ["prod-brand-guidelines"]="prod-brand-guidelines/outputs/brand-guidelines.md"
  ["prod-interaction-design"]="prod-interaction-design/outputs/interaction-design.md"
  ["prod-user-stories"]="prod-user-stories/outputs/user-stories.md"
  ["prod-assumptions-and-risks"]="prod-assumptions-and-risks/outputs/assumptions-and-risks.md"
  ["prod-success-metrics"]="prod-success-metrics/outputs/success-metrics.md"
  ["prod-communicator"]="prod-communicator/outputs/"  # Multiple timestamped files
  # prod-discussion has no output files (conversational only)

  # Dev Skills
  ["dev-constitution"]="dev-constitution/outputs/constitution.md"
  ["dev-specify"]="dev-specify/outputs/specs/"                  # Multiple spec dirs
  # ["dev-plan"]="dev-plan/outputs/specs/"  # Multiple plan dirs
  # ["dev-tasks"]="dev-tasks/outputs/specs/"  # Multiple task dirs
)

# =============================================================================
# DECISION EXIT CODES
# =============================================================================

EXIT_DECISION_NEEDED=10
EXIT_PREREQ_MISSING=11

# =============================================================================
# COLORS
# =============================================================================

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# =============================================================================
# STRUCTURED OUTPUT HELPERS
# =============================================================================

# Output structured decision message for Claude to parse
output_decision() {
  local type="$1"
  local message="$2"
  local options="$3"

  echo "DECISION_NEEDED: $type"
  echo "MESSAGE: $message"
  echo "OPTIONS: $options"
}

# =============================================================================
# PREREQUISITE CHECKING
# =============================================================================

# Check if skill prerequisites are met
# Usage: check_skill_prerequisites "prod-personas"
check_skill_prerequisites() {
  local skill_name="$1"
  local skip_prereqs="${2:-false}"  # Optional override

  # Skip if flag set
  if [[ "$skip_prereqs" == "true" ]]; then
    echo -e "${YELLOW}⚠${NC} Skipping prerequisite checks (--skip-prereqs)"
    return 0
  fi

  # Get prerequisite for this skill
  local prereq="${SKILL_PREREQUISITES[$skill_name]}"

  # No prerequisite required
  if [[ -z "$prereq" ]]; then
    return 0
  fi

  # Check if prerequisite output exists
  local prereq_file="${SKILL_OUTPUT_FILES[$prereq]}"
  local repo_root=$(get_repo_root)
  local full_path="$repo_root/.shipkit/skills/$prereq_file"

  if [[ ! -f "$full_path" ]]; then
    output_decision "PREREQUISITE_MISSING" \
      "This skill works best after: /$prereq (missing: $prereq_file)" \
      "--skip-prereqs (Continue anyway)"
    exit $EXIT_PREREQ_MISSING
  else
    echo -e "${GREEN}✓${NC} Prerequisite found: /$prereq"
  fi
}

# =============================================================================
# FILE EXISTENCE CHECKING
# =============================================================================

# Check if output file exists and prompt for action
# Usage: check_output_exists "$OUTPUT_FILE" "Strategy"
check_output_exists() {
  local output_file="$1"
  local artifact_name="$2"
  local update_flag="${3:-false}"
  local archive_flag="${4:-false}"

  if [[ ! -f "$output_file" ]]; then
    return 0  # File doesn't exist, proceed
  fi

  # If flags already set, skip decision
  if [[ "$update_flag" == "true" ]]; then
    echo -e "${GREEN}✓${NC} Updating existing $artifact_name"
    return 0
  fi

  if [[ "$archive_flag" == "true" ]]; then
    TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
    local dir=$(dirname "$output_file")
    local base=$(basename "$output_file" .md)
    local archive_file="$dir/${base}-${TIMESTAMP}.md"
    mv "$output_file" "$archive_file"
    echo -e "${GREEN}✓${NC} Archived existing $artifact_name to: $archive_file"
    return 0
  fi

  # No flag set - need decision
  output_decision "FILE_EXISTS" \
    "$artifact_name already exists at: $output_file" \
    "--update (Update existing) | --archive (Create new version) | --cancel (Cancel operation)"
  exit $EXIT_DECISION_NEEDED
}

# =============================================================================
# REPOSITORY HELPERS
# =============================================================================

# Get repository root, with fallback for non-git repositories
get_repo_root() {
    if git rev-parse --show-toplevel >/dev/null 2>&1; then
        git rev-parse --show-toplevel
    else
        # Fall back to script location for non-git repos
        local script_dir="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        (cd "$script_dir/../../.." && pwd)
    fi
}

# Get current branch, with fallback for non-git repositories
get_current_branch() {
    # First check if SPECIFY_FEATURE environment variable is set
    if [[ -n "${SPECIFY_FEATURE:-}" ]]; then
        echo "$SPECIFY_FEATURE"
        return
    fi

    # Then check git if available
    if git rev-parse --abbrev-ref HEAD >/dev/null 2>&1; then
        git rev-parse --abbrev-ref HEAD
        return
    fi

    # For non-git repos, try to find the latest feature directory
    local repo_root=$(get_repo_root)
    local specs_dir="$repo_root/.devkit/specs"

    if [[ -d "$specs_dir" ]]; then
        local latest_feature=""
        local highest=0

        for dir in "$specs_dir"/*; do
            if [[ -d "$dir" ]]; then
                local dirname=$(basename "$dir")
                if [[ "$dirname" =~ ^([0-9]{3})- ]]; then
                    local number=${BASH_REMATCH[1]}
                    number=$((10#$number))
                    if [[ "$number" -gt "$highest" ]]; then
                        highest=$number
                        latest_feature=$dirname
                    fi
                fi
            fi
        done

        if [[ -n "$latest_feature" ]]; then
            echo "$latest_feature"
            return
        fi
    fi

    echo "main"  # Final fallback
}

# Check if we have git available
has_git() {
    git rev-parse --show-toplevel >/dev/null 2>&1
}

check_feature_branch() {
    local branch="$1"
    local has_git_repo="$2"

    # For non-git repos, we can't enforce branch naming but still provide output
    if [[ "$has_git_repo" != "true" ]]; then
        echo "[specify] Warning: Git repository not detected; skipped branch validation" >&2
        return 0
    fi

    if [[ ! "$branch" =~ ^[0-9]{3}- ]]; then
        echo "ERROR: Not on a feature branch. Current branch: $branch" >&2
        echo "Feature branches should be named like: 001-feature-name" >&2
        return 1
    fi

    return 0
}

get_feature_dir() { echo "$1/.devkit/specs/$2"; }

# Find feature directory by numeric prefix instead of exact branch match
# This allows multiple branches to work on the same spec (e.g., 004-fix-bug, 004-add-feature)
find_feature_dir_by_prefix() {
    local repo_root="$1"
    local branch_name="$2"
    local specs_dir="$repo_root/.devkit/specs"

    # Extract numeric prefix from branch (e.g., "004" from "004-whatever")
    if [[ ! "$branch_name" =~ ^([0-9]{3})- ]]; then
        # If branch doesn't have numeric prefix, fall back to exact match
        echo "$specs_dir/$branch_name"
        return
    fi

    local prefix="${BASH_REMATCH[1]}"

    # Search for directories in specs/ that start with this prefix
    local matches=()
    if [[ -d "$specs_dir" ]]; then
        for dir in "$specs_dir"/"$prefix"-*; do
            if [[ -d "$dir" ]]; then
                matches+=("$(basename "$dir")")
            fi
        done
    fi

    # Handle results
    if [[ ${#matches[@]} -eq 0 ]]; then
        # No match found - return the branch name path (will fail later with clear error)
        echo "$specs_dir/$branch_name"
    elif [[ ${#matches[@]} -eq 1 ]]; then
        # Exactly one match - perfect!
        echo "$specs_dir/${matches[0]}"
    else
        # Multiple matches - this shouldn't happen with proper naming convention
        echo "ERROR: Multiple spec directories found with prefix '$prefix': ${matches[*]}" >&2
        echo "Please ensure only one spec directory exists per numeric prefix." >&2
        echo "$specs_dir/$branch_name"  # Return something to avoid breaking the script
    fi
}

get_feature_paths() {
    local repo_root=$(get_repo_root)
    local current_branch=$(get_current_branch)
    local has_git_repo="false"

    if has_git; then
        has_git_repo="true"
    fi

    # Use prefix-based lookup to support multiple branches per spec
    local feature_dir=$(find_feature_dir_by_prefix "$repo_root" "$current_branch")

    cat <<EOF
REPO_ROOT='$repo_root'
CURRENT_BRANCH='$current_branch'
HAS_GIT='$has_git_repo'
FEATURE_DIR='$feature_dir'
FEATURE_SPEC='$feature_dir/spec.md'
IMPL_PLAN='$feature_dir/plan.md'
TASKS='$feature_dir/tasks.md'
RESEARCH='$feature_dir/research.md'
DATA_MODEL='$feature_dir/data-model.md'
QUICKSTART='$feature_dir/quickstart.md'
CONTRACTS_DIR='$feature_dir/contracts'
EOF
}

check_file() { [[ -f "$1" ]] && echo "  ✓ $2" || echo "  ✗ $2"; }
check_dir() { [[ -d "$1" && -n $(ls -A "$1" 2>/dev/null) ]] && echo "  ✓ $2" || echo "  ✗ $2"; }


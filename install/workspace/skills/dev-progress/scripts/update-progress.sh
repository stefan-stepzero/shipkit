#!/usr/bin/env bash
# Update development progress tracking
set -euo pipefail

# =============================================================================
# FLAG PARSING
# =============================================================================

JSON_MODE=false
VERBOSE=false

show_help() {
  cat << 'EOF'
Usage: update-progress.sh [OPTIONS]

Update the development progress tracking document based on roadmap and git state.

OPTIONS:
  --json          Output in JSON format (for programmatic use)
  --verbose       Show detailed scanning information
  --help, -h      Show this help message

EXAMPLES:
  # Update progress (normal output)
  ./update-progress.sh

  # Update progress (JSON output)
  ./update-progress.sh --json

  # Update progress with detailed logging
  ./update-progress.sh --verbose

PREREQUISITES:
  - Roadmap must exist (.shipkit/skills/dev-roadmap/outputs/roadmap.md)

OUTPUT:
  - .shipkit/skills/dev-progress/outputs/progress.md

EOF
}

while [[ $# -gt 0 ]]; do
  case $1 in
    --json)
      JSON_MODE=true
      shift
      ;;
    --verbose)
      VERBOSE=true
      shift
      ;;
    --help|-h)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown flag: $1" >&2
      echo "Use --help for usage information" >&2
      exit 1
      ;;
  esac
done

# =============================================================================
# SETUP
# =============================================================================

# Get script directory and source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Source common.sh from workspace scripts
COMMON_SH="$SCRIPT_DIR/../../../scripts/bash/common.sh"
if [[ ! -f "$COMMON_SH" ]]; then
  echo "ERROR: common.sh not found at: $COMMON_SH" >&2
  exit 1
fi
source "$COMMON_SH"

# Setup paths
OUTPUT_DIR="$SKILL_DIR/outputs"
OUTPUT_FILE="$OUTPUT_DIR/progress.md"
TEMPLATE_FILE="$SKILL_DIR/templates/progress-template.md"

REPO_ROOT=$(get_repo_root)
ROADMAP_PATH="$REPO_ROOT/.shipkit/skills/dev-roadmap/outputs/roadmap.md"
SPECS_DIR="$REPO_ROOT/.shipkit/skills/dev-specify/outputs/specs"

# =============================================================================
# HEADER
# =============================================================================

if [[ "$JSON_MODE" != "true" ]]; then
  echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${CYAN}  Development Progress Tracker${NC}"
  echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo
fi

# =============================================================================
# PREREQUISITE CHECKS
# =============================================================================

if [[ "$VERBOSE" == "true" ]]; then
  echo -e "${BLUE}Checking prerequisites...${NC}"
  echo
fi

# Check for roadmap (required)
if [[ ! -f "$ROADMAP_PATH" ]]; then
  if [[ "$JSON_MODE" == "true" ]]; then
    echo '{"error":"roadmap_missing","message":"No roadmap found. Run /dev-roadmap first."}'
  else
    echo -e "${YELLOW}⚠️  No roadmap found${NC}" >&2
    echo >&2
    echo "Roadmap required for progress tracking." >&2
    echo >&2
    echo "Create roadmap first:" >&2
    echo "  /dev-roadmap" >&2
    echo >&2
  fi
  exit 1
fi

if [[ "$VERBOSE" == "true" ]]; then
  echo -e "${GREEN}✓${NC} Roadmap found: $ROADMAP_PATH"
  echo
fi

# =============================================================================
# SCAN CURRENT STATE
# =============================================================================

if [[ "$VERBOSE" == "true" ]]; then
  echo -e "${BLUE}Scanning current state...${NC}"
  echo
fi

# Count total specs from roadmap (count "### Spec N:" lines)
TOTAL_SPECS=$(grep -c "^### Spec [0-9]" "$ROADMAP_PATH" 2>/dev/null || echo "0")

# Scan spec directories
if [[ -d "$SPECS_DIR" ]]; then
  SPEC_DIRS=$(find "$SPECS_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null || echo "")
  SPEC_COUNT=$(echo "$SPEC_DIRS" | grep -c "." || echo "0")
else
  SPEC_DIRS=""
  SPEC_COUNT=0
fi

# Check git for merged branches (if git available)
MERGED_BRANCHES=""
if has_git; then
  # Look for merge commits mentioning "Spec" or numbered branches
  MERGED_BRANCHES=$(git log --all --merges --oneline --grep="Spec" 2>/dev/null | head -20 || echo "")
fi

if [[ "$VERBOSE" == "true" ]]; then
  echo -e "  ${GREEN}✓${NC} Total specs in roadmap: $TOTAL_SPECS"
  echo -e "  ${GREEN}✓${NC} Spec directories found: $SPEC_COUNT"
  if [[ -n "$MERGED_BRANCHES" ]]; then
    echo -e "  ${GREEN}✓${NC} Merged branches detected: $(echo "$MERGED_BRANCHES" | wc -l)"
  fi
  echo
fi

# =============================================================================
# CREATE OUTPUT DIRECTORY
# =============================================================================

mkdir -p "$OUTPUT_DIR"

# =============================================================================
# OUTPUT RESULTS
# =============================================================================

if [[ "$JSON_MODE" == "true" ]]; then
  # JSON output for programmatic use
  cat << EOF
{
  "roadmap_path": "$ROADMAP_PATH",
  "total_specs": $TOTAL_SPECS,
  "spec_count": $SPEC_COUNT,
  "specs_dir": "$SPECS_DIR",
  "spec_dirs": [
$(echo "$SPEC_DIRS" | sed 's/^/    "/' | sed 's/$/"/' | paste -sd ',' -)
  ],
  "merged_branches": [
$(echo "$MERGED_BRANCHES" | sed 's/^/    "/' | sed 's/$/"/' | paste -sd ',' -)
  ],
  "output_file": "$OUTPUT_FILE",
  "template_file": "$TEMPLATE_FILE"
}
EOF
else
  # Human-readable output
  echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${GREEN}Ready for Claude${NC}"
  echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo
  echo "Claude should now:"
  echo
  echo "  1. Read roadmap:"
  echo "     $ROADMAP_PATH"
  echo
  echo "  2. Analyze spec directories:"
  echo "     $SPECS_DIR"
  echo "     Found: $SPEC_COUNT spec(s)"
  echo
  echo "  3. Check git history:"
  if [[ -n "$MERGED_BRANCHES" ]]; then
    echo "     Merged branches detected:"
    echo "$MERGED_BRANCHES" | head -5 | sed 's/^/       /'
    [[ $(echo "$MERGED_BRANCHES" | wc -l) -gt 5 ]] && echo "       ... (see git log for more)"
  else
    echo "     No merged branches found (or git unavailable)"
  fi
  echo
  echo "  4. Determine status for each spec:"
  echo "     - ✅ Completed: Directory exists AND branch merged"
  echo "     - 🔄 Current: Directory exists but NOT merged yet"
  echo "     - 📋 Next: No directory, next in roadmap sequence"
  echo
  echo "  5. Load template:"
  echo "     $TEMPLATE_FILE"
  echo
  echo "  6. Fill in placeholders:"
  echo "     - {{TIMESTAMP}} - Current date/time"
  echo "     - {{COMPLETED_COUNT}} - Number of merged specs"
  echo "     - {{TOTAL_COUNT}} - Total specs from roadmap ($TOTAL_SPECS)"
  echo "     - {{PERCENTAGE}} - Progress percentage"
  echo "     - {{COMPLETED_SPECS}} - List of completed specs"
  echo "     - {{CURRENT_SPEC}} - Current in-progress spec (if any)"
  echo "     - {{NEXT_SPECS}} - Upcoming specs from roadmap"
  echo "     - {{IN_PROGRESS_COUNT}} - Number of active specs"
  echo "     - {{REMAINING_COUNT}} - Specs not started yet"
  echo "     - {{SUGGESTED_NEXT_ACTION}} - What to do next"
  echo
  echo "  7. Write to: $OUTPUT_FILE"
  echo
  echo -e "${CYAN}Output location:${NC} $OUTPUT_FILE"
  echo
  echo -e "${YELLOW}Remember:${NC}"
  echo "  - Only count merged specs as complete"
  echo "  - Show clear completed/current/next sections"
  echo "  - Suggest the next action"
  echo
fi

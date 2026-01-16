#!/usr/bin/env bash
# Simple progress snapshot for session continuity
set -e

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
CURRENT_FILE="$OUTPUT_DIR/progress-current.md"
TEMPLATE_FILE="$SKILL_DIR/templates/progress-template.md"

REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
REGISTRY_FILE="$REPO_ROOT/.shipkit/skills/dev-specify/outputs/specs/registry.txt"

mkdir -p "$OUTPUT_DIR"

# =============================================================================
# HEADER
# =============================================================================

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  Development Progress Snapshot${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

# =============================================================================
# ARCHIVE CURRENT PROGRESS
# =============================================================================

# Archive current progress file if it exists
if [[ -f "$CURRENT_FILE" ]]; then
  TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
  ARCHIVE_FILE="$OUTPUT_DIR/progress-$TIMESTAMP.md"
  cp "$CURRENT_FILE" "$ARCHIVE_FILE"
  echo -e "${GREEN}✓${NC} Archived: progress-$TIMESTAMP.md"
fi

# =============================================================================
# CREATE FRESH PROGRESS FILE
# =============================================================================

# Check template exists
if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo -e "${RED}ERROR: Template not found: $TEMPLATE_FILE${NC}" >&2
  exit 1
fi

# Create fresh progress file from template
cp "$TEMPLATE_FILE" "$CURRENT_FILE"
echo -e "${GREEN}✓${NC} Created: progress-current.md"
echo

# =============================================================================
# SHOW REGISTRY CONTEXT
# =============================================================================

echo -e "${CYAN}Existing specs (from registry):${NC}"
echo

if [[ -f "$REGISTRY_FILE" && -s "$REGISTRY_FILE" ]]; then
  SPEC_COUNT=$(wc -l < "$REGISTRY_FILE" | tr -d ' ')
  echo -e "  ${BLUE}○${NC} Total specs: $SPEC_COUNT"
  echo
  while IFS='|' read -r num name created; do
    echo "  $num: $name"
  done < "$REGISTRY_FILE"
else
  echo -e "  ${YELLOW}⚠${NC} No specs created yet"
fi

echo

# =============================================================================
# READY FOR CLAUDE
# =============================================================================

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Ready for Claude${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo "Claude should now:"
echo
echo "  1. Read current progress context:"
echo "     $CURRENT_FILE"
echo
echo "  2. Update progress-current.md with:"
echo "     • {{TIMESTAMP}} - Current date/time"
echo "     • {{COMPLETED_COUNT}} - Number of completed specs"
echo "     • {{TOTAL_COUNT}} - Total specs from registry"
echo "     • {{PERCENTAGE}} - Progress percentage"
echo "     • {{COMPLETED_SPECS}} - List completed specs (e.g., '001 - User Auth')"
echo "     • {{CURRENT_SPEC}} - Currently working on (e.g., '002 - Dashboard')"
echo "     • {{NEXT_SPECS}} - What's next from roadmap"
echo "     • {{IN_PROGRESS_COUNT}} - Usually 1"
echo "     • {{REMAINING_COUNT}} - Total - Completed - In Progress"
echo "     • {{SUGGESTED_NEXT_ACTION}} - What to do next"
echo
echo "  3. Base updates on:"
echo "     • Conversation context (what we just worked on)"
echo "     • NOT git history"
echo "     • Manual snapshot for session continuity"
echo
echo -e "${CYAN}Output:${NC} $CURRENT_FILE"
echo
echo -e "${YELLOW}Note:${NC} This is a manual snapshot - Claude updates based on conversation, not automated scanning"
echo

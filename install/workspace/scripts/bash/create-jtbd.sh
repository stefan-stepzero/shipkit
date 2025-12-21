#!/usr/bin/env bash
# create-jtbd.sh - Create jobs-to-be-done current state document
set -e
set -u

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Arguments
PERSONA=""
JOB=""
CURRENT_SOLUTION=""
STEPS=""
PAINS=""
WORKAROUNDS=""
FREQUENCY=""
SWITCHING_COSTS=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --persona) PERSONA="$2"; shift 2;;
    --job) JOB="$2"; shift 2;;
    --current-solution) CURRENT_SOLUTION="$2"; shift 2;;
    --steps) STEPS="$2"; shift 2;;
    --pains) PAINS="$2"; shift 2;;
    --workarounds) WORKAROUNDS="$2"; shift 2;;
    --frequency) FREQUENCY="$2"; shift 2;;
    --switching-costs) SWITCHING_COSTS="$2"; shift 2;;
    *)
      echo -e "${RED}Unknown argument: $1${NC}"
      exit 1
      ;;
  esac
done

# Validate
if [[ -z "$PERSONA" ]] || [[ -z "$JOB" ]]; then
  echo -e "${RED}Error: Missing required arguments${NC}"
  echo "Required: --persona, --job"
  exit 1
fi

# Create directory
mkdir -p .prodkit/discovery

# Initialize or append
if [[ ! -f ".prodkit/discovery/jobs-to-be-done-current.md" ]]; then
  cat > .prodkit/discovery/jobs-to-be-done-current.md <<EOF
# Jobs-to-be-Done (Current State)

Generated: $(date +"%Y-%m-%d")

This document captures how users **currently** solve their problems.

---

EOF
fi

# Append job
cat >> .prodkit/discovery/jobs-to-be-done-current.md <<EOF
## $PERSONA

**Job Statement**:
$JOB

**Current Solution**:
$CURRENT_SOLUTION

**Current Workflow Steps**:
$STEPS

**Pain Points**:
$PAINS

**Workarounds**:
$WORKAROUNDS

**Frequency**: $FREQUENCY

**Switching Costs**:
$SWITCHING_COSTS

---

EOF

# Touch AGENTS.md
if [[ -f ".claude/AGENTS.md" ]] || [[ -f ".github/AGENTS.md" ]]; then
  touch .claude/AGENTS.md 2>/dev/null || touch .github/AGENTS.md 2>/dev/null || true
fi

echo -e "${GREEN}✓${NC} Added JTBD for '$PERSONA' to .prodkit/discovery/jobs-to-be-done-current.md"

exit 0

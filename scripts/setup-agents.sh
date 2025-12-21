#!/usr/bin/env bash
# setup-agents.sh - Initialize agent personas for the project
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_info() { echo -e "${BLUE}ℹ${NC} $1"; }

# Get script directory (where agents are stored)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
AGENTS_SOURCE="$SCRIPT_DIR/agents"

# Target directory
TARGET_DIR=".claude/agents"

# Check if source exists
if [[ ! -d "$AGENTS_SOURCE" ]]; then
    echo "Error: Agent personas not found at $AGENTS_SOURCE" >&2
    exit 1
fi

# Create target directory
mkdir -p "$TARGET_DIR"

# Copy agent personas
print_info "Setting up agent personas..."

for agent in "$AGENTS_SOURCE"/*.md; do
    if [[ -f "$agent" ]]; then
        filename=$(basename "$agent")

        # Don't overwrite if exists (preserve customizations)
        if [[ -f "$TARGET_DIR/$filename" ]]; then
            print_info "  Skipping $filename (already exists)"
        else
            cp "$agent" "$TARGET_DIR/"
            print_success "  Installed $filename"
        fi
    fi
done

# Create agents index for Claude to read
cat > "$TARGET_DIR/index.md" << 'EOF'
# Agent Personas

Use these specialized agents for different parts of the workflow.

## Quick Reference

| Task | Agent | Invoke With |
|------|-------|-------------|
| ProdKit discovery | Discovery Agent | See `discovery-agent.md` |
| Technical planning | Architect Agent | See `architect-agent.md` |
| TDD implementation | Implementer Agent | See `implementer-agent.md` |
| Code review | Reviewer Agent | See `reviewer-agent.md` |
| Research tasks | Researcher Agent | See `researcher-agent.md` |

## When to Use

- **Subagent mode in /implement**: Use Implementer + Reviewer agents
- **Brainstorming**: Use Discovery + Researcher agents
- **Planning**: Use Architect agent
- **Reviews**: Use Reviewer agent

Read the individual agent files for detailed prompts and behaviors.
EOF

print_success "Agent personas ready at $TARGET_DIR/"

# Summary
echo ""
echo "Installed agents:"
ls -1 "$TARGET_DIR"/*.md 2>/dev/null | while read f; do
    echo "  - $(basename "$f")"
done

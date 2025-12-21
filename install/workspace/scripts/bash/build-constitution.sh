#!/usr/bin/env bash
# build-constitution.sh - Create or update project constitution
set -e

# Parse arguments
JSON_OUTPUT=false
PHASE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --json) JSON_OUTPUT=true; shift;;
        --phase) PHASE="$2"; shift 2;;
        *) shift;;
    esac
done

# Validate phase
if [[ -z "$PHASE" ]]; then
    echo "Error: --phase required (product or technical)" >&2
    exit 1
fi

if [[ "$PHASE" != "product" && "$PHASE" != "technical" ]]; then
    echo "Error: --phase must be 'product' or 'technical'" >&2
    exit 1
fi

# Configuration
CONSTITUTION_FILE=".claude/constitution.md"
DATE=$(date +%Y-%m-%d)

# Ensure .claude directory exists
mkdir -p .claude

# Check if constitution exists
if [[ -f "$CONSTITUTION_FILE" ]]; then
    STATUS="updated"
else
    STATUS="created"
fi

# Create constitution based on phase
if [[ "$PHASE" == "product" ]]; then
    # Create product constitution template
    cat > "$CONSTITUTION_FILE" << 'EOF'
# Project Constitution

## Product Principles

### Project Type
<!-- Fill in: SaaS/Consumer/Internal/Library/MVP -->

### Brand Voice
<!-- Fill in based on interview -->
- Tone:
- Error messages must be helpful and suggest resolution

### UX Requirements
<!-- Check applicable items -->
- [ ] Destructive actions require confirmation
- [ ] Forms show inline validation before submit
- [ ] Loading states required for actions >200ms
- [ ] Error messages suggest resolution
- [ ] Mobile-first responsive design
- [ ] Keyboard navigation support

### Accessibility
<!-- Fill in: WCAG 2.1 AA/AAA/Basic/None -->
- Standard:
- All images must have alt text
- All forms must have labels

---
EOF
    echo "*Product constitution created: $DATE*" >> "$CONSTITUTION_FILE"
    echo "*Technical section pending: Run /constitution-builder --technical*" >> "$CONSTITUTION_FILE"

elif [[ "$PHASE" == "technical" ]]; then
    # Append technical section to existing constitution
    if [[ -f "$CONSTITUTION_FILE" ]]; then
        # Remove the pending note if it exists
        sed -i 's/\*Technical section pending.*\*//g' "$CONSTITUTION_FILE" 2>/dev/null || true
    else
        # Create header if no product section exists
        echo "# Project Constitution" > "$CONSTITUTION_FILE"
        echo "" >> "$CONSTITUTION_FILE"
        echo "## Product Principles" >> "$CONSTITUTION_FILE"
        echo "*Product section not created - run /constitution-builder --product*" >> "$CONSTITUTION_FILE"
        echo "" >> "$CONSTITUTION_FILE"
    fi

    # Append technical section
    cat >> "$CONSTITUTION_FILE" << 'EOF'

---

## Technical Standards

### Team & Process
<!-- Fill in based on interview -->
- Team size:
- AI agents: Enabled

### Tech Stack
<!-- Fill in based on plan.md or interview -->
- Frontend:
- Backend:
- Database:
- Hosting:

### Architecture
<!-- Fill in based on interview -->
- Authentication:
- API style:

### Code Quality
<!-- Fill in based on interview -->
- Testing:
- Coverage target:
- Functions must be <50 lines
- Files must be <300 lines

### File Organization
<!-- Fill in based on interview -->
- Pattern:

### AI Agent Rules
- Dependencies: Ask before adding new packages
- Always run tests before marking task done
- Never commit secrets or credentials
- Follow existing patterns in codebase

---
EOF
    echo "*Technical constitution added: $DATE*" >> "$CONSTITUTION_FILE"
    echo "*Full constitution ready for /specify*" >> "$CONSTITUTION_FILE"
fi

# Output
if [[ "$JSON_OUTPUT" == true ]]; then
    cat << EOF
{
  "constitution_file": "$CONSTITUTION_FILE",
  "phase": "$PHASE",
  "created": "$DATE",
  "status": "$STATUS"
}
EOF
else
    echo "Constitution $STATUS at $CONSTITUTION_FILE (phase: $PHASE)"
fi

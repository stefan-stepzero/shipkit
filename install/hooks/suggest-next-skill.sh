#!/usr/bin/env bash
# suggest-next-skill.sh - Suggest next skill after Claude stops
#
# This hook runs when Claude finishes responding (Stop event).
# It analyzes the transcript to detect which skill just completed
# and suggests the logical next step in the workflow.

set -e

# Read hook input from stdin
INPUT=$(cat)

# Extract transcript path
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path')

# Check if stop hook is already active (prevent infinite loops)
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active')
if [[ "$STOP_HOOK_ACTIVE" == "true" ]]; then
  exit 0  # Don't suggest if we're already in a stop hook loop
fi

# Exit early if no transcript
if [[ ! -f "$TRANSCRIPT_PATH" ]]; then
  exit 0
fi

# Function to check if skill was recently invoked
skill_completed() {
  local skill_name="$1"
  grep -q "\"tool_name\":\"Skill\"" "$TRANSCRIPT_PATH" 2>/dev/null && \
  grep -q "\"skill\":\"$skill_name\"" "$TRANSCRIPT_PATH" 2>/dev/null
}

# Detect which skill just completed and suggest next step
# Product Discovery Chain
if skill_completed "prod-strategic-thinking"; then
  cat << 'EOF'

✅ Strategic thinking complete

👉 Suggested next step:
   /prod-constitution-builder - Define your product principles and project type (POC, MVP, Greenfield, etc.)

EOF
  exit 0
fi

if skill_completed "prod-constitution-builder"; then
  cat << 'EOF'

✅ Product constitution created

👉 Suggested next step:
   /prod-personas - Identify and document target users

EOF
  exit 0
fi

if skill_completed "prod-personas"; then
  cat << 'EOF'

✅ Personas defined

👉 Suggested next step:
   /prod-jobs-to-be-done - Map current state workflows and pain points

EOF
  exit 0
fi

if skill_completed "prod-jobs-to-be-done"; then
  cat << 'EOF'

✅ Jobs to be done mapped

👉 Suggested next step:
   /prod-market-analysis - Analyze competitive landscape

EOF
  exit 0
fi

if skill_completed "prod-market-analysis"; then
  cat << 'EOF'

✅ Market analysis complete

👉 Suggested next step:
   /prod-brand-guidelines - Define visual direction and personality

EOF
  exit 0
fi

if skill_completed "prod-brand-guidelines"; then
  cat << 'EOF'

✅ Brand guidelines established

👉 Suggested next step:
   /prod-interaction-design - Design future state user journeys

EOF
  exit 0
fi

if skill_completed "prod-interaction-design"; then
  cat << 'EOF'

✅ Interaction design complete

👉 Suggested next step:
   /prod-user-stories - Write actionable requirements with acceptance criteria

EOF
  exit 0
fi

if skill_completed "prod-user-stories"; then
  cat << 'EOF'

✅ User stories written

👉 Suggested next steps:
   /prod-assumptions-and-risks - Identify strategic risks
   OR
   /dev-constitution - Start technical implementation planning

EOF
  exit 0
fi

if skill_completed "prod-assumptions-and-risks"; then
  cat << 'EOF'

✅ Assumptions and risks documented

👉 Suggested next step:
   /prod-success-metrics - Define KPIs and instrumentation

EOF
  exit 0
fi

if skill_completed "prod-success-metrics"; then
  cat << 'EOF'

✅ Product discovery complete!

👉 Ready to start development:
   /dev-constitution - Reference or build technical standards
   Then:
   /dev-specify - Create feature specifications

EOF
  exit 0
fi

# Development Chain
if skill_completed "dev-constitution"; then
  cat << 'EOF'

✅ Technical constitution ready

👉 Suggested next step:
   /dev-specify - Create feature specification from description

EOF
  exit 0
fi

if skill_completed "dev-specify"; then
  cat << 'EOF'

✅ Specification created

👉 Suggested next steps:
   /dev-plan - Generate implementation plan (reads constitution)
   OR
   /dev-clarify - Resolve any ambiguities first (if needed)

EOF
  exit 0
fi

if skill_completed "dev-plan"; then
  cat << 'EOF'

✅ Implementation plan ready

👉 Suggested next step:
   /dev-tasks - Break plan into executable tasks

EOF
  exit 0
fi

if skill_completed "dev-tasks"; then
  cat << 'EOF'

✅ Tasks defined

👉 Suggested next step:
   /dev-implement - Execute tasks with integrated TDD + reviews

EOF
  exit 0
fi

if skill_completed "dev-implement"; then
  cat << 'EOF'

✅ Implementation complete

👉 Suggested next step:
   /dev-finish - Merge workflow with test validation

EOF
  exit 0
fi

if skill_completed "dev-roadmap"; then
  cat << 'EOF'

✅ Roadmap created

👉 Suggested next step:
   Start implementing features in roadmap order:
   /dev-plan - For the first spec in the roadmap

EOF
  exit 0
fi

# Communicator skill
if skill_completed "prod-communicator"; then
  cat << 'EOF'

✅ Stakeholder communication generated

Continue with your product discovery or development workflow.

EOF
  exit 0
fi

# Default: No specific suggestion
# This is normal - not every stop requires a skill suggestion
exit 0

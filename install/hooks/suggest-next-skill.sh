#!/usr/bin/env bash
# suggest-next-skill.sh - Suggest next skill after Claude stops
#
# This hook runs when Claude finishes responding (Stop event).
# It analyzes the last user/assistant exchange to detect which skill completed
# and suggests the logical next step in the workflow.

set -e

# Find the last skill invocation in .claude directory
# We'll check if any skill outputs were recently created/modified
LAST_SKILL=""

# Check for recently completed product skills (within last 60 seconds)
for skill in prod-strategic-thinking prod-constitution-builder prod-personas \
             prod-jobs-to-be-done prod-market-analysis prod-brand-guidelines \
             prod-interaction-design prod-user-stories prod-assumptions-and-risks \
             prod-success-metrics prod-communicator; do
    OUTPUT_DIR=".shipkit/skills/$skill/outputs"
    if [[ -d "$OUTPUT_DIR" ]]; then
        # Check if any files were modified in last 60 seconds
        if find "$OUTPUT_DIR" -type f -mmin -1 2>/dev/null | grep -q .; then
            LAST_SKILL="$skill"
            break
        fi
    fi
done

# If no product skill, check dev skills
if [[ -z "$LAST_SKILL" ]]; then
    for skill in dev-constitution-builder dev-specify dev-plan dev-tasks \
                 dev-implement dev-roadmap dev-finish; do
        OUTPUT_DIR=".shipkit/skills/$skill/outputs"
        if [[ -d "$OUTPUT_DIR" ]]; then
            if find "$OUTPUT_DIR" -type f -mmin -1 2>/dev/null | grep -q .; then
                LAST_SKILL="$skill"
                break
            fi
        fi
    done
fi

# Suggest next step based on completed skill
case "$LAST_SKILL" in
    prod-strategic-thinking)
        cat << 'EOF'

✅ Strategic thinking complete

👉 Next: /prod-constitution-builder - Define project type and principles

EOF
        ;;
    prod-constitution-builder)
        cat << 'EOF'

✅ Product constitution created

👉 Next: /prod-personas - Identify target users

EOF
        ;;
    prod-personas)
        cat << 'EOF'

✅ Personas defined

👉 Next: /prod-jobs-to-be-done - Map workflows and pain points

EOF
        ;;
    prod-jobs-to-be-done)
        cat << 'EOF'

✅ Jobs to be done mapped

👉 Next: /prod-market-analysis - Analyze competition

EOF
        ;;
    prod-market-analysis)
        cat << 'EOF'

✅ Market analysis complete

👉 Next: /prod-brand-guidelines - Define brand identity

EOF
        ;;
    prod-brand-guidelines)
        cat << 'EOF'

✅ Brand guidelines established

👉 Next: /prod-interaction-design - Design user journeys

EOF
        ;;
    prod-interaction-design)
        cat << 'EOF'

✅ Interaction design complete

👉 Next: /prod-user-stories - Write requirements

EOF
        ;;
    prod-user-stories)
        cat << 'EOF'

✅ User stories written

👉 Next: /prod-assumptions-and-risks OR /dev-constitution

EOF
        ;;
    prod-assumptions-and-risks)
        cat << 'EOF'

✅ Assumptions and risks documented

👉 Next: /prod-success-metrics - Define KPIs

EOF
        ;;
    prod-success-metrics)
        cat << 'EOF'

✅ Product discovery complete!

👉 Next: /dev-constitution - Start development

EOF
        ;;
    dev-constitution-builder)
        cat << 'EOF'

✅ Technical constitution ready

👉 Next: /dev-specify - Create feature spec

EOF
        ;;
    dev-specify)
        cat << 'EOF'

✅ Specification created

👉 Next: /dev-plan - Generate implementation plan

EOF
        ;;
    dev-plan)
        cat << 'EOF'

✅ Implementation plan ready

👉 Next: /dev-tasks - Break into tasks

EOF
        ;;
    dev-tasks)
        cat << 'EOF'

✅ Tasks defined

👉 Next: /dev-implement - Execute with TDD

EOF
        ;;
    dev-implement)
        cat << 'EOF'

✅ Implementation complete

👉 Next: /dev-finish - Merge and validate

EOF
        ;;
    dev-roadmap)
        cat << 'EOF'

✅ Roadmap created

👉 Next: /dev-plan - Start first feature

EOF
        ;;
    *)
        # No suggestion - normal, not every stop requires one
        ;;
esac

exit 0

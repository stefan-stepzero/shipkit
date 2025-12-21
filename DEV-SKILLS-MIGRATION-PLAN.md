# Dev Skills Migration Plan

**Created:** 2025-12-21
**Status:** Ready to Execute

## Overview

Migrate 20 dev skills from old structure to new hybrid architecture matching the completed prod skills pattern.

## Current State Analysis

### Skills with Infrastructure (1 skill)
**dev-specify** has:
- SKILL.md
- reference.md
- scripts/ directory
- templates/ directory (3 templates)

### Skills with Only SKILL.md (19 skills)
All others have only SKILL.md files:
- dev-tasks
- dev-plan
- dev-implement
- dev-analyze
- dev-checklist
- dev-clarify
- dev-taskstoissues
- dev-constitution
- dev-constitution-builder
- dev-requesting-code-review
- dev-receiving-code-review
- dev-finishing-a-development-branch
- dev-using-git-worktrees
- dev-systematic-debugging
- dev-test-driven-development
- dev-verification-before-completion
- dev-dispatching-parallel-agents
- dev-subagent-driven-development
- dev-writing-plans
- dev-writing-skills

## Target Structure

Following the prod skills pattern:

```
install/
├── skills/
│   └── [skill-name]/
│       └── SKILL.md               # Skill definition (Claude reads)
└── workspace/
    └── skills/
        └── [skill-name]/
            ├── scripts/           # Optional (only for artifact-generating skills)
            │   └── create-[artifact].sh
            ├── templates/         # Optional (only for artifact-generating skills)
            │   └── [artifact]-template.md
            ├── references/        # Always present
            │   ├── reference.md   # Extended guidance
            │   ├── examples.md    # Concrete examples
            │   └── README.md      # Explains folder
            └── outputs/           # Optional (created at runtime if needed)
```

## Migration Strategy

### Category 1: Artifact-Generating Skills
**Need scripts/ + templates/ + references/**

These skills create files in outputs/:

1. **dev-specify** - Creates spec.md ✅ (already has infrastructure)
2. **dev-plan** - Creates plan.md
3. **dev-tasks** - Creates tasks.md
4. **dev-constitution-builder** - Creates constitution.md
5. **dev-checklist** - Creates checklists/*.md

**Migration steps:**
- Create workspace/skills/[skill-name]/ structure
- Create scripts/create-[artifact].sh (based on prod-user-stories pattern)
- Create templates/[artifact]-template.md
- Create references/ with reference.md, examples.md, README.md
- Update SKILL.md if paths need changing

### Category 2: Workflow Skills
**Need only references/**

These skills guide process but don't create artifacts:

1. **dev-implement** - Executes tasks with TDD workflow
2. **dev-analyze** - Analyzes codebase
3. **dev-clarify** - Clarification dialogue
4. **dev-taskstoissues** - Converts tasks to GitHub issues
5. **dev-constitution** - Uses existing constitution
6. **dev-requesting-code-review** - Git/GitHub workflow
7. **dev-receiving-code-review** - Code review process
8. **dev-finishing-a-development-branch** - Git workflow
9. **dev-using-git-worktrees** - Git worktrees guide
10. **dev-systematic-debugging** - Debugging methodology
11. **dev-test-driven-development** - TDD methodology
12. **dev-verification-before-completion** - Verification checklist
13. **dev-dispatching-parallel-agents** - Agent orchestration
14. **dev-subagent-driven-development** - Agent patterns
15. **dev-writing-plans** - Guide for writing plans
16. **dev-writing-skills** - Guide for writing skills

**Migration steps:**
- Create workspace/skills/[skill-name]/references/
- Create references/reference.md (extended guidance)
- Create references/examples.md (concrete examples)
- Create references/README.md (explains folder)
- Keep SKILL.md as-is (minimal path changes)

## Execution Plan

### Phase 1: Migrate dev-specify (Already has infrastructure) ✅ PRIORITY

**Why first:** Has existing scripts/templates to migrate, sets pattern for other artifact skills

**Steps:**
1. Create install/workspace/skills/dev-specify/
2. Move scripts/ → workspace/skills/dev-specify/scripts/
3. Move templates/ → workspace/skills/dev-specify/templates/
4. Create references/ directory
5. Move reference.md → references/reference.md
6. Create references/examples.md
7. Create references/README.md
8. Update scripts to source common.sh (like prod skills)
9. Create outputs/ directory
10. Update SKILL.md paths if needed

### Phase 2: Migrate Core Pipeline Skills (Artifact-generating)

**Order:** dev-plan → dev-tasks → dev-constitution-builder → dev-checklist

For each:
1. Create workspace/skills/[skill-name]/ structure
2. Extract template content from SKILL.md (if embedded)
3. Create scripts/create-[artifact].sh (based on prod pattern)
4. Create templates/[artifact]-template.md
5. Create references/reference.md (extract from SKILL.md)
6. Create references/examples.md (add concrete examples)
7. Create references/README.md
8. Update SKILL.md to reference new locations

### Phase 3: Migrate Workflow Skills (References-only)

**Batch process all 15 workflow skills**

For each:
1. Create workspace/skills/[skill-name]/references/
2. Extract extended content from SKILL.md → references/reference.md
3. Create references/examples.md with examples
4. Create references/README.md
5. Update SKILL.md to reference extended docs

## Reference Pattern

### references/reference.md
Extended guidance, frameworks, best practices (2000-5000 words)

### references/examples.md
3-5 concrete examples for different contexts/scenarios

### references/README.md
```markdown
# [Skill Name] - Extended References

This folder contains extended documentation for the [skill-name] skill.

## Files in This Folder

- **reference.md** - [Description of what's in reference.md]
- **examples.md** - [Description of examples]

## Adding Your Own References

Feel free to add:
- PDFs from research
- Links to articles
- Notes from team discussions
- Custom templates or variations

Claude will read all files in this folder when running the skill.
```

## Script Pattern (for artifact-generating skills)

Based on prod-user-stories/scripts/create-user-stories.sh:

```bash
#!/usr/bin/env bash
# create-[artifact].sh - Create or update [artifact]
# Part of shipkit dev-[skill-name] skill

set -e

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# Get skill directory
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$SKILL_DIR/outputs"
TEMPLATE_DIR="$SKILL_DIR/templates"

# Parse flags (--update, --archive, --skip-prereqs, --cancel)
UPDATE=false
ARCHIVE=false
SKIP_PREREQS=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --update) UPDATE=true; shift ;;
    --archive) ARCHIVE=true; shift ;;
    --skip-prereqs) SKIP_PREREQS=true; shift ;;
    --cancel) echo "Cancelled."; exit 0 ;;
    --help|-h)
      echo "Usage: $0 [--update|--archive|--skip-prereqs|--cancel]"
      exit 0
      ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

# Check prerequisites
check_skill_prerequisites "dev-[skill-name]" "$SKIP_PREREQS"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Output file location
OUTPUT_FILE="$OUTPUT_DIR/[artifact].md"

# Check if file exists and handle decision
check_output_exists "$OUTPUT_FILE" "[Artifact Name]" "$UPDATE" "$ARCHIVE"

# Check if template exists
TEMPLATE_FILE="$TEMPLATE_DIR/[artifact]-template.md"
if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo "✗ Template not found: $TEMPLATE_FILE"
  exit 1
fi

echo "✓ Template available: $TEMPLATE_FILE"
echo "Output file: $OUTPUT_FILE"
echo ""
echo "Ready for Claude to create [artifact] via dialogue"

exit 0
```

## Success Criteria

For each migrated skill:
- [ ] SKILL.md exists in install/skills/[skill-name]/
- [ ] references/ exists with reference.md, examples.md, README.md
- [ ] (If artifact skill) scripts/ and templates/ exist
- [ ] (If artifact skill) Script sources common.sh
- [ ] (If artifact skill) Script follows flag pattern (--update, --archive, etc.)
- [ ] references/reference.md has extended content (2000+ words)
- [ ] references/examples.md has 3+ concrete examples
- [ ] All paths in SKILL.md are correct

## Validation

After migration:
1. Test install.sh creates correct structure
2. Verify all 20 dev skills follow new pattern
3. Test prerequisite chain works via common.sh
4. Update RESTRUCTURING-PLAN.md with progress

## Notes

- **Don't rewrite content** - Just restructure existing content into new locations
- **Follow prod-user-stories as reference** - It's the cleanest example
- **Use common.sh utilities** - check_skill_prerequisites, check_output_exists
- **Keep SKILL.md concise** - Move extended content to references/

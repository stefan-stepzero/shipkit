# Shipkit Skill Restructuring Plan

**Status: IN PROGRESS** (Updated 2025-12-21)

## Goal

Shift to hybrid architecture with protected outputs:
- **Skill definitions** → `.claude/skills/[skill-name]/SKILL.md`
- **Skill implementation** → `.shipkit/skills/[skill-name]/` (scripts, templates, references, outputs)
- **Shared utilities** → `.shipkit/scripts/bash/common.sh` (sourced by skills)
- **File protections** → `settings.json` denies direct writes to skill outputs/templates/scripts
- **Session enforcement** → `shipkit-master` meta-skill loaded at startup

---

## Completed Skills ✅

### Meta Skills (1)
- ✅ **shipkit-master** - Session-start enforcement (skill usage discipline)

### Prodkit Skills (9)
- ✅ **prod-strategic-thinking** - Business canvas with 4 sections
- ✅ **prod-constitution-builder** - Context-based product principles (POC/MVP/Established × B2C/B2B)
- ✅ **prod-personas** - User personas with integrated empathy mapping
- ✅ **prod-jobs-to-be-done** - JTBD framework with forces diagram
- ✅ **prod-market-analysis** - Competitive landscape analysis
- ✅ **prod-brand-guidelines** - Brand personality, voice, tone, and visual direction
- ✅ **prod-interaction-design** - User journeys (7 stages), interaction patterns, screen flows
- ✅ **prod-user-stories** - INVEST stories with Given-When-Then acceptance criteria, MoSCoW prioritization
- ✅ **prod-communicator** - Stakeholder communications (5 templates: investor/exec/team/customer/board)

**Structure per skill:**
```
.shipkit/skills/prod-[name]/
├── scripts/
│   └── create-[artifact].sh       # Sources common.sh
├── templates/
│   └── [artifact]-template.md     # Single adaptive template
├── references/
│   ├── reference.md               # Extended guidance
│   ├── examples.md                # Concrete examples
│   └── README.md                  # Explains folder
└── outputs/
    └── [artifact].md              # Protected (read-only)
```

---

## Remaining Prod Skills 🔜 (3)

### Sequential Workflow Skills
1. **prod-assumptions-and-risks**
   - Strategic assumptions and risk mitigation
   - Templates: assumptions-risks-template.md

2. **prod-success-metrics**
   - KPIs, success criteria
   - Templates: success-definition-template.md

### Async Skills
3. **prod-trade-off-analysis**
   - Feature prioritization, ROI analysis
   - Templates: tradeoff-matrix-template.md

---

## Dev Skills (Status: NOT STARTED)

All dev skills need restructuring to match new architecture.

### Core Dev Skills
- dev-constitution-builder
- dev-specify
- dev-plan
- dev-tasks
- dev-implement (integrates TDD, reviews, verification)

### Supporting Dev Skills
- dev-analyze
- dev-checklist
- dev-clarify
- dev-taskstoissues
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

### Any (Cross-Cutting) Skills
- any-brainstorming (can interrupt any workflow)

---

## Architecture Decisions

### 1. Single Adaptive Templates
- ✅ One template per skill (not lite/full variants)
- ✅ Templates adapt based on context questions (POC/MVP/Established, B2C/B2B)
- ✅ Sections marked "Deferred" when not applicable

### 2. References Subfolder
- ✅ `references/` folder within each skill
- ✅ Contains reference.md, examples.md, README.md
- ✅ Users can add PDFs, research, custom docs
- ✅ Claude reads all files in references/ when running skill

### 3. Protected Outputs
- ✅ `settings.json` denies writes to `.shipkit/skills/*/outputs/**`
- ✅ Also protects templates/ and scripts/
- ✅ Only skill scripts can modify outputs
- ✅ Forces workflow discipline

### 4. Session Hooks
- ✅ SessionStart hook loads shipkit-master enforcement
- ✅ SkillComplete hooks prompt for next steps (e.g., /prod-communicator after prod skills)
- ✅ Constitution reminders after strategic-thinking

### 5. Shared Utilities
Keep in `.shipkit/scripts/bash/`:
- `common.sh` - Shared functions (sourced by all skills)
- `check-prerequisites.sh` - Validates prereqs (called by skills)
- `update-agent-context.sh` - Updates agent context

---

## File Locations

### Before Restructuring
```
skills/prodkit/sequential/1-strategic-thinking.md
prodkit-files/scripts/bash/create-strategy.sh
prodkit-files/templates/structure/strategy/business-canvas.template.md
```

### After Restructuring
```
.claude/skills/prod-strategic-thinking/SKILL.md
.shipkit/skills/prod-strategic-thinking/
  ├── scripts/create-strategy.sh
  ├── templates/business-canvas-template.md
  ├── references/
  │   ├── reference.md
  │   ├── examples.md
  │   └── README.md
  └── outputs/business-canvas.md (PROTECTED)
```

---

## Remaining Tasks

### Immediate (Current Sprint)
- [ ] Create 3 remaining prod skill packages
- [ ] Update all SKILL.md frontmatter paths to reference new locations
- [ ] Update installer to copy new structure

### Next Sprint
- [ ] Restructure all dev skills
- [ ] Restructure any-brainstorming skill
- [ ] Create missing agent personas (if needed)

### Final
- [ ] Test full installation workflow
- [ ] Validate skill chains work end-to-end
- [ ] Verify session hooks trigger correctly
- [ ] Test file protections prevent direct edits

---

## Progress Tracker

**Prod Skills:** 9/12 complete (75%)
- ✅ strategic-thinking
- ✅ constitution-builder
- ✅ personas
- ✅ jobs-to-be-done
- ✅ market-analysis
- ✅ brand-guidelines
- ✅ interaction-design
- ✅ communicator (async)
- ✅ user-stories
- ⏳ assumptions-and-risks (NEXT)
- ⏳ success-metrics
- ⏳ trade-off-analysis (async)

**Dev Skills:** 0/16 complete (0%)

**Meta Skills:** 1/1 complete (100%)
- ✅ shipkit-master

**Overall:** 10/29 skills complete (34%)

---

## Reference: Skill Package Checklist

For each new skill package, create:

1. **Directory structure**
   ```bash
   mkdir -p skill-name/{scripts,templates,references,outputs}
   ```

2. **Script (scripts/create-[artifact].sh)**
   - Sources `.shipkit/scripts/bash/common.sh`
   - Creates/updates `outputs/[artifact].md`
   - Handles existing file (update/archive/cancel)
   - References templates and references folders

3. **Template (templates/[artifact]-template.md)**
   - Single adaptive template
   - Supports context variations (POC/MVP/Established, B2C/B2B)
   - Sections can be marked "Deferred"

4. **References folder (references/)**
   - `reference.md` - Extended guidance, frameworks, best practices
   - `examples.md` - Concrete examples for different contexts
   - `README.md` - Explains folder, invites user additions

5. **Outputs folder (outputs/)**
   - Created by script on first run
   - Protected by settings.json (read-only)

---

**Template Reference:** Use `prod-personas` as the cleanest example package.

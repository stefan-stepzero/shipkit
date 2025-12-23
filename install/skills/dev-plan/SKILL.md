---
name: dev-plan
description: Transform feature specifications into comprehensive technical designs including data models, API contracts, and implementation strategies with constitution-driven architecture. Use when the user asks to "plan", "design architecture", "create technical design", or "how should we implement" after a spec is created.
triggers:
  - "Create implementation plan"
  - "Design the architecture"
  - "Plan how to build"
  - "Technical design"
handoffs:
  - label: Create Tasks
    skill: dev-tasks
    prompt: Break the plan into dependency-ordered tasks
    send: true
  - label: Create Checklist (optional)
    skill: dev-checklist
    prompt: Generate acceptance test checklist
    send: false
---

# dev-plan - Implementation Planning

**Purpose**: Transform feature specifications into comprehensive technical designs that guide implementation while respecting architectural standards.

---

## When to Invoke

**After**:
- `/dev-specify` has created `spec.md` for the feature
- `/dev-constitution` has established technical standards (recommended)

**User triggers**:
- "Create implementation plan for specs/1-feature-name"
- "Plan how to build this feature"
- "Design the technical architecture"
- "How should we implement this?"

---

## Prerequisites

**Required**:
- Feature specification exists: `.shipkit/skills/dev-specify/outputs/specs/N-feature-name/spec.md`

**Recommended**:
- Technical constitution exists: `.shipkit/skills/dev-constitution/outputs/constitution.md`

**Check**: Script will validate spec exists, warn if constitution missing

---

## What This Skill Creates

**Output location**: `.shipkit/skills/dev-plan/outputs/specs/N-feature-name/`

**Artifacts generated**:
1. **plan.md** - High-level technical blueprint
2. **research.md** - Technical research and decisions (Phase 0)
3. **data-model.md** - Entities, relationships, indexes (Phase 1)
4. **contracts/** - API definitions (OpenAPI/GraphQL schemas)
5. **quickstart.md** - How to build, run, and test
6. **checklist.md** - Acceptance criteria (optional, with `--with-checklist`)

---

## Agent Persona

**Primary**: Architect Agent
- **Mindset**: Systematic, thorough, considers trade-offs
- **Approach**: Decompose problems, explicit dependencies, proven patterns
- **Values**: Constitution alignment, research-driven decisions

**For Phase 0 Research**: Also adopt Researcher Agent
- **Mindset**: Curious, skeptical, evidence-based
- **Approach**: Cross-reference sources, cite findings, test assumptions
- **Values**: Don't guess, investigate thoroughly

---

## How to Invoke

```bash
# From repository root
.shipkit/skills/dev-plan/scripts/create-plan.sh specs/1-user-authentication

# With optional checklist
.shipkit/skills/dev-plan/scripts/create-plan.sh specs/1-user-authentication --with-checklist

# Update existing plan
.shipkit/skills/dev-plan/scripts/create-plan.sh specs/1-user-authentication --update

# Archive old plan and create new
.shipkit/skills/dev-plan/scripts/create-plan.sh specs/1-user-authentication --archive
```

---

## Execution Process

### Step 1: Setup & Validation

**Script runs** (`.shipkit/skills/dev-plan/scripts/create-plan.sh`):
1. Validates spec path format: `specs/N-feature-name`
2. Checks spec.md exists
3. Checks constitution.md exists (warns if missing)
4. Creates output directory structure
5. Reports paths to Claude

**Claude receives**:
- Spec file path
- Constitution file path (if exists)
- Template paths (plan, data-model, research, contract)
- Reference paths (reference.md, examples.md)
- Output file paths

### Step 2: Read References

Read all files in the skill's references directory:
```bash
.shipkit/skills/dev-plan/references/
```

**If >2 files exist:** Ask the user which files are most relevant for this task.

This includes built-in guidance (reference.md, examples.md) and any user-added files (PDFs, research, notes).

---

### Step 3: Read Context

**Read these files to understand requirements and constraints**:

1. **Templates** (structures to fill):
   - `templates/plan-template.md`
   - `templates/data-model-template.md`
   - `templates/research-template.md`
   - `templates/contract-template.yaml`
   - `templates/checklist-template.md` (if --with-checklist)

2. **Input artifacts**:
   - `specs/N-feature-name/spec.md` (feature requirements)
   - `.shipkit/skills/dev-constitution/outputs/constitution.md` (technical standards)

### Step 4: Constitution Check (Pre-Design)

**Before any technical decisions**:

1. **Read constitution thoroughly**:
   - Approved technology stack
   - Architectural patterns
   - Coding standards
   - Testing requirements
   - Performance targets
   - Security standards

2. **Validate spec alignment**:
   - Do requirements fit existing patterns?
   - Are there conflicts with constitution?
   - What constraints apply?

3. **Document alignment in plan.md**:
   ```markdown
   ## Constitution Check

   ### Alignment with Standards
   - [x] Architectural patterns
   - [x] Technology stack
   - [x] Coding standards
   - [x] Testing requirements
   - [x] API conventions
   - [x] Performance requirements
   - [x] Security standards

   ### Violations & Justifications
   | Rule | Violation | Why Needed | Alternative Rejected |
   |------|-----------|------------|---------------------|
   | ... | ... | ... | ... |
   ```

### Step 4: Phase 0 - Research & Unknowns

**Goal**: Resolve all "NEEDS CLARIFICATION" before design

**See** [reference.md](references/reference.md#research-phase) for complete research process

**Process**:
1. Scan Technical Context for unknowns
2. Web search for documentation, best practices, benchmarks
3. Document all decisions with rationale in research.md
4. Update Technical Context with concrete answers

**Output**: `research.md` with all unknowns resolved

### Step 5: Phase 1 - Design & Contracts

**Prerequisites**: research.md complete (no NEEDS CLARIFICATION)

**See** [reference.md](references/reference.md#design-phase) for detailed guidance

**Create**:
1. **Data Model** (`data-model.md`): Entities, fields, relationships, indexes
2. **API Contracts** (`contracts/`): OpenAPI or GraphQL specs
3. **Quickstart Guide** (`quickstart.md`): How to build, run, test
4. **Plan Document** (`plan.md`): High-level technical blueprint

### Step 6: Constitution Check (Post-Design)

**Re-validate plan against constitution**:
1. Review all decisions for alignment
2. Update Constitution Check section
3. ERROR if critical violations without justification

### Step 7: Report Completion

**Output to user**:
```
✅ Implementation plan complete

📁 Created artifacts:
  • Plan: .shipkit/skills/dev-plan/outputs/specs/1-feature-name/plan.md
  • Research: .../research.md
  • Data Model: .../data-model.md
  • Contracts: .../contracts/
  • Quickstart: .../quickstart.md
  [• Checklist: .../checklist.md] (if --with-checklist)

🔍 Constitution check: PASSED
  • All requirements aligned with technical standards
  [• X violations documented with justification] (if violations)

👉 Next step: /dev-tasks specs/1-feature-name
   Break this plan into dependency-ordered tasks

Proceed with /dev-tasks?
```

---

## Key Principles

**The Iron Law**:
```
READ CONSTITUTION BEFORE EVERY TECHNICAL DECISION
```

**Constitution-Driven Design**:
- Technology choices must align with approved stack
- Architectural patterns must follow established conventions
- Security standards must meet constitution requirements
- Testing requirements must match constitution targets
- Violations require explicit justification

**Research First**:
- Don't guess unknowns - research them
- Document sources and evidence
- Compare multiple options
- Never say "we'll figure it out later"

**See** [reference.md](references/reference.md) for:
- Detailed constitution integration patterns
- Complete research phase workflow
- Design phase step-by-step guidance
- Error handling procedures
- Common pitfalls and solutions

---

## Flags & Options

- `--with-checklist` - Include acceptance test checklist
- `--update` - Update existing plan (preserves with backup)
- `--archive` - Archive current plan and start fresh
- `--skip-prereqs` - Skip prerequisite checks (dangerous)

---

## Handoff to dev-tasks

**After planning complete**, run:
```bash
/dev-tasks specs/N-feature-name
```

**dev-tasks will**:
- Read plan.md, spec.md, constitution.md
- Generate dependency-ordered task breakdown
- Include TDD test tasks before implementation
- Mark parallel vs sequential execution
- Output: tasks.md

---

## Success Criteria

Plan is complete when:
- [ ] All "NEEDS CLARIFICATION" resolved
- [ ] Constitution check passed (or violations justified)
- [ ] Technical decisions documented with rationale
- [ ] Data model defined (entities, relationships, indexes)
- [ ] API contracts created (OpenAPI/GraphQL)
- [ ] Security considerations addressed
- [ ] Performance targets defined
- [ ] Testing strategy planned
- [ ] Deployment steps documented
- [ ] Quickstart guide created
- [ ] All artifacts reference spec and constitution

---

**For detailed guidance**, see:
- [reference.md](references/reference.md) - Complete planning process
- [examples.md](references/examples.md) - Real-world examples
- [README.md](references/README.md) - Reference folder guide

**Remember**: Time invested in thorough planning saves time during implementation. A great plan sets up great execution.

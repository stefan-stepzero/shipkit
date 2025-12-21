# Dev Skills Implementation Plan

**Updated:** 2025-12-21
**Status:** Ready for implementation

---

## Key Clarifications

1. **dev-specify script behavior:** Script creates structure from template, Claude fills conversationally (like prod skills)
2. **dev-implement orchestration:** RED-GREEN-REFACTOR is enforced via SKILL.md instructions, not script orchestration
   - 🔴 RED = Write failing test first
   - 🟢 GREEN = Write minimal code to pass
   - 🔵 REFACTOR = Clean up while tests pass
3. **Output locations:** ALL dev skill outputs under `.shipkit/skills/dev-*/outputs/` (matching prod skills)
4. **Spec versioning:** Auto-archiving when `--update` flag used (like prod skills)

---

## Scripting Strategy

### Category A: FULLY Script-Driven (Generate Artifacts)

These skills **MUST** use scripts to extract/transform data and generate outputs:

1. **dev-constitution** - Extracts from product artifacts
2. **dev-specify** - Extracts from user-stories, interaction-design, brand-guidelines
3. **dev-plan** - Analyzes spec.md and generates technical design
4. **dev-tasks** - Parses spec+plan and generates dependency-ordered tasks

### Category B: Script-Assisted (Interactive with Script Support)

5. **dev-implement** - TDD workflow orchestration
6. **dev-finish** - Merge workflow execution

### Category C: Minimally Scripted (Primarily Interactive)

7. **dev-worktree** - Git worktree wrapper
8. **dev-parallel** - Agent dispatch orchestration
9. **dev-debug** - Investigation process (guidance only)
10. **dev-write-skill** - Meta-authoring (guidance only)

---

## Skill Structures (Following Product Skill Schema)

### 1. dev-constitution (FULL - Script-Driven)

```
install/
├── skills/
│   └── dev-constitution/
│       └── SKILL.md                                    # Skill definition
└── workspace/
    └── skills/
        └── dev-constitution/
            ├── scripts/
            │   └── create-constitution.sh              # Extracts from prod outputs
            ├── templates/
            │   └── constitution-template.md            # Technical standards template
            ├── references/
            │   ├── reference.md                        # Standards guidance
            │   ├── examples.md                         # Example constitutions
            │   └── README.md                           # Folder explanation
            └── outputs/
                └── constitution.md                     # PROTECTED
```

**Script Behavior:**
```bash
create-constitution.sh --create
```
- Reads: `.shipkit/skills/prod-user-stories/outputs/user-stories.md`
- Reads: `.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md`
- Reads: `.shipkit/skills/prod-success-metrics/outputs/success-metrics.md`
- Extracts: Tech stack hints, quality standards, constraints
- Generates: `outputs/constitution.md` with technical standards

**Flags:**
- `--create` - Initial constitution from product artifacts
- `--update` - Modify existing with versioning
- `--archive` - Archive current, create new version
- `--skip-prereqs` - Skip prerequisite checks
- `--cancel` - Cancel operation

---

### 2. dev-specify (FULL - Script-Driven) ⭐ UPDATED

```
install/
├── skills/
│   └── dev-specify/
│       └── SKILL.md                                    # Skill definition
└── workspace/
    └── skills/
        └── dev-specify/
            ├── scripts/
            │   └── create-spec.sh                      # Extracts from prod outputs
            ├── templates/
            │   └── spec-template.md                    # Feature spec structure
            ├── references/
            │   ├── reference.md                        # Specification guidance
            │   ├── examples.md                         # Example specs
            │   └── README.md                           # Folder explanation
            └── outputs/
                └── specs/
                    └── N-feature-name/
                        └── spec.md                     # PROTECTED
```

**Script Behavior:**
```bash
create-spec.sh "Add user authentication"
```
- Creates: `outputs/specs/1-user-authentication/spec.md` structure from template
- Reads (for Claude context):
  - `.shipkit/skills/prod-user-stories/outputs/user-stories.md`
  - `.shipkit/skills/prod-interaction-design/outputs/interaction-design.md`
  - `.shipkit/skills/prod-brand-guidelines/outputs/brand-guidelines.md`
  - `.shipkit/skills/dev-constitution/outputs/constitution.md`
- Outputs: Template path and spec path for Claude
- **Claude fills spec via dialogue**, extracting relevant info from product artifacts

**Flags:**
- `--clarify` - Re-run to resolve [NEEDS_CLARIFICATION] markers (interactive)
- `--update` - Update existing spec (archives old version automatically)
- `--skip-prereqs` - Skip prerequisite checks
- `--cancel` - Cancel operation

**Process:**
1. User runs: `/dev-specify "Add user authentication"`
2. Script creates `specs/1-user-authentication/` directory and empty spec.md from template
3. Script tells Claude where the template and product artifacts are
4. Claude reads template + product artifacts, asks user questions, fills spec.md conversationally
5. If user later runs: `/dev-specify --update` on same spec
6. Script auto-archives old spec to `specs/1-user-authentication/spec-YYYYMMDD-HHMMSS.md.bak`
7. Claude updates spec.md with new information

**Key Similarity to prod skills:**
- Script creates structure only
- Claude fills content conversationally
- Spec is PROTECTED after creation (update via --update with auto-archiving)

---

### 3. dev-plan (FULL - Script-Driven)

```
install/
├── skills/
│   └── dev-plan/
│       └── SKILL.md                                    # Skill definition
└── workspace/
    └── skills/
        └── dev-plan/
            ├── scripts/
            │   └── create-plan.sh                      # Generates plan artifacts
            ├── templates/
            │   ├── plan-template.md
            │   ├── data-model-template.md
            │   ├── research-template.md
            │   └── contract-template.yaml
            ├── references/
            │   ├── reference.md                        # Architecture guidance
            │   ├── examples.md                         # Example plans
            │   └── README.md                           # Folder explanation
            └── outputs/
                └── specs/
                    └── N-feature-name/
                        ├── plan.md                     # PROTECTED
                        ├── data-model.md               # PROTECTED
                        ├── research.md                 # PROTECTED
                        ├── checklist.md                # PROTECTED (optional)
                        └── contracts/                  # PROTECTED
                            └── auth-api.yaml
```

**Script Behavior:**
```bash
create-plan.sh specs/1-user-authentication
```
- Reads: `specs/1-user-authentication/spec.md`
- Reads: `.shipkit/skills/dev-constitution/outputs/constitution.md`
- Analyzes: Feature requirements, technical constraints
- Generates: All plan artifacts (plan, data model, contracts, research)

**Flags:**
- `--with-checklist` - Include acceptance test checklist
- `--update` - Update existing plan
- `--archive` - Archive current, create new version
- `--skip-prereqs` - Skip prerequisite checks
- `--cancel` - Cancel operation

---

### 4. dev-tasks (FULL - Script-Driven)

```
install/
├── skills/
│   └── dev-tasks/
│       └── SKILL.md                                    # Skill definition
└── workspace/
    └── skills/
        └── dev-tasks/
            ├── scripts/
            │   └── create-tasks.sh                     # Dependency graph generator
            ├── templates/
            │   └── tasks-template.md                   # Task format structure
            ├── references/
            │   ├── reference.md                        # Dependency ordering rules
            │   ├── examples.md                         # Example task breakdowns
            │   └── README.md                           # Folder explanation
            └── outputs/
                └── specs/
                    └── N-feature-name/
                        └── tasks.md                    # PROTECTED
```

**Script Behavior:**
```bash
create-tasks.sh specs/1-user-authentication
```
- Reads: `specs/1-user-authentication/spec.md`
- Reads: `specs/1-user-authentication/plan.md`
- Reads: `.shipkit/skills/dev-constitution/outputs/constitution.md`
- Validates: Spec/plan consistency
- Analyzes: Dependencies between components
- Generates: `tasks.md` with dependency-ordered implementation tasks

**Flags:**
- `--update` - Regenerate tasks (if spec/plan changed)
- `--archive` - Archive current, create new version
- `--skip-prereqs` - Skip prerequisite checks
- `--cancel` - Cancel operation

---

### 5. dev-implement (Script-Assisted)

```
install/
├── skills/
│   └── dev-implement/
│       └── SKILL.md                                    # Skill definition
└── workspace/
    └── skills/
        └── dev-implement/
            ├── scripts/
            │   ├── start-implementation.sh             # Mode selection + task tracking
            │   └── verify-task.sh                      # Evidence-based completion
            ├── templates/
            │   └── task-completion-checklist.md
            └── references/
                ├── tdd-reference.md                    # RED-GREEN-REFACTOR cycle
                ├── verification-reference.md           # Evidence requirements
                ├── debugging-reference.md              # Root cause debugging
                └── README.md                           # Folder explanation
```

**Script Behavior:**
```bash
start-implementation.sh .shipkit/skills/dev-tasks/outputs/specs/1-user-authentication
```
- Reads: `.shipkit/skills/dev-tasks/outputs/specs/1-user-authentication/tasks.md`
- Counts tasks: 1-5 = direct mode, 6+ = subagent mode
- Tracks: Current task progress
- **TDD enforcement is via SKILL.md guidance, not script orchestration**

**Flags:**
- `--mode=direct` - Force direct mode (single context)
- `--mode=subagent` - Force subagent mode (fresh context per task)

**TDD Cycle (RED-GREEN-REFACTOR) - Enforced by SKILL.md:**

The script doesn't orchestrate TDD; instead, the SKILL.md instructs Claude to follow this cycle:

1. **🔴 RED** - Write a failing test first
   - Write test that describes desired behavior
   - Run test → it should FAIL (proving test works)
   - Never write production code before the test

2. **🟢 GREEN** - Write minimal code to pass
   - Write simplest code that makes test pass
   - No extra features, no premature optimization
   - Run test → it should PASS

3. **🔵 REFACTOR** - Clean up while keeping tests passing
   - Improve code structure
   - Remove duplication
   - Run tests → they should STILL PASS

This cycle repeats for each task. The SKILL.md enforces this discipline through instructions.

**Notes:**
- No protected outputs (code goes in project, not .shipkit/)
- Script handles mode selection and task tracking
- SKILL.md enforces TDD discipline through instructions

---

### 6. dev-finish (Script-Assisted)

```
install/
├── skills/
│   └── dev-finish/
│       └── SKILL.md                                    # Skill definition
└── workspace/
    └── skills/
        └── dev-finish/
            ├── scripts/
            │   ├── check-readiness.sh                  # Test validation
            │   └── merge-branch.sh                     # Merge execution
            └── references/
                ├── reference.md                        # Merge workflows
                └── README.md                           # Folder explanation
```

**Script Behavior:**
```bash
check-readiness.sh
```
- Runs: All tests
- Checks: Git status
- Validates: No uncommitted changes
- Presents: Merge options (merge/keep/discard)

```bash
merge-branch.sh --option=1  # Merge to main
```
- Executes: Git merge workflow
- Cleans up: Branch (if requested)

**Flags:**
- `--option=1` - Merge to main locally
- `--option=2` - Keep branch as-is
- `--option=3` - Discard branch

---

### 7. dev-worktree (Minimal)

```
install/
├── skills/
│   └── dev-worktree/
│       └── SKILL.md                                    # Skill definition
└── workspace/
    └── skills/
        └── dev-worktree/
            ├── scripts/
            │   └── create-worktree.sh                  # Git worktree wrapper
            └── references/
                ├── reference.md                        # Worktree guidance
                └── README.md                           # Folder explanation
```

**Script Behavior:**
```bash
create-worktree.sh feature-name
```
- Validates: .gitignore safety
- Creates: `git worktree add ../project-feature-name`

---

### 8. dev-parallel (Minimal)

```
install/
├── skills/
│   └── dev-parallel/
│       └── SKILL.md                                    # Skill definition
└── workspace/
    └── skills/
        └── dev-parallel/
            ├── scripts/
            │   └── dispatch-agents.sh                  # Parallel orchestration
            └── references/
                ├── reference.md                        # Parallel patterns
                └── README.md                           # Folder explanation
```

**Script Behavior:**
```bash
dispatch-agents.sh domain1 domain2 domain3
```
- Dispatches: 3+ parallel agents
- Waits: For completion
- Integrates: Results

---

### 9. dev-debug (Minimal - Guidance Only)

```
install/
├── skills/
│   └── dev-debug/
│       └── SKILL.md                                    # Skill definition
└── workspace/
    └── skills/
        └── dev-debug/
            └── references/
                ├── reference.md                        # Systematic debugging
                ├── examples.md                         # Example investigations
                └── README.md                           # Folder explanation
```

**No scripts** - Pure process guidance (Reproduce → Isolate → Root cause → Fix → Verify → Prevent)

---

### 10. dev-write-skill (Minimal - Guidance Only)

```
install/
├── skills/
│   └── dev-write-skill/
│       └── SKILL.md                                    # Skill definition
└── workspace/
    └── skills/
        └── dev-write-skill/
            └── references/
                ├── reference.md                        # TDD for skills
                ├── examples.md                         # Example skills
                └── README.md                           # Folder explanation
```

**No scripts** - Pure authoring guidance (Baseline → Write → Verify → Close loopholes)

---

## common.sh Updates Needed

Add to `SKILL_PREREQUISITES`:
```bash
["dev-constitution"]="prod-user-stories"        # Needs product context
["dev-specify"]="dev-constitution"              # Needs technical standards
["dev-plan"]="dev-specify"                      # Needs feature spec
["dev-tasks"]="dev-plan"                        # Needs technical design
["dev-implement"]="dev-tasks"                   # Needs task breakdown
["dev-finish"]=""                               # Just needs passing tests (runtime check)
["dev-worktree"]=""                             # No prereqs
["dev-parallel"]=""                             # No prereqs
["dev-debug"]=""                                # No prereqs
["dev-write-skill"]=""                          # No prereqs
```

Add to `SKILL_OUTPUT_FILES`:
```bash
["dev-constitution"]="dev-constitution/outputs/constitution.md"
["dev-specify"]="dev-specify/outputs/specs/"    # Multiple spec dirs
["dev-plan"]="dev-plan/outputs/specs/"          # Multiple plan dirs
["dev-tasks"]="dev-tasks/outputs/specs/"        # Multiple task dirs
# dev-implement, dev-finish, etc. don't have .shipkit outputs
```

---

## File Protection (settings.json)

Add to `deny_write`:
```json
{
  "protections": {
    "deny_write": [
      ".shipkit/skills/dev-constitution/outputs/**",
      ".shipkit/skills/dev-constitution/templates/**",
      ".shipkit/skills/dev-constitution/scripts/**",
      ".shipkit/skills/dev-specify/outputs/**",
      ".shipkit/skills/dev-specify/templates/**",
      ".shipkit/skills/dev-specify/scripts/**",
      ".shipkit/skills/dev-plan/outputs/**",
      ".shipkit/skills/dev-plan/templates/**",
      ".shipkit/skills/dev-plan/scripts/**",
      ".shipkit/skills/dev-tasks/outputs/**",
      ".shipkit/skills/dev-tasks/templates/**",
      ".shipkit/skills/dev-tasks/scripts/**"
    ]
  }
}
```

**Why protect:** Constitution, specs, plans, and tasks are generated artifacts. To update, re-run the skill.

**Not protected:** Code from dev-implement (normal development workflow)

---

## Implementation Phases

### Phase 1: Core Pipeline (Script-Heavy)
**Priority:** HIGHEST - These enable the dev workflow

1. ✅ **dev-constitution**
   - Script extracts from prod artifacts
   - Creates technical standards document
   - Consumed by all other dev skills

2. ✅ **dev-specify**
   - Script extracts from user-stories, interaction-design, brand-guidelines
   - Creates feature spec with [NEEDS_CLARIFICATION] markers
   - Supports --clarify for iterative refinement

3. ✅ **dev-plan**
   - Script analyzes spec.md
   - Generates plan.md, data-model.md, contracts/, research.md
   - Optional checklist.md with --with-checklist

4. ✅ **dev-tasks**
   - Script parses spec + plan
   - Validates consistency
   - Generates dependency-ordered tasks.md

### Phase 2: Execution Pipeline
**Priority:** HIGH - Completes the workflow

5. ✅ **dev-implement**
   - Script orchestrates TDD workflow
   - Enforces RED → GREEN → REFACTOR
   - Auto-selects direct vs. subagent mode
   - Integrates verification and debugging

6. ✅ **dev-finish**
   - Script validates test passage
   - Presents merge options
   - Executes chosen workflow

### Phase 3: Supporting Tools
**Priority:** MEDIUM - Useful but not critical

7. ✅ **dev-worktree**
   - Simple git worktree wrapper
   - Validates .gitignore safety

8. ✅ **dev-parallel**
   - Parallel agent dispatcher
   - For 3+ independent failures

### Phase 4: Advanced/Meta
**Priority:** LOW - Can be added later

9. ✅ **dev-debug**
   - Systematic debugging guidance
   - No scripts needed

10. ✅ **dev-write-skill**
    - Skill authoring guidance
    - TDD for process docs

---

## Testing Strategy

For each script-driven skill, validate:

1. **Prerequisite checking** works correctly
2. **File existence handling** (--update, --archive, --cancel)
3. **Extraction accuracy** (reads correct product artifacts)
4. **Template usage** (generates correct structure)
5. **Output protection** (settings.json denies writes)
6. **Error messages** are clear and actionable

Test the full pipeline:
```bash
# After product discovery completed
/dev-constitution --create
/dev-specify "Add user authentication"
/dev-specify --clarify  # (if needed)
/dev-plan
/dev-tasks
/dev-implement
/dev-finish
```

---

## Success Criteria

Each skill must:
- ✅ Follow product skill schema exactly
- ✅ Source `common.sh` for shared utilities
- ✅ Use prerequisite checking
- ✅ Handle existing files (update/archive/cancel)
- ✅ Generate protected outputs (for script-driven skills)
- ✅ Include references/ with reference.md, examples.md, README.md
- ✅ Include templates/ with single adaptive template (for artifact-generating skills)
- ✅ Have clear SKILL.md with purpose, triggers, process, constraints

---

## Next Steps

1. Review this plan
2. Start with Phase 1 (dev-constitution, dev-specify, dev-plan, dev-tasks)
3. Create each skill following the product skill schema
4. Test incrementally
5. Move to Phase 2 when Phase 1 complete

---

**Ready to proceed with implementation?**

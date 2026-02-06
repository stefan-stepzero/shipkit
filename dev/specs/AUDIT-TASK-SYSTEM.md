# Task System Integration Audit

**Status:** Implemented
**Last Updated:** 2026-02-06
**Implementation:** No changes needed - existing design is optimal

## Purpose

Assess whether complex Shipkit skills should leverage Claude Code's new task management system with dependency tracking.

## New Task System Capabilities

| Feature | Description |
|---------|-------------|
| `TaskCreate` | Create tasks with subject, description, activeForm |
| `TaskUpdate` | Update status, set dependencies with addBlockedBy |
| `TaskList` | View all tasks with status |
| `TaskGet` | Get full task details |
| `addBlockedBy` | Set task dependencies |
| `status: deleted` | Delete tasks |
| Persistence | Tasks persist across context compaction |

## Skills to Evaluate

### Complex multi-step skills

#### shipkit-master
**Current behavior:** Lightweight orchestrator that auto-loads at session start. Checks file freshness, loads context efficiently (~400-500 tokens), and routes user requests to appropriate skills via keyword matching. Does NOT write files - purely routing/orchestration.

**Could benefit from tasks?** No

**Rationale:**
- Not multi-step execution - it's a routing layer
- No long-running operations that could benefit from persistence
- No dependencies between steps (routing is instantaneous)
- User doesn't need visual progress for routing
- Context is small (~400 tokens) so compaction is not a concern

---

#### shipkit-plan
**Current behavior:** Transforms feature specs into validated implementation plans through 5+ major steps:
1. Confirm scope (read specs, ask user)
2. UI-heavy gate check
3. Read existing context (stack.md, architecture.md)
4. Anti-pattern check
5. Codebase pattern scan (uses subagent)
6. Generate implementation plan with phases
7. Plan validation gate (6 separate checks)
8. Log decision (optional)
9. Suggest next step

**Could benefit from tasks?** Possibly - Low Priority

**Rationale:**
- **Multiple distinct steps:** Yes (5+ major steps)
- **Dependency tracking:** Moderate value - validation depends on generation, but steps are largely sequential anyway
- **Persistence across compaction:** Low value - planning typically completes in one session
- **Visual progress:** Moderate value - user could see "Scanning codebase patterns" vs "Validating plan"

**Verdict:** The skill already has well-defined steps with clear outputs. Tasks would add visual progress but the overhead of creating/updating tasks may not be worth it. The existing completion checklist serves a similar purpose. **Consider only if users report losing progress during long planning sessions.**

---

#### shipkit-verify
**Current behavior:** Batch verification across 12 quality dimensions:
1. Detect scope (git diff)
2. Expand scope via pattern ripple (uses subagent)
3. Read context (specs, architecture)
4. Work through 12 quality dimensions
5. Generate prioritized report (Critical/Should Fix/Minor)

**Could benefit from tasks?** No

**Rationale:**
- **Multiple distinct steps:** Yes, but they're analytical not actionable
- **Dependency tracking:** Not applicable - this is read-only analysis
- **Persistence across compaction:** Low value - verify is fast, single-session
- **Visual progress:** Low value - user just wants the final report

**Verdict:** This skill is designed to be fast and produce an ephemeral report. Adding task overhead would slow it down without meaningful benefit. The final report is the only artifact that matters.

---

#### shipkit-preflight
**Current behavior:** Comprehensive production readiness audit with incremental capabilities:
1. Determine audit scope (full/incremental/quick-verify)
2. Check prerequisites (routes to other skills if missing)
3. Gap analysis (minimal intake questions)
4. Run audit against checklist (9 categories, uses subagent for parallel checks)
5. Generate audit report with status tracking
6. Save and present (with metadata for future incremental runs)

**Could benefit from tasks?** Possibly - Medium Priority

**Rationale:**
- **Multiple distinct steps:** Yes (6 major steps, 9 checklist categories)
- **Dependency tracking:** Moderate value - checklist categories could run in parallel
- **Persistence across compaction:** Moderate value - full audit on large codebase could be lengthy
- **Visual progress:** High value - user would benefit from seeing "Checking Auth & Security (3/9 categories complete)"

**Considerations:**
- The skill already has good progress tracking via the audit report metadata
- Thorough mode with pr-review-toolkit partitions WOULD benefit from tasks
- Standard mode is usually fast enough that tasks add overhead

**Verdict:** Consider tasks for "thorough mode" only, where partitioned deep reviews could benefit from dependency tracking and progress visualization. Standard preflight is likely fast enough without tasks.

---

#### shipkit-project-context
**Current behavior:** Smart context scanner with caching:
1. Check freshness (compare file modification times)
2. Ask before heavy work (first run vs stale)
3. Scan project files (uses subagent for comprehensive detection)
4. Detect working patterns (provider hierarchy, API patterns, etc.)
5. Generate 3 context files (stack.md, env-requirements.md, schema.md)
6. Confirm completion

**Could benefit from tasks?** No

**Rationale:**
- **Multiple distinct steps:** Yes (5-6 steps)
- **Dependency tracking:** Minimal - steps are naturally sequential
- **Persistence across compaction:** Low value - scanning is fast with caching
- **Visual progress:** Low value - user just wants the final context files

**Verdict:** The skill already has excellent caching (87% token reduction on subsequent runs). The main value is the output files, not progress tracking. Tasks would add overhead without meaningful benefit.

---

### Relentless execution skills

#### shipkit-build-relentlessly
**Current behavior:** Iterative loop until build passes:
1. Parse arguments (task, --max N)
2. Auto-detect build system
3. Create state file (.shipkit/relentless-state.local.md)
4. Loop: Fix errors → Run build → Check promise → Repeat
5. Completion (success or max iterations)

**Could benefit from tasks?** No - Would Conflict

**Rationale:**
- **Multiple distinct steps:** Yes, but it's a loop not a pipeline
- **Dependency tracking:** Not applicable - no parallel work
- **Persistence across compaction:** Already handled by state file
- **Visual progress:** Already handled by hook ("Iteration 3/10")

**Critical Issue:** This skill has its own persistence mechanism (relentless-state.local.md) that drives the stop hook. Introducing tasks would create two competing state systems. The existing mechanism is well-designed for the iterative loop pattern.

**Verdict:** Do NOT add tasks. The existing state file + hook mechanism is purpose-built for this use case. Tasks would add complexity without benefit and potentially conflict with the relentless loop logic.

---

#### shipkit-test-relentlessly
**Current behavior:** Same iterative pattern as build-relentlessly:
1. Parse arguments
2. Auto-detect test framework
3. Create state file
4. Loop: Fix tests → Run tests → Check promise → Repeat
5. Completion

**Could benefit from tasks?** No - Would Conflict

**Rationale:** Same as shipkit-build-relentlessly. Uses identical state file mechanism for loop persistence. Adding tasks would conflict with the relentless stop hook.

**Verdict:** Do NOT add tasks. Keep existing mechanism.

---

#### shipkit-lint-relentlessly
**Current behavior:** Same iterative pattern as the other relentless skills:
1. Parse arguments
2. Auto-detect linter
3. Create state file
4. Loop: Auto-fix → Manual fix → Run lint → Check promise → Repeat
5. Completion

**Could benefit from tasks?** No - Would Conflict

**Rationale:** Same as other relentless skills. Uses identical state file mechanism.

**Verdict:** Do NOT add tasks. Keep existing mechanism.

---

## Analysis

### When tasks add value

Tasks are valuable when:

1. **Multiple independent phases** that could run in parallel or benefit from dependency tracking
2. **Long-running operations** where context compaction is a real risk
3. **User needs visual progress** on complex multi-stage operations
4. **State needs to persist across sessions** (via CLAUDE_CODE_TASK_LIST_ID env var)
5. **Cross-session handoff** is expected (different human picks up where another left off)

### When tasks add overhead

Tasks add overhead without benefit when:

1. **Operations are fast** (complete in one response)
2. **Steps are strictly sequential** with no parallelization opportunity
3. **Skill has its own state management** (like relentless skills)
4. **Output is the only artifact that matters** (like verify)
5. **Simple routing/orchestration** (like master)

---

## Recommendations

### Do NOT Integrate Tasks

| Skill | Reason |
|-------|--------|
| `shipkit-master` | Routing layer, no multi-step execution |
| `shipkit-verify` | Fast analysis, ephemeral output only |
| `shipkit-project-context` | Fast with caching, output files are the value |
| `shipkit-build-relentlessly` | Has purpose-built state file mechanism, would conflict |
| `shipkit-test-relentlessly` | Same - uses relentless state file mechanism |
| `shipkit-lint-relentlessly` | Same - uses relentless state file mechanism |

### Consider for Future (Low Priority)

| Skill | Condition | Why |
|-------|-----------|-----|
| `shipkit-plan` | Only if users report losing progress | Would add visual progress but existing checklist works |
| `shipkit-preflight` | Only for "thorough mode" | Standard mode is fast; thorough mode with partitions could benefit |

### Potential Future Use Cases (Not Current Skills)

Tasks would be valuable for:

1. **Multi-project migrations** - tracking progress across many files/packages
2. **Release orchestration** - version bump, changelog, tag, publish as tracked steps
3. **Large refactoring campaigns** - tracking which files/modules have been updated
4. **Cross-session feature implementations** - where work spans multiple days/people

---

## Implementation Plan

### Immediate Actions

**None required.** Current skills are well-designed for their use cases:
- Fast skills don't need task overhead
- Relentless skills have purpose-built state management
- Routing skills don't do multi-step work

### If Implementing Tasks Later

For `shipkit-preflight` thorough mode (if decided):

```markdown
## Thorough Mode Task Structure

1. TaskCreate: "Preflight: Partition Codebase"
   - Partition codebase into MECE chunks

2. TaskCreate (for each partition):
   - "Preflight: Review [partition-name]"
   - addBlockedBy: partition task

3. TaskCreate: "Preflight: Aggregate Findings"
   - addBlockedBy: all partition review tasks

4. TaskCreate: "Preflight: Generate Report"
   - addBlockedBy: aggregate task
```

For `shipkit-plan` (if decided):

```markdown
## Plan Task Structure

1. TaskCreate: "Plan: Confirm Scope"
2. TaskCreate: "Plan: Scan Codebase Patterns"
   - addBlockedBy: scope confirmation
3. TaskCreate: "Plan: Generate Plan"
   - addBlockedBy: codebase scan
4. TaskCreate: "Plan: Validate"
   - addBlockedBy: plan generation
```

---

## Conclusion

**The current Shipkit skills are well-architected for their purposes.** The task system would add overhead without meaningful benefit for most skills:

- **Routing skills** (master) don't need task tracking
- **Analysis skills** (verify) are fast and produce ephemeral output
- **Context skills** (project-context) have excellent caching
- **Relentless skills** have purpose-built state management that would conflict with tasks

The task system is designed for different use cases than these skills serve. Consider tasks for **future skills** that involve multi-session work, parallel independent phases, or complex orchestration across many components.

**Recommendation: No changes needed to existing skills.**

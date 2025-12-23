---
name: shipkit-status
description: "Efficiently assess project status across all phases and suggest next steps. Use when user asks 'where are we?', 'what's the status?', 'what should I do next?'"
agent: any-researcher
---

# Shipkit Status

## Agent Persona

**Load:** `.claude/agents/any-researcher-agent.md`

Adopt: Analytical, efficient context gatherer, provides clear synthesis and actionable recommendations.

## Purpose

Quickly assess where the project stands across product discovery and development phases, then suggest the most logical next steps. Designed to be **token-efficient** by using Claude Code's native tools to scan filesystem, then reading only what's necessary.

## When to Trigger

User says:
- "Where are we at?"
- "What's the status?"
- "What should I do next?"
- "Show me progress"
- "What have we completed?"

Or explicitly:
- `/shipkit-status`

## Process

### Step 1: Scan for Product Discovery Artifacts

Use Glob to check which product skills have outputs:

```
Glob: .shipkit/skills/prod-*/outputs/**
```

This shows which product skills have been completed without reading content yet.

**Product skills to check:**
- prod-strategic-thinking
- prod-constitution-builder
- prod-personas
- prod-jobs-to-be-done
- prod-market-analysis
- prod-brand-guidelines
- prod-interaction-design
- prod-user-stories
- prod-assumptions-and-risks
- prod-success-metrics

**Token cost:** ~200-500 tokens (just file paths)

---

### Step 2: Scan for Development Artifacts

Use Glob to check dev artifacts:

```
Glob: .shipkit/skills/dev-specify/outputs/**/
Glob: .shipkit/skills/dev-constitution/outputs/**
Glob: .shipkit/skills/dev-roadmap/outputs/**
Glob: .shipkit/skills/dev-progress/outputs/**
```

This shows:
- How many specs exist
- Whether constitution, roadmap, progress exist
- Without reading full content yet

**Token cost:** ~200-500 tokens

---

### Step 3: Check Git Status

Use Bash to get git context:

```bash
git branch --show-current && echo "---" && git status --short && echo "---" && git log --oneline -3
```

This gives you:
- Current branch
- Modified files
- Recent commits

**Token cost:** ~100-200 tokens

---

### Step 4: Selective Deep Reading

Based on what exists, read **only** what's necessary:

**If product discovery is in progress:**
- Read: `.shipkit/skills/prod-constitution-builder/outputs/product-constitution.md` (if exists)
  - Understand project type (POC vs Greenfield affects suggestions)
- Read: Most recent completed product artifact
  - See what was last accomplished
- Scan: `.shipkit/skills/prod-user-stories/outputs/user-stories.md` (if exists)
  - Count features, see scope

**If development is in progress:**
- Read: `.shipkit/skills/dev-constitution/outputs/technical-constitution.md` (if exists)
- Read: `.shipkit/skills/dev-roadmap/outputs/roadmap.md` (if exists)
  - See feature sequencing
- Read: `.shipkit/skills/dev-progress/outputs/progress.md` (if exists)
  - See completion status
- Scan: Most recent spec directory
  - Check if spec.md, plan.md, tasks.md exist

**Token budget:** Keep selective reading under 3000 tokens total.

**Strategy:**
- Use Read with `limit` parameter for large files (read first 100 lines)
- For status, you don't need full artifact content
- Headers and structure tell you what's complete

---

### Step 5: Synthesize Status

Create a clear status snapshot covering:

**Product Discovery Status:**
- What's complete? (✅)
- What's next? (⏭️)
- Project type from constitution (if exists)

**Development Status:**
- How many specs exist?
- Roadmap status (sequenced/not sequenced)
- Current feature being worked on (if any)
- Recent completions

**Git Status:**
- Current branch
- Uncommitted changes
- Recent activity

**Efficiency note:** Present information in structured format (table or list), not prose.

---

### Step 6: Suggest Next Steps

Based on what exists and what's missing, suggest **2-3 logical next actions**:

**Decision logic:**

If no product outputs exist:
```
👉 Start: /prod-strategic-thinking
   Define your business strategy before building.
```

If product discovery incomplete (e.g., stopped at personas):
```
👉 Continue: /prod-jobs-to-be-done
   You've defined personas, now map their workflows.
```

If product complete, no dev work:
```
👉 Transition: /dev-constitution
   Product discovery complete. Define technical standards.
```

If specs exist but no roadmap:
```
👉 Sequence: /dev-roadmap
   You have X specs. Sequence them (foundation → features).
```

If actively implementing (progress.md shows in-progress feature):
```
👉 Continue: /dev-implement for spec-00X
   Current feature: [name]. Complete before moving to next.
```

**Constitution-aware suggestions:**
- POC projects: Suggest faster path, skip optional skills
- Greenfield projects: Suggest comprehensive workflow
- Check project type from constitution if it exists

---

### Step 7: Write Status Snapshot

Write concise status summary to:

```
.shipkit/skills/shipkit-status/outputs/status-snapshot.md
```

**Include:**
- Timestamp
- Current branch
- Project type (from constitution, if exists)
- Product discovery: X/10 complete (table format)
- Development: X specs, roadmap status, current work
- Git: uncommitted changes, recent commits
- Suggested next steps (2-3 options)
- Key blockers (missing prerequisites)

**Format:** Concise markdown (1-2 pages max, use tables)

---

## Outputs

**Status snapshot (timestamped):**
```
.shipkit/skills/shipkit-status/outputs/status-snapshot.md
```

Overwrites each time (keeps latest status only).

---

## Token Efficiency Strategy

**Glob → Git → Selective Read → Synthesize**

1. **Glob for artifacts** - 400-800 tokens (paths only)
2. **Git status** - 100-200 tokens
3. **Selective deep reading** - 2000-3000 tokens (constitution + 1-2 key artifacts)
4. **Synthesis** - 500-1000 tokens

**Total cost:** ~3000-5000 tokens (vs 20k+ if reading everything)

**How we achieve efficiency:**
- Glob shows what exists without reading content
- Git status is concise
- Only read artifacts that matter for current phase
- Use Read with `limit` for large files (first 50-100 lines)
- Skip reading templates/scripts (we know what they are)
- Write structured output (tables, not prose)

---

## Integration with Other Skills

**Called after:**
- Any skill completion (to see what's next)
- Session resume (to understand where you left off)
- Confusion about workflow (to reorient)

**Informs:**
- User about where they are
- What skill to invoke next
- What's blocking progress

**Does NOT replace:**
- `/dev-progress` (that's automated roadmap tracking)
- This is broader: works across all phases

---

## Edge Cases

**Empty project (no .shipkit/ yet):**
- Report: "Shipkit not installed. Run installer first."
- Suggest: Start with `/prod-strategic-thinking` or `/dev-constitution`

**Only product discovery (no dev work):**
- Report: "Product phase: X/10 skills complete"
- Suggest: Next product skill OR transition to dev

**Only dev work (no product discovery):**
- Report: "Development only. No product discovery artifacts."
- Suggest: Continue dev work, optionally backfill product discovery

**Mixed state (some product, some dev):**
- Report both phases
- Suggest logical next step based on completeness

---

## Constraints

**DO:**
- ✅ Use Claude Code's native tools (Glob, Read, Bash)
- ✅ Be token-efficient (scan first, read selectively)
- ✅ Provide clear next steps (2-3 options max)
- ✅ Use Read with `limit` for large files (avoid reading full artifacts)
- ✅ Respect constitution if it exists (POC vs Greenfield affects suggestions)
- ✅ Be honest about gaps (missing prerequisites)

**DON'T:**
- ❌ Read every artifact (wasteful)
- ❌ Read full content when headers suffice
- ❌ Suggest rigid linear chains (be flexible)
- ❌ Assume workflow order (check what exists)
- ❌ Create artifacts for other skills (just report and suggest)

---

## Success Criteria

A good status check:
1. ✅ Completes in <5000 tokens
2. ✅ Accurately identifies current phase
3. ✅ Lists completed artifacts
4. ✅ Suggests 2-3 logical next actions
5. ✅ Accounts for constitution constraints (if exists)
6. ✅ Helps user reorient quickly

---

## Example Workflow

**User:** "Where are we at?"

**Claude:**
1. Glob `.shipkit/skills/prod-*/outputs/**` → Sees 3 product skills complete
2. Glob `.shipkit/skills/dev-*/outputs/**` → Sees 0 dev artifacts
3. Bash git status → On feature/onboarding branch
4. Read constitution → Project type: "Side Project MVP"
5. Synthesize: "Product 3/10 complete (strategic-thinking, constitution, personas). No dev work yet."
6. Suggest: "Next: /prod-jobs-to-be-done (map persona workflows)"
7. Write status snapshot

**Token cost:** ~3500 tokens

---

**This skill is your "where am I?" compass for navigating Shipkit workflows.**

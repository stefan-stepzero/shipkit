# Next Steps

## 1. Mission Control Data Sharing

**Problem:** Mission control currently only sees operational metrics (skill usage counts, tool events). It's blind to actual project substance — goals, architecture, spec status, progress.

**Idea:** Projects push structured state snapshots to mission control, turning it into a visualization layer.

**What gets shared:**
- Architecture decisions (count, staleness, diagram summary)
- Spec status (active/completed/stale)
- Stack overview
- Progress/resume point
- Goals (once the goals skill exists)

**Sync triggers (pick one or combine):**
- `shipkit-update` — natural sync point, already touches the whole project
- Stop hook — automatic, keeps mission control continuously fresh
- Dedicated `shipkit-mission-control sync` command

**Storage:** Extend existing `~/.shipkit-mission-control/codebases/{project}.json` with a `projectState` object alongside current skill usage data.

**Dashboard:** Mission control renders this data — project health at a glance across all codebases.

---

## 2. Goals Skill (`shipkit-goals`)

**Problem:** There's a conceptual gap between `why.md` (vision/constraints) and `specs/` (feature details). Nothing tracks the actual objectives that connect them.

```
why.md (vision) → ??? → specs (features) → plans (implementation)
```

**Idea:** A goals skill that captures structured, trackable objectives with priorities and linked specs.

**Output:** `goals.md` and/or `goals.json` in `.shipkit/`
- Goals with status (active/achieved/deferred)
- Priority ranking
- Links to related specs
- Success criteria
- Machine-readable format for mission control visualization

**Passes the skill value test:**
- Forces human decisions (what are the actual goals, what's the priority, what does success look like)
- Creates persistence (goal tracking across sessions)

**Design decisions to make:**
- Markdown vs JSON vs both (Claude reads markdown, mission control reads JSON)
- How granular — strategic goals only, or also tactical milestones?
- Does mission control become a place to *set* goals, or read-only?

---

## Sequencing

These two features reinforce each other but can be built independently:
- **Goals first** → creates the structured data, then wire it into mission control later
- **Data sharing first** → establishes the pipeline, then goals becomes another data source

**Recommendation:** TBD — decide which delivers standalone value faster.

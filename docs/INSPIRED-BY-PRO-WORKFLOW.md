# Inspired by pro-workflow: Patterns Worth Adopting

**Date:** 2026-02-09
**Source:** https://github.com/rohitg00/pro-workflow
**Status:** Research complete, not yet implemented

---

## Context

pro-workflow is an open-source Claude Code plugin focused on workflow optimization and persistent learning. It implements 10 commands, 3 agents, 8 hook types, and a SQLite+FTS5 learning database. Its core philosophy is the "80/20 AI coding ratio" — 80% written by AI, 20% reviewing and correcting.

Shipkit and pro-workflow solve different problems at different scopes. pro-workflow optimizes the *process* of working with Claude. Shipkit provides a *product development framework* on top of Claude Code. But pro-workflow has patterns worth being inspired by.

This document captures those patterns and proposed adaptations for Shipkit.

---

## Proposed Implementations (Priority Order)

### 1. Post-Edit Security Scanning Hook

**Inspired by:** pro-workflow's `post-edit-check.js` (PostToolUse hook)

**What:** A `PostToolUse` hook on Edit/Write that scans modified files for:
- `console.log/debug/info` (excluding commented lines)
- `print()` in Python (excluding comments)
- TODO/FIXME/XXX/HACK markers
- Hardcoded secrets (`api_key|secret|password|token` with 8+ char values)

Reports up to 5 issues immediately via stderr after each edit.

**Build effort:** One Python script (~50 lines), one hook entry in settings JSON.

**Benefit:** Catches mistakes at the moment of creation, not at review time. Complements `/shipkit-verify` (comprehensive post-hoc review) with real-time feedback. Particularly valuable for catching secrets before they hit git staging.

**Shipkit adaptation:** Keep it lightweight. No database, no state. Just regex scanning on the file that was just edited. Our existing `shipkit-verify` handles the deep review — this is the fast, always-on safety net.

---

### 2. Drift Detection Hook

**Inspired by:** pro-workflow's `drift-detector.js` (UserPromptSubmit hook)

**What:** A `UserPromptSubmit` hook that:
1. On first prompt, saves intent keywords to a temp file
2. On subsequent prompts, compares keyword overlap
3. After 6+ edits with <20% relevance to original intent, logs a warning
4. Resets on explicit "new task" signals ("now let's...", "switch to...", "actually...")

**Build effort:** One Python script (~60 lines), one hook entry.

**Implementation details:**
- Keyword extraction: split on whitespace, filter stopwords, keep words >2 chars
- State: temp file at OS temp dir (`shipkit-intent-{session_id}.json`)
- Relevance: `len(overlap) / len(intent_keywords)`
- Warning threshold: 6+ edits AND relevance < 0.2

**Benefit:** Sessions stay focused. Especially valuable during `/shipkit-build-relentlessly` loops where Claude operates autonomously for extended stretches. Catches the common pattern: "ask about auth → end up refactoring CSS → 40 minutes later realize auth is unfinished."

**Shipkit adaptation:** Gentler than pro-workflow's version. Log to stderr as information, not a block. Let the user decide if the tangent is intentional.

---

### 3. Handoff Enhancement for Work Memory

**Inspired by:** pro-workflow's separation of `/wrap-up` (writer-focused) from `/handoff` (reader-focused)

**What:** Enhance `/shipkit-work-memory` to produce a "Resume Command" — a single copy-paste prompt optimized for loading the next session with full context.

**Current state:** `shipkit-work-memory` writes `.shipkit/progress.json` with resume state, but it's structured data that requires the session hook to parse and surface.

**Proposed addition:** Add a `resumeCommand` field to progress.json that contains a natural-language prompt like:
```
Continue working on feature/auth branch. Last completed: rate limiting middleware.
Next step: add Redis-backed sliding window for IP tracking. Watch out for:
the test suite expects mock Redis, not real connection.
```

**Build effort:** Edit to existing SKILL.md instructions. No new files.

**Benefit:** The difference between writing for yourself (current) vs. writing for your future self (proposed). A purpose-built resume prompt means the next session starts productive immediately without reading through progress.json manually.

---

### 4. Split CLAUDE.md Template

**Inspired by:** pro-workflow's split memory architecture (CLAUDE.md + AGENTS.md + SOUL.md + LEARNED.md)

**What:** Add an optional modular template to `/shipkit-claude-md` for larger projects:
- **CLAUDE.md** — Entry point with project overview and links
- **WORKFLOW.md** — How to work (planning rules, quality gates, delegation patterns)
- **PREFERENCES.md** — Style, tone, communication preferences
- **LEARNED.md** — Auto-populated corrections and project-specific patterns

**Build effort:** Template files + option in existing skill.

**Benefit:** For larger projects, monolithic CLAUDE.md becomes a wall of text that Claude partially ignores. Splitting by concern keeps each file focused and within Claude's effective attention window. Smaller projects keep the simple single-file approach.

**Shipkit adaptation:** Offer as an option during `/shipkit-claude-md`, not as the default. The split only helps projects complex enough to outgrow a single file.

---

### 5. Auto-Memory Integration Audit

**Inspired by:** The gap between Shipkit's `.shipkit/` memory system and Claude Code's built-in auto-memory (`MEMORY.md`)

**What:** Research task — not code. Determine whether Shipkit should integrate with Claude Code's auto-memory system.

**Current state:** Shipkit documents auto-memory in `install/rules/shipkit.md` but no skill reads, writes, or integrates with `~/.claude/projects/<hash>/memory/MEMORY.md`. We have a parallel memory system in `.shipkit/` that's completely independent.

**Questions to answer:**
1. Should `/shipkit-work-memory` write its resume point to MEMORY.md *in addition to* progress.json? Claude loads MEMORY.md automatically — no hook needed.
2. Should `/shipkit-architecture-memory` surface key decisions in MEMORY.md so Claude naturally recalls them?
3. Are we duplicating what auto-memory already captures automatically?
4. Could our session-start hook read MEMORY.md to enrich context with auto-learned patterns?
5. What's the interaction between auto-memory and our `.shipkit/` files — complementary or conflicting?

**Why this matters:** If MEMORY.md is the right place for resume state, it changes how we build #3 (handoff). If auto-memory already captures project patterns, some of our explicit persistence may be redundant. Either way, the answer shapes our memory strategy.

**Build effort:** Research only. Read auto-memory docs, test what it captures, decide integration points.

---

## Patterns We Considered and Skipped

### SQLite Persistent Learning Database
**What pro-workflow does:** SQLite with FTS5 full-text search stores corrections, searchable across sessions and projects. Powers `/search`, `/list`, `/insights`, `/replay`.

**Why we're skipping it:** Heavy infrastructure (SQLite, Node.js build step, better-sqlite3 dependency) for something Claude Code's auto-memory partially handles. Shipkit is a framework that installs into user projects — adding a database layer increases complexity and maintenance burden disproportionately.

**What we'd do instead:** If we want persistent learning, explore using MEMORY.md (always loaded) + additional `.md` files in the memory directory (loaded on demand). File-based, no dependencies, works with Claude Code's existing infrastructure.

### Adaptive Quality Gates
**What pro-workflow does:** Edit checkpoint thresholds adjust based on correction rate history. High error rate = tighter gates.

**Why we're skipping it:** Our relentless execution skills already handle quality loops with their own feedback mechanisms. Adding correction-rate tracking on top adds complexity without clear payoff given our existing architecture.

### Scout Agent (Confidence-Gated Exploration)
**What pro-workflow does:** Scores readiness 0-100 on 5 dimensions before implementation. Blocks at <70.

**Why we're skipping it:** Our planner + architect agents already cover readiness assessment. A formal confidence score adds ceremony. The Scout concept is clever but the benefit over "just run /shipkit-plan first" isn't clear enough to justify a new agent.

### Correction Heatmap / Analytics
**What pro-workflow does:** Tracks which categories get corrected most, visualizes as heatmap, identifies hot/cold learnings.

**Why we're skipping it:** Requires the SQLite database we're not building. The insight is valuable but the infrastructure cost is too high for Shipkit's lightweight approach.

---

## Other Interesting Patterns (Not Prioritized)

### Rotating Reminder Cycling
pro-workflow's Stop hook cycles through 3 different reminder messages every 20 responses instead of repeating the same one. Prevents reminder fatigue. Escalates at 50 responses. Small UX detail, worth keeping in mind for our hooks.

### Contexts (Dev/Review/Research Modes)
Lightweight markdown files that switch Claude's behavior mode. Similar to our agents but simpler — just personality/priority adjustments, not full personas. Could inspire a "mode" concept in Shipkit.

### Model Preferences Per Task Type
Config maps task complexity to model choice (haiku for quick fixes, opus for architecture). We already do this in CLAUDE.md guidance but pro-workflow makes it explicit in config.json.

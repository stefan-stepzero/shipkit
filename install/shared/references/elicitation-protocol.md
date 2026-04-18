# Elicitation Protocol (Return-Prompt-Resume)

**Status:** draft (pilot phase — only `shipkit-why-project` currently uses this)
**Spec:** `.claude/specs/return-prompt-resume.json`

Shared protocol for Shipkit skills that need user input but run in forked contexts where `AskUserQuestion` is unavailable. Instead of hallucinating inputs the user would have provided, skills emit a structured marker and pause; the main session runs the elicitive skill inline (where it has user access), writes answers to a state file, and re-invokes the orchestrator to resume.

This protocol is **mandatory** for all Tier 1 elicitive skills listed in the spec. Do not paraphrase or re-derive the logic — reference this file.

---

## Entry Protocol (every elicitive skill follows this)

On every invocation, in order:

1. **Check for final artifact.** Read `.shipkit/<artifact>.json`. If it exists and a reviewer-flagged gap is not present, the skill is done — exit early with a "no changes needed" note.

2. **Check context shortcut.** If the skill supports a context-based shortcut (e.g., enough info in `README.md` + `package.json` to propose a complete artifact without asking), use it. Write the artifact and skip the rest of the protocol.

3. **Check elicitation state.** Read `.shipkit/elicitation/<skill-slug>/answers.md`.
   - If it contains answers sufficient for all needed fields → synthesize `.shipkit/<artifact>.json` from those answers, update `progress.json` with `status: complete` and `completed_at` timestamp, exit.
   - If it contains partial answers → continue from the next unanswered turn.
   - If it's absent or empty → start at turn 1.

4. **Generate or advance questions.** Produce 3-5 questions for the current turn, informed by any prior answers. Keep turns short — users get overwhelmed by 20 questions at once.

5. **Write state files.** Overwrite `questions.md`, append to `answers.md` (headers only, no answers yet), update `progress.json` (increment turn, refresh `last_updated_at`).

6. **Emit marker and return.** The final line of your output must be:
   ```
   NEEDS_ELICITATION:<skill-slug>
   ```
   Optionally preceded by context lines (`status=paused`, `turn=<n>`, `questions_file=...`). Do not attempt any synthesis. Do not invent answers. Do not continue past this point.

---

## File Structure

```
.shipkit/
├── <artifact>.json                       ← final output (presence = skill complete)
└── elicitation/
    └── <skill-slug>/
        ├── questions.md                  ← current turn's questions — overwritten each turn
        ├── answers.md                    ← accumulated Q&A across turns — overwritten on full re-elicitation, appended within a session
        └── progress.json                 ← turn state + timestamps
```

**Overwrite policy:** re-running a skill from scratch (user explicitly asks to refresh) overwrites all three files. Mid-elicitation resumption appends to `answers.md`.

**The elicitation folder persists** even after the artifact is complete — it's the audit trail for how the artifact was shaped. Timestamps inside the files tell you when it was last elicited.

---

## File Schemas

### `progress.json`

```json
{
  "skill": "shipkit-<name>",
  "status": "in_progress | complete",
  "elicitation_turn": 2,
  "started_at": "2026-04-18T14:32:00Z",
  "last_updated_at": "2026-04-18T14:41:00Z",
  "completed_at": null,
  "last_elicited_at": "2026-04-18T14:41:00Z",
  "total_questions_planned": 5,
  "questions_answered": 3,
  "confidence": "medium"
}
```

- `last_elicited_at` — always matches the most recent `completed_at` when complete. Used by freshness checks.
- All timestamps are ISO 8601 UTC.

### `questions.md`

```markdown
---
skill: shipkit-<name>
turn: 2
last_updated: 2026-04-18T14:41:00Z
---

## Turn 2

1. Question text here (field: `targetUsers`)
2. Second question (field: `problem`)
3. ...
```

Rewritten every turn. When elicitation completes, the file can be emptied or set to `## Complete`.

### `answers.md`

```markdown
---
skill: shipkit-<name>
turns_completed: 2
started_at: 2026-04-18T14:32:00Z
last_updated: 2026-04-18T14:45:00Z
---

## Turn 1 (2026-04-18T14:35:00Z)

**Q1: Who is this project for?**
A: [user answer]

**Q2: What problem does it solve?**
A: [user answer]

## Turn 2 (2026-04-18T14:45:00Z)
...
```

Accumulated across turns. Users can pre-populate this file directly to run the skill in batch/walk-away mode — the skill will read it and synthesize the artifact without asking.

---

## Marker Format

Emitted as the final line(s) of the forked skill's output:

```
NEEDS_ELICITATION:<skill-slug>
```

Optional additional lines (for logging or automation):

```
status=paused
turn=2
questions_file=.shipkit/elicitation/<skill-slug>/questions.md
reason=awaiting user answers for turn 2
```

**Rules:**
- The `NEEDS_ELICITATION:` prefix is load-bearing — detection depends on it
- One marker per return. If multiple elicitations are needed, they bubble up one at a time.
- The skill-slug after the colon names the elicitive skill that should run inline to collect answers (usually the skill itself).

---

## Orchestrator Dispatch Protocol

Orchestrator skills/agents that dispatch Tier 1 elicitive skills must:

1. Dispatch the child skill as usual.
2. Inspect the child's return output for `NEEDS_ELICITATION:<skill>` on the final line(s).
3. If marker present:
   - Do **not** proceed with dependent work.
   - Bubble the marker up to your own caller (emit it in your own return).
4. If marker absent:
   - Verify the expected artifact exists at `.shipkit/<artifact>.json`.
   - Proceed.

Markers bubble all the way up to the main session, where handling happens.

---

## Main Session Handling

When a top-level invocation returns with `NEEDS_ELICITATION:<skill>`:

1. Main session runs `/<skill>` **inline** (no fork). Inline execution has `AskUserQuestion`.
2. The inline skill reads `questions.md`, asks the user via `AskUserQuestion`, appends answers to `answers.md`, updates `progress.json`.
3. Main session re-invokes the original orchestrator/skill.
4. Repeat until no marker is returned.

**Automation:** a `SubagentStop` hook can parse return output for the marker and auto-dispatch. Until that hook is built, treat it as a documented convention the user follows (or Claude follows in the main session).

---

## Pre-Populated / Walk-Away Mode

Users can run elicitive skills autonomously by pre-populating `answers.md`:

1. User creates `.shipkit/elicitation/<skill-slug>/answers.md` with their answers in the expected format.
2. User invokes the skill (or an orchestrator that dispatches it).
3. Skill reads answers at step 3 of the entry protocol, synthesizes the artifact, exits without emitting a marker.

No separate "inbox" mechanism. The state file IS the input.

---

## Do Not

- **Do not hallucinate answers** when `AskUserQuestion` is unavailable. Emit the marker and return.
- **Do not skip the context shortcut** if it's available — saves the user from answering questions they've already implicitly answered in README/package.json.
- **Do not write the final artifact** until you have real answers (from user input, pre-populated file, or sufficient context).
- **Do not use a fresh elicitation folder** for every invocation. The folder is persistent; re-elicitation overwrites.
- **Do not emit the marker in inline mode.** When the skill is running in main session (has `AskUserQuestion`), just ask and proceed normally — no marker needed.

---

## How to Tell If You're in a Fork

Check whether `AskUserQuestion` is in your available tools. If it is → you're inline, proceed normally. If it isn't → you're in a fork, follow the marker protocol.

---

## Related

- Spec: `.claude/specs/return-prompt-resume.json`
- Test validation: T4/T5/T6 in `P:/Projects2/shipkit-testing/results/`
- CC limitation: [GitHub issues #12890](https://github.com/anthropics/claude-code/issues/12890) and [#18721](https://github.com/anthropics/claude-code/issues/18721)

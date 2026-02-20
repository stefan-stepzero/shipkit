---
name: shipkit-implement-independently
description: Spawn an independent implementation agent in an isolated git worktree. Creates parallel work that can be merged back via PR. Use when you want to implement something independently in the background.
argument-hint: "<spec-file-or-task-description>"
context: fork
agent: shipkit-implement-independently
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---

# shipkit-implement-independently

Spawn an autonomous implementation agent in an isolated git worktree. The agent implements the spec, verifies the work, and creates a PR targeting the source branch. You then decide whether to merge.

---

## When to Invoke

**User triggers:**
- "Implement this independently"
- "Work on this in parallel"
- "Create a branch and implement [spec]"
- "Implement [feature] in the background"

**Use cases:**
- Implementing a feature while continuing other work
- Parallel feature development
- Delegating implementation to run autonomously
- Long-running implementations you want to "fire and forget"

---

## Prerequisites

**Required:**
- Git repository initialized
- GitHub CLI (`gh`) installed and authenticated
- Clean working tree (no uncommitted changes on current branch)

**Recommended:**
- Spec file in `.shipkit/specs/active/` for structured implementation
- `.shipkit/stack.json` exists for project patterns

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│  1. SETUP                                                       │
│     • Capture current branch (source_branch)                    │
│     • Parse task input (spec path or description)               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. SPAWN AGENT (isolation: worktree)                           │
│     • CC auto-creates isolated worktree                         │
│     • Agent implements spec/task                                │
│     • Runs tests, lint, build                                   │
│     • Creates PR → source_branch                                │
│     • Returns structured result                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. MERGE PROMPT                                                │
│     • Display stats (files, lines, tests, confidence)           │
│     • Ask user: Ready to merge?                                 │
│     • On yes: squash merge via gh pr merge                      │
│     • On no: keep PR open for manual review                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Process

### Step 1: Parse Input

Extract from user input:
- **Spec file path**: If user provides `.shipkit/specs/active/*.json` path
- **Task description**: If user provides inline description
- **Task slug**: Generate from spec name or first few words

**Examples:**
```
/shipkit-implement-independently .shipkit/specs/active/login-form.json
/shipkit-implement-independently add user avatar upload feature
```

### Step 2: Capture Source Branch

```bash
SOURCE_BRANCH=$(git branch --show-current)
```

**Critical**: This is the PR target. Store it for the agent.

### Step 3: Spawn Implementation Agent

Use the Task tool to spawn `shipkit-implement-independently-agent`. The agent has `isolation: worktree` in its frontmatter — CC automatically creates and manages the worktree.

**Prompt template:**
```
Source branch (PR target): {SOURCE_BRANCH}

## Task
{spec_content_or_task_description}

## Instructions
1. Rename your branch to impl/{task-slug}
2. Implement the task completely
3. Run build, tests, lint
4. Create PR targeting {SOURCE_BRANCH}
5. Report results with stats and confidence score

Work autonomously. Create a mergeable PR.
```

**Agent settings:**
- `agent: shipkit-implement-independently` - Uses dedicated agent persona with `isolation: worktree`
- Background execution if desired

### Step 4: Receive Results

Agent returns structured result:
```
{
  pr_url: "https://github.com/org/repo/pull/42",
  target_branch: "feature/auth",
  files_changed: 5,
  lines_added: 120,
  lines_removed: 30,
  tests_passed: 12,
  tests_failed: 0,
  lint_status: "clean",
  confidence: "high",
  confidence_reasoning: "All tests pass, implementation matches spec scope"
}
```

### Step 5: Present Merge Decision

Display to user:

```
## Implementation Complete: {task_slug}

**PR**: {pr_url}
**Target**: {target_branch}

### Stats
| Metric | Value |
|--------|-------|
| Files changed | 5 |
| Lines | +120 / -30 |
| Tests | 12 passed, 0 failed |
| Lint | clean |

### Confidence: High
All tests pass, implementation matches spec scope.

---

**Ready to merge into {target_branch}?**

[Yes, squash merge] [Yes, merge commit] [Review PR first] [Skip - keep for later]
```

### Step 6: Execute User Decision

**If merge approved:**
```bash
gh pr merge {pr_number} --squash --delete-branch
```

CC automatically cleans up the worktree when the agent exits.

**If review/skip:**
```
PR available at: {pr_url}

To merge later: gh pr merge {pr_number} --squash
To cleanup stale worktrees: /shipkit-cleanup-worktrees
```

**Branch naming:** `impl/{task-slug}`

**Cleanup:**
- Auto-cleanup on successful merge
- Manual cleanup via `/shipkit-cleanup-worktrees`
- Stale worktree warnings on session start (>7 days)

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-spec` - Create a spec first
  - **When**: You have a feature idea but no formal specification
  - **Why**: Specs provide clear acceptance criteria for the agent to implement against
- `/shipkit-plan` - Create implementation plan
  - **When**: Complex feature requiring architectural decisions
  - **Why**: Plans break down work into steps the agent can follow

### After This Skill
- `/shipkit-cleanup-worktrees` - Clean up stale worktrees
  - **When**: Worktrees accumulate from abandoned or completed work
  - **Why**: Reclaim disk space and reduce clutter

### When Implementation Fails
- Manual intervention in worktree
  - **Trigger**: Agent reports low confidence or errors
  - **Why**: Worktree is preserved for debugging and manual fixes

---

## Context Files This Skill Reads

- `.shipkit/specs/active/*.json` - Spec files (if provided)
- `.shipkit/stack.json` - Project patterns (passed to agent)
- `.shipkit/architecture.json` - Design decisions (passed to agent)

---

## Context Files This Skill Writes

**Write Strategy: CREATE**
- `.shipkit/worktrees/{task-slug}/` - Isolated working directory
- Git branch: `impl/{task-slug}`
- GitHub PR targeting source branch

**Cleanup:**
- Worktree and branch auto-deleted on successful merge
- Manual cleanup via `/shipkit-cleanup-worktrees`

---

## Constraints

- **Git required**: Must be in a git repository
- **GitHub CLI required**: Uses `gh` for PR creation/merge
- **Clean working tree**: Source branch should have no uncommitted changes
- **One worktree per task**: Slug collision creates error

---

## Error Handling

**Worktree creation fails:**
- Check if slug already exists
- Check git status for conflicts
- Report error and abort

**Agent fails:**
- Worktree is preserved for debugging
- Partial work may exist
- User can manually continue or cleanup

**Merge fails:**
- PR remains open
- Worktree preserved
- User resolves conflicts manually

---

## Example Session

```
User: /shipkit-implement-independently .shipkit/specs/active/user-settings.json

Claude:
1. Captures source branch: feature/dashboard
2. Creates worktree: .shipkit/worktrees/user-settings/
3. Creates branch: impl/user-settings
4. Spawns implementation agent
5. [Agent works autonomously - implements, tests, creates PR]
6. Agent returns: PR #47, 8 files, +340/-45, all tests pass, confidence: high

Claude displays:
## Implementation Complete: user-settings

**PR**: https://github.com/acme/app/pull/47
**Target**: feature/dashboard

### Stats
| Metric | Value |
|--------|-------|
| Files changed | 8 |
| Lines | +340 / -45 |
| Tests | 15 passed, 0 failed |
| Lint | clean |

### Confidence: High
Full test coverage, implementation matches spec.

**Ready to merge into feature/dashboard?**

User: Yes, squash merge

Claude:
1. Runs: gh pr merge 47 --squash --delete-branch
2. Cleans up worktree
3. Confirms: "Merged and cleaned up. Changes now in feature/dashboard."
```

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Worktree created successfully
- [ ] Agent spawned with correct context
- [ ] Implementation completed
- [ ] PR created targeting correct branch
- [ ] User prompted for merge decision
- [ ] Cleanup executed (on merge) or preserved (on skip)
<!-- /SECTION:success-criteria -->

---

<!-- SECTION:after-completion -->
## After Completion

**If merged:** Changes are now in your source branch. Continue with your workflow.

**If skipped:** Worktree preserved at `.shipkit/worktrees/{slug}/`. Options:
- Review PR manually on GitHub
- Continue work in worktree later
- Run `/shipkit-cleanup-worktrees` to remove

**Next steps:**
- Continue with main work (implementation was parallel)
- `/shipkit-verify` - If you want to verify the merged changes
- `/shipkit-work-memory` - Log the parallel implementation in progress
<!-- /SECTION:after-completion -->

---

## Troubleshooting

**"Worktree already exists"**
- Another implementation with same slug is in progress
- Use `/shipkit-cleanup-worktrees` to review and clean

**"gh: command not found"**
- Install GitHub CLI: https://cli.github.com/
- Authenticate: `gh auth login`

**"Branch already exists"**
- Previous implementation wasn't fully cleaned up
- Run: `git branch -D impl/{slug}` then retry

**Agent seems stuck**
- Check `.shipkit/worktrees/{slug}/` for partial work
- Agent may be running relentless loops
- Let it finish or manually intervene

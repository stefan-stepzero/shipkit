# Loop Mode Reference

Shared reference for skills that support `--loop N` iterative execution.

## How It Works

1. User invokes skill with `--loop N` (e.g., `/shipkit-framework-integrity --loop 3 --fix`)
2. Skill creates a state file in `.shipkit/` with YAML frontmatter
3. Skill runs its normal check, then updates the Progress section
4. If the completion promise is met (zero errors), skill deletes the state file and stops
5. If not met, skill ends its response — the relentless stop hook blocks exit and feeds context back
6. Claude continues with the next iteration, reading the Progress section for context
7. Repeats until promise met or N iterations exhausted

## State File Format

**Filename pattern**: `.shipkit/{name}-loop.local.md`

Examples:
- `.shipkit/framework-integrity-loop.local.md`
- `.shipkit/validate-skill-loop.local.md`

**Structure**:

```markdown
---
skill: framework-integrity
enabled: true
iteration: 1
max_iterations: 3
completion_promise: "Framework integrity check reports zero errors and zero warnings"
---

## Task

Run /shipkit-framework-integrity --fix and resolve all issues found.

## Progress

### Iteration 1
- Ran integrity check: 4 errors, 2 warnings
- Fixed: manifest sync (2 errors), broken reference (1 error)
- Remaining: 1 error (missing hook in installer), 2 warnings
```

## Parsing `--loop N`

When the skill receives arguments containing `--loop`:

1. Extract N from `--loop N` (default: 3 if `--loop` specified without number)
2. Validate N is between 1 and 10
3. Create the state file with `max_iterations: N` and `iteration: 1`
4. Proceed with normal skill execution

## Creating the State File

```
1. Build frontmatter:
   - skill: {skill-short-name}  (e.g., "framework-integrity")
   - enabled: true
   - iteration: 1
   - max_iterations: {N from --loop}
   - completion_promise: {skill-specific promise}

2. Build body:
   ## Task
   {What the skill should do each iteration}

   ## Progress
   (empty — filled after first iteration)

3. Write to .shipkit/{name}-loop.local.md
```

## Updating Progress After Each Iteration

After completing a check (whether first or subsequent iteration):

1. Read the current state file
2. Append to the `## Progress` section:
   ```
   ### Iteration {N}
   - {summary of what was checked}
   - {summary of what was fixed, if --fix was used}
   - {summary of remaining issues}
   ```
3. Write the updated state file

## Checking Completion and Cleanup

After each iteration:

1. Evaluate the completion promise against actual results
2. If promise is met (e.g., zero errors and zero warnings):
   - Delete the state file
   - Output a success message: "Loop complete: promise met after {N} iterations"
   - End response (hook will allow exit since file is gone)
3. If promise is NOT met:
   - Ensure Progress section is updated
   - End response normally (hook will block exit and re-prompt)

## Integration with Stop Hook

The `shipkit-relentless-stop-hook.py` discovers loop state files via glob:
- Pattern: `.shipkit/*-loop.local.md`
- Priority: relentless > standby > loop (loop files checked last)
- The hook increments the iteration counter and feeds back the task + progress
- When max iterations reached, hook deletes the file and allows exit

## Early Exit

To stop a loop early:
- Delete the `.shipkit/*-loop.local.md` file manually
- Or set `enabled: false` in the frontmatter
- The hook will allow exit on the next stop attempt

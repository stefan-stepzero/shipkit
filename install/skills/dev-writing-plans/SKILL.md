---
name: writing-plans
description: "DEPRECATED - Use /plan instead. This skill is for reference only."
---

# Writing Plans

## DEPRECATED

**This skill has been integrated into the devkit workflow.**

Use the standard workflow instead:
```
/brainstorming → /specify → /plan → /tasks → /implement
```

- `/plan` creates structured implementation plans in `.devkit/specs/XXX/plan.md`
- `/implement` executes with TDD and optional subagent mode

---

## Legacy Reference (for ad-hoc use only)

If you're working outside of devkit and need a quick plan:

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

**Bite-sized tasks (2-5 minutes each):**
```markdown
**Step 1: Write the failing test**
```python
def test_feature():
    result = feature()
    assert result == expected
```

**Step 2: Run test to verify it fails**
Run: `pytest tests/test.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**
...

**Step 4: Run test to verify it passes**
...

**Step 5: Commit**
```

**But prefer the devkit workflow** - it provides better structure, traceability, and automatic TDD/review enforcement.

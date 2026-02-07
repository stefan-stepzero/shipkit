# File 5: Update install/shared/hooks/suggest-next-skill.py

**Purpose**: Add detection logic and suggestion message for new skill

**File**: `install/shared/hooks/suggest-next-skill.py`

**Note**: Current implementation is very simple and may not require modification for every skill. Only update if the skill has specific next-step triggers.

---

## Current Hook Structure

```python
#!/usr/bin/env python3
"""
Shipkit - Suggest Next Skill Hook

Prompts user to check what's next after Claude stops.
Delegates all intelligence to shipkit-whats-next skill.
"""

import sys
from pathlib import Path


def main():
    """Suggest running shipkit-whats-next for intelligent workflow guidance."""

    # Check if this is a Lite installation
    project_root = Path.cwd()
    shipkit_lite = project_root / '.shipkit'

    if shipkit_lite.exists():
        # Lite installation - suggest shipkit-whats-next
        print()
        print("---")
        print()
        print("💡 **What's next?** Run `/shipkit-whats-next` for smart workflow guidance")
        print()
    else:
        # Full Shipkit or no Shipkit - no suggestion
        pass

    return 0


if __name__ == '__main__':
    sys.exit(main())
```

---

## When to Modify This Hook

**Modify ONLY if**:
- Your skill creates a specific output file that triggers a natural next step
- There's a deterministic "after X, always do Y" pattern
- The suggestion is MORE specific than generic "run /shipkit-whats-next"

**Don't modify if**:
- Your skill is part of a flexible workflow
- Next steps depend on context
- Generic "/shipkit-whats-next" is sufficient

---

## Pattern: File-Based Detection

**If your skill creates a specific output that triggers next steps:**

### Example: shipkit-spec creates spec → suggest shipkit-plan

**Add detection logic**:

```python
def main():
    """Suggest next skill based on recent file changes."""

    project_root = Path.cwd()
    shipkit_lite = project_root / '.shipkit'

    if not shipkit_lite.exists():
        return 0

    # Check for recently created spec files
    specs_dir = shipkit_lite / 'specs' / 'active'
    if specs_dir.exists():
        # Get most recent spec file
        spec_files = list(specs_dir.glob('*.json'))
        if spec_files:
            most_recent = max(spec_files, key=lambda p: p.stat().st_mtime)
            age_seconds = time.time() - most_recent.stat().st_mtime

            # If spec was created < 5 minutes ago
            if age_seconds < 300:
                print()
                print("---")
                print()
                print(f"📋 New spec created: {most_recent.name}")
                print()
                print("💡 **Next step**: Run `/shipkit-plan` to create implementation plan")
                print()
                return 0

    # Default suggestion
    print()
    print("---")
    print()
    print("💡 **What's next?** Run `/shipkit-whats-next` for smart workflow guidance")
    print()

    return 0
```

---

## Pattern: Multiple File Detection

**If multiple output types require different suggestions:**

```python
import time
from pathlib import Path


def check_recent_file(path: Path, max_age_seconds: int = 300) -> bool:
    """Check if file was modified within max_age_seconds."""
    if not path.exists():
        return False
    age = time.time() - path.stat().st_mtime
    return age < max_age_seconds


def main():
    """Suggest next skill based on recent activity."""

    project_root = Path.cwd()
    shipkit_lite = project_root / '.shipkit'

    if not shipkit_lite.exists():
        return 0

    # Check different output types (in priority order)

    # 1. Recently created spec → suggest plan
    specs_dir = shipkit_lite / 'specs' / 'active'
    if specs_dir.exists():
        recent_specs = [f for f in specs_dir.glob('*.json') if check_recent_file(f)]
        if recent_specs:
            print("💡 New spec created → Run `/shipkit-plan`")
            return 0

    # 2. Recently created plan → suggest implement
    plans_dir = shipkit_lite / 'plans'
    if plans_dir.exists():
        recent_plans = [f for f in plans_dir.glob('*.json') if check_recent_file(f)]
        if recent_plans:
            print("💡 New plan created → Run `/shipkit-implement`")
            return 0

    # 3. Recently logged decision → suggest spec or plan
    arch_file = shipkit_lite / 'architecture.json'
    if check_recent_file(arch_file):
        print("💡 Decision logged → Continue with `/shipkit-spec` or `/shipkit-plan`")
        return 0

    # Default: generic suggestion
    print("💡 **What's next?** Run `/shipkit-whats-next` for guidance")
    return 0
```

---

## Template for Adding New Detection

**If your skill creates**: `.shipkit/{OUTPUT_PATH}`

**Add this detection block**:

```python
# Check for {SKILL_NAME} output
{OUTPUT_FILE} = shipkit_lite / '{OUTPUT_PATH}'
if check_recent_file({OUTPUT_FILE}):
    print()
    print("---")
    print()
    print("💡 {SKILL_NAME} complete → Run `/{NEXT_SKILL}`")
    print()
    return 0
```

---

## Decision Tree: Should You Modify?

```
Does your skill create a file?
├─ NO → Don't modify hook
└─ YES → Is there ONE obvious next step?
    ├─ NO → Don't modify hook (use /shipkit-whats-next)
    └─ YES → Is this next step ALWAYS correct?
        ├─ NO → Don't modify hook
        └─ YES → Add detection logic
```

---

## Examples by Skill Type

### Example 1: SHOULD Modify (Deterministic Flow)

**Skill**: `shipkit-spec`
**Output**: `.shipkit/specs/active/[feature].json`
**Next Step**: ALWAYS `/shipkit-plan`

✅ **Add detection**: Spec → Plan is deterministic

---

### Example 2: SHOULD NOT Modify (Flexible Flow)

**Skill**: `shipkit-architecture-memory`
**Output**: Appends to `.shipkit/architecture.json`
**Next Step**: Could be `/shipkit-spec`, `/shipkit-plan`, `/shipkit-implement`, or something else

❌ **Don't modify**: Next step is context-dependent

---

### Example 3: SHOULD NOT Modify (No Clear Next Step)

**Skill**: `shipkit-communications`
**Output**: Creates HTML visualization
**Next Step**: Returns to previous workflow

❌ **Don't modify**: No specific next skill

---

## Validation

**After modifying, test**:

```bash
# Run the hook manually
python install/shared/hooks/suggest-next-skill.py

# Should output suggestion based on recent files
```

**Check**:
- [ ] Python syntax is valid (`python -m py_compile`)
- [ ] Import statements are correct
- [ ] File paths are correct
- [ ] Time-based detection works (< 5 minutes)
- [ ] Suggestion message is helpful

---

## Common Mistakes

**❌ Overly complex detection**
- Keep it simple: check file timestamp, suggest next step

**❌ Adding suggestions for every skill**
- Most skills don't need specific detection
- Generic `/shipkit-whats-next` is often better

**❌ Breaking existing detection**
- Add new detection BEFORE default suggestion
- Don't remove the fallback `/shipkit-whats-next` message

**❌ Incorrect file paths**
- Use `Path` objects, not string concatenation
- Test file existence checks

---

## Report Format

**If modified**:
```
✓ File 5: Updated suggest-next-skill.py
  - Added detection for {output_file}
  - Suggests: /{next-skill} when file < 5 minutes old
  - Python syntax validated ✓
```

**If not modified** (most common):
```
⊘ File 5: No hook modification needed
  - Skill relies on /shipkit-whats-next for suggestions
  - No deterministic next step to detect
```

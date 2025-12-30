---
name: lite-debug-systematically
description: Structured 4-phase debugging methodology to find root causes instead of random fixes. Guides through Observe, Hypothesize, Test, Fix phases with evidence-based investigation. Documents bugs in architecture.md for future reference.
---

# debug-systematically-lite - Evidence-Based Debugging

**Purpose**: Replace "try this fix" debugging cycles with systematic root cause investigation. Find the real problem before writing code.

---

## When to Invoke

**User triggers**:
- "This isn't working"
- "I'm getting an error"
- "Bug in [feature]"
- "Sharing/auth/feature X is broken"
- "Why is this failing?"

**Auto-invoked by**:
- `/lite-implement` when tests fail unexpectedly
- `/lite-quality-confidence` when verification fails

---

## Prerequisites

**Optional but helpful**:
- Spec exists: `.shipkit-lite/specs/active/[feature].md` (to understand expected behavior)
- Implementation exists: `.shipkit-lite/implementations.md` (to understand current code)
- Stack defined: `.shipkit-lite/stack.md` (to know tech being debugged)

**Can run standalone**: User reports bug without any prior context.

---

## The Anti-Pattern We're Preventing

**Random Fix Debugging (BAD)**:
```
User: "Sharing isn't working"
Developer: "Try adding await here"
[doesn't work]
Developer: "Maybe the permissions are wrong, try this"
[doesn't work]
Developer: "Let's refactor the whole thing"
[30 minutes wasted, still broken]
```

**Systematic Debugging (GOOD)**:
```
User: "Sharing isn't working"
Developer: "Let me observe the exact error first"
[Sees: 500 error in network tab]
Developer: "Hypothesis: Server action is failing. Test: Check server logs"
[Finds: Missing auth check throwing error]
Developer: "Root cause found. Fix: Add auth validation"
[Fixed in 5 minutes]
```

**The rule**: Evidence first, fixes last. No code changes until root cause is identified.

---

## Process

### Phase 1: OBSERVE - Gather Evidence

**Before asking hypothetical questions, collect facts.**

**Ask user these questions**:

1. **What is the exact symptom?**
   - "What did you try to do?"
   - "What happened instead?"
   - "Is there an error message? (exact text)"

2. **When does it happen?**
   - "Every time or intermittent?"
   - "Did this ever work?"
   - "What changed recently?"

3. **Where is the evidence?**
   - "Check browser console - any errors?"
   - "Check network tab - any failed requests?"
   - "Check server logs - any output?"
   - "Check terminal - any error traces?"

**Evidence Collection Template**:

See `references/debugging-templates.md` for:
- Complete evidence collection template
- "Where to look for evidence" guide by symptom type
- Environment and recent changes tracking

**Complete Phase 1 before moving to Phase 2.**---

### Phase 2: HYPOTHESIZE - List Possible Causes

**Now that we have evidence, what could explain it?**

**Based on evidence collected, list 3-5 hypotheses ranked by likelihood**:

See `references/debugging-templates.md` for:
- Complete hypothesis ranking template
- Common bug pattern → hypothesis mapping
- How to rule out hypotheses

**Ask user**:
- "Based on [evidence], my top hypothesis is [X]. Does that align with what you're seeing?"
- "Should I test hypothesis #1 first, or do you have a different theory?"

**Don't skip this phase.**---

### Phase 3: TEST - Validate Hypotheses

**Design tests to prove/disprove each hypothesis.**

**For each hypothesis, determine the fastest way to test it**:

See `references/debugging-templates.md` for:
- Complete test execution template
- Test methods by bug type (auth, data, race conditions, etc.)
- Evidence-based testing patterns

**Keep testing until ONE hypothesis is confirmed as root cause.**---

### Phase 4: FIX - Implement Solution

**Only execute this phase once root cause is identified.**

**Before writing code**:

1. **Confirm root cause**:
   - "The root cause is: [specific problem]"
   - "Evidence: [what we found in testing]"
   - "The fix: [what needs to change]"

2. **Plan minimal fix**:
   - Don't refactor everything
   - Fix the specific issue
   - Add test to prevent regression (if appropriate)

3. **Execute fix**:

See `references/debugging-templates.md` for:
- Complete fix implementation template
- Verification checklist (symptom gone, no new errors, test added)
- Fix testing guidelines

**After fix verified**, document the bug:**After fix verified**, document the bug:

---

### Step 5: Document in Architecture

**Use Write tool to APPEND to `.shipkit-lite/architecture.md`**:

See `references/debugging-templates.md` for:
- Complete bug documentation template
- Example filled documentation
- Why document bugs (future reference, team learning, pattern recognition)

---

## What Makes This "Lite"

**Included**:
- ✅ 4-phase systematic methodology
- ✅ Evidence gathering before guessing
- ✅ Hypothesis ranking
- ✅ Test-driven investigation
- ✅ Minimal targeted fixes
- ✅ Bug documentation in architecture.md

**Not included** (vs full dev-systematic-debugging):
- ❌ Git bisect automation
- ❌ Performance profiling
- ❌ Memory leak detection
- ❌ Distributed tracing
- ❌ Integration test harness
- ❌ Regression test suite generation

**Philosophy**: Get to root cause fast, fix it cleanly, document it. Good enough for POC/MVP debugging.

---

## Integration with Other Skills

**Before debug-systematically-lite**:
- `/lite-implement` - May auto-invoke this when tests fail
- `/lite-quality-confidence` - May auto-invoke when verification fails

**During debug-systematically-lite**:
- May read: `.shipkit-lite/specs/active/[feature].md` (expected behavior)
- May read: `.shipkit-lite/implementations.md` (current code context)
- May read: `.shipkit-lite/stack.md` (tech stack debugging tips)

**After debug-systematically-lite**:
- `/lite-architecture-memory` - If fix reveals architectural pattern to remember
- `/lite-quality-confidence` - Verify fix didn't break other things
- `/lite-implement` - Continue implementation after fix

---

## Context Files This Skill Reads

**Optional context** (load if helpful):
- `.shipkit-lite/specs/active/[feature].md` - Expected behavior
- `.shipkit-lite/implementations.md` - Current code
- `.shipkit-lite/stack.md` - Tech stack
- `.shipkit-lite/architecture.md` - Past bug patterns

**None are required.** Can debug from zero context.

---

## Context Files This Skill Writes

**Write Strategy**: **APPEND** (preserves all historical bug documentation)

**Updates**:
- `.shipkit-lite/architecture.md` - Appends bug documentation after each fix

**Why APPEND?**
- Builds architectural memory of bug patterns over time
- Enables pattern recognition (similar bugs → check past fixes)
- Preserves team learning history
- Chronological bug log helps identify recurring issues
- Referenced by future debugging sessions to avoid repeated mistakes

---

## Success Criteria

Debug session is complete when:
- [ ] Root cause identified with evidence
- [ ] Fix implemented and verified
- [ ] Original symptom gone
- [ ] No new errors introduced
- [ ] Bug documented in architecture.md
- [ ] User can demonstrate feature works

---

## Common Debugging Scenarios

See `references/debugging-scenarios.md` for detailed examples:
- Scenario 1: API Call Failing (auth check missing)
- Scenario 2: UI Not Rendering (null check missing)
- Scenario 3: Build Error (package not installed)

Each scenario demonstrates the full 4-phase process from observation to fix.

---

## Tips for Effective Debugging---

## Tips for Effective Debugging

**Resist the urge to fix immediately**:
- Observation phase is fastest in the long run
- 5 minutes of evidence gathering saves 30 minutes of wrong fixes

**Use browser/server logs first**:
- Errors tell you exactly what's wrong
- Stack traces point to exact lines
- Network tab shows what data is moving

**Narrow the scope**:
- Binary search: Is it client or server?
- Is it data, code, or infrastructure?
- When did it last work?

**Document even "obvious" bugs**:
- Future you will forget
- Team members hit the same issues
- Patterns emerge over time

**When to upgrade to full /dev-systematic-debugging**:
- Production incidents requiring RCA
- Performance issues needing profiling
- Intermittent bugs requiring statistical analysis
- Complex distributed system debugging
- Regression requiring git bisect

---

## Suggest Next Skill at Completion

**After documenting the bug fix, suggest**:

**If debugging during implementation**:
```
✅ Bug fixed and documented

📁 Updated: .shipkit-lite/architecture.md
🐛 Root cause: [brief description]
🔧 Fix: [brief description]

👉 Next: /lite-implement
   Continue implementation where you left off

Ready to continue?
```

**If debugging after implementation**:
```
✅ Bug fixed and documented

📁 Updated: .shipkit-lite/architecture.md
🐛 Root cause: [brief description]
🔧 Fix: [brief description]

👉 Next: /lite-quality-confidence
   Verify this fix didn't break other things

Ready to verify?
```

**If architectural pattern discovered**:
```
✅ Bug fixed and documented

📁 Updated: .shipkit-lite/architecture.md
🐛 Root cause: [brief description]
🔧 Fix: [brief description]

💡 This fix reveals a pattern: [pattern description]

👉 Consider: /lite-architecture-memory
   Log this pattern to prevent future bugs

Document the pattern?
```

---

## The Golden Rule

**Evidence → Hypothesis → Test → Fix**

Never skip phases. Never guess before observing. Never fix before confirming root cause.

Systematic debugging is slower at first, but 10x faster overall because you fix the real problem the first time.

---

**Remember**: POC debugging prioritizes speed, but systematic beats random every time. Spend 5 minutes investigating, save 30 minutes of wrong fixes.

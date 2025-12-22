# Systematic Debugging Reference

Complete guide to root cause investigation before fixing.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

This means:
- No "quick fix for now"
- No "just try changing X"
- No "add multiple changes and see"
- No "probably this, let me fix it"

**Find root cause FIRST. Fix SECOND. Always.**

## The Four Phases

### Phase 1: Root Cause Investigation

**Goal:** Find the REAL problem, not the symptom.

**Process:**
1. Read the error message completely
2. Locate where the error occurs
3. Understand what the code is trying to do
4. Identify why it's failing

**Example:**
```
Error: Cannot read property 'price' of undefined
  at calculateTotal (calculate.js:10)
```

**Investigation:**
```javascript
// Line 10 in calculate.js
const total = items.reduce((sum, item) => sum + item.price, 0);
                                                      ↑
                                              Why is item undefined?
```

**Root Cause:**
```javascript
// Looking at the data
const items = [
  { price: 10 },
  { price: 20 },
  null,  // ← ROOT CAUSE: null item in array
  { price: 30 }
];
```

**Not root cause:** "reduce is broken"
**Not root cause:** "price property missing"
**Root cause:** Null item in array

### Phase 2: Pattern Analysis

**Goal:** Understand what works vs. what doesn't.

**Compare:**
- What works?
- What fails?
- What's different?

**Example:**
```
✓ calculateTotal([{price: 10}])           → Works
✓ calculateTotal([{price: 10}, {price: 20}]) → Works
✗ calculateTotal([{price: 10}, null])     → Fails
✗ calculateTotal([null])                  → Fails

Pattern: Fails when array contains null
```

### Phase 3: Hypothesis and Testing

**Goal:** Verify your understanding before fixing.

**Process:**
1. Form hypothesis about root cause
2. Design test to prove/disprove
3. Run test
4. Confirm or refine hypothesis

**Example:**
```javascript
// Hypothesis: Function doesn't handle null items

// Test (create focused failing test)
test('calculateTotal handles null items', () => {
  const items = [
    { price: 10 },
    null,
    { price: 20 }
  ];

  expect(calculateTotal(items)).toBe(30);
});

// Run test
// FAIL: Cannot read property 'price' of undefined
// ✓ Hypothesis confirmed
```

### Phase 4: Implementation

**Goal:** Fix the ROOT CAUSE, not the symptom.

**Process:**
1. Write test for the bug (RED)
2. Fix root cause (GREEN)
3. Verify fix with evidence
4. Run all tests (no regressions)

**Example:**
```javascript
// Fix: Filter out null items
function calculateTotal(items) {
  const validItems = items.filter(item => item !== null);
  return validItems.reduce((sum, item) => sum + item.price, 0);
}

// Run test
// PASS: calculateTotal handles null items
```

## Common Debugging Patterns

### Pattern 1: The Error Message Investigation

**Error:**
```
TypeError: Cannot read property 'length' of undefined
  at formatList (format.js:42)
```

**Investigation:**
```javascript
// What's on line 42?
function formatList(items) {
  if (items.length === 0) return 'No items';  // Line 42
  return items.map(i => i.name).join(', ');
}

// What's undefined? items
// Why? Function called without argument
// Root cause: Missing argument validation
```

**Fix:**
```javascript
function formatList(items) {
  if (!items || items.length === 0) return 'No items';
  return items.map(i => i.name).join(', ');
}
```

### Pattern 2: The Unexpected Behavior

**Problem:**
```javascript
// Expected: [2, 4, 6]
// Actual:   [1, 2, 3]

const numbers = [1, 2, 3];
const doubled = numbers.map(n => n * 2);
console.log(numbers); // [1, 2, 3] ← Not [2, 4, 6]
```

**Investigation:**
```
What did I expect? numbers to be modified
What actually happened? numbers unchanged
Why? map() returns NEW array, doesn't modify original
Root cause: Misunderstanding of map() behavior
```

**Fix:**
```javascript
const numbers = [1, 2, 3];
const doubled = numbers.map(n => n * 2);
console.log(doubled); // [2, 4, 6] ← Use the return value
```

### Pattern 3: The Intermittent Failure

**Problem:**
```
Test sometimes passes, sometimes fails
```

**Investigation:**
```
When does it pass? After X
When does it fail? After Y
What's different?

Common causes:
• Async timing issues
• Test order dependencies
• Shared mutable state
• Random data generation
```

**Root cause discovery:**
```javascript
// Hypothesis: Tests share state

test('test 1', () => {
  sharedCache.set('user', { id: 1 });
  expect(sharedCache.get('user').id).toBe(1);
});

test('test 2', () => {
  // Assumes clean cache, but test 1 ran first
  expect(sharedCache.get('user')).toBeUndefined(); // FAILS if test 1 ran
});

// Root cause: Tests share mutable cache
```

**Fix:**
```javascript
beforeEach(() => {
  sharedCache.clear(); // Clean state before each test
});
```

### Pattern 4: The Performance Issue

**Problem:**
```
Function is too slow
```

**Investigation:**
```javascript
// Measure first
console.time('calculateTotal');
const total = calculateTotal(items);
console.timeEnd('calculateTotal');
// calculateTotal: 2534.234ms ← Too slow

// Profile: Where is time spent?
// [Use profiler or add strategic timing]

console.time('reduce');
const total = items.reduce((sum, item) => sum + item.price, 0);
console.timeEnd('reduce');
// reduce: 5.123ms ← Not the problem

console.time('API call inside loop');
items.forEach(item => {
  fetchItemDetails(item.id); // ← Makes API call for EACH item
});
console.timeEnd('API call inside loop');
// API call inside loop: 2500.456ms ← ROOT CAUSE
```

**Root cause:** N+1 query problem (API call per item)

**Fix:**
```javascript
// Batch fetch all items at once
const itemIds = items.map(i => i.id);
const details = await fetchItemDetailsBatch(itemIds);
```

## Red Flags

### Red Flag 1: "Quick fix for now"

**Problem:**
```
"I'll just add a try-catch and investigate later"
```

**Why it's wrong:**
- Hides the real problem
- Creates technical debt
- May mask future bugs

**Right approach:**
1. Investigate WHY it's throwing
2. Fix root cause
3. Then add try-catch if truly needed

### Red Flag 2: "Just try changing X"

**Problem:**
```
"Try changing the timeout from 1000 to 5000 and see if it works"
```

**Why it's wrong:**
- No understanding of problem
- Random changes create confusion
- Wastes time

**Right approach:**
1. Why does timeout matter?
2. What's taking so long?
3. Fix the slowness, don't hide it

### Red Flag 3: Multiple changes at once

**Problem:**
```
"I changed X, Y, and Z. One of them should fix it."
```

**Why it's wrong:**
- Don't know which change helped
- May have introduced new bugs
- Can't understand root cause

**Right approach:**
1. Make ONE change
2. Test
3. If it works, understand why
4. If not, revert and try next hypothesis

### Red Flag 4: "Probably this"

**Problem:**
```
"It's probably a caching issue, let me add cache.clear()"
```

**Why it's wrong:**
- Guessing without investigation
- May be wrong
- Doesn't prove hypothesis

**Right approach:**
1. Form hypothesis: "It's caching"
2. Test hypothesis: Disable cache, does it work?
3. Confirm: Yes/no
4. Fix based on confirmed understanding

### Red Flag 5: Fix attempt #4

**Problem:**
```
Fix 1: Didn't work
Fix 2: Didn't work
Fix 3: Didn't work
Fix 4: Let me try...
```

**Why it's wrong:**
- 3+ failed fixes = don't understand problem
- Thrashing, not debugging
- Wasting time

**Right approach after 3 failures:**
1. STOP
2. Question the architecture
3. Ask for help
4. Review assumptions
5. Start investigation from scratch

## Debugging Tools by Language

### JavaScript/TypeScript

```javascript
// Console logging
console.log('Variable:', variable);
console.table(arrayOfObjects);
console.trace(); // Call stack

// Debugger
debugger; // Breakpoint in code

// Node.js inspect
node --inspect-brk app.js

// Browser DevTools
// Right-click → Inspect → Sources → Set breakpoints
```

### Python

```python
# Print debugging
print(f"Variable: {variable}")

# Debugger
import pdb; pdb.set_trace()

# Or ipdb (better)
import ipdb; ipdb.set_trace()

# Or breakpoint() (Python 3.7+)
breakpoint()
```

### Go

```go
// Print debugging
fmt.Printf("Variable: %+v\n", variable)

// Delve debugger
// dlv debug
// (dlv) break main.go:42
// (dlv) continue
```

### Rust

```rust
// Print debugging
println!("Variable: {:?}", variable);

// Or debug
dbg!(variable);

// rust-gdb or rust-lldb
// rust-gdb target/debug/myapp
```

## Investigation Techniques

### Technique 1: Binary Search

**When:** Bug is in large codebase, not sure where

**Process:**
1. Find midpoint in execution
2. Add logging/breakpoint
3. Run code
4. Bug before or after midpoint?
5. Repeat on problematic half
6. Narrow down until found

**Example:**
```
Code path: A → B → C → D → E → F

Bug occurs at F

Midpoint: C
Check: A → B → C (working? yes)
      C → D → E → F (working? no)

Midpoint of C→F: E
Check: C → D → E (working? yes)
      E → F (working? no)

Bug is in E → F transition
```

### Technique 2: Rubber Duck Debugging

**When:** Stuck, can't find root cause

**Process:**
1. Explain code to rubber duck (or colleague)
2. Line by line, what it does
3. Often realize problem while explaining

**Example:**
```
"So this function takes an array of items...
 It filters out... wait, it filters?
 But I want to map, not filter!
 Found it: wrong method."
```

### Technique 3: Minimal Reproduction

**When:** Complex bug in large system

**Process:**
1. Create smallest possible code that reproduces bug
2. Remove everything unrelated
3. If bug disappears, what was removed?
4. If bug persists, debug minimal version

**Example:**
```javascript
// Original (100 lines, complex)
class ShoppingCart {
  // ... many methods
  calculateTotal() {
    // Bug is here somewhere
  }
}

// Minimal reproduction (5 lines)
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

calculateTotal([{price: 10}, null]); // ERROR
// Now easy to debug
```

### Technique 4: Bisect Blame

**When:** Bug appeared recently, not sure which change

**Process:**
```bash
# Git bisect
git bisect start
git bisect bad           # Current commit is bad
git bisect good <commit> # Known good commit

# Git will checkout midpoint
# Test: Does bug exist?

git bisect bad   # If yes
git bisect good  # If no

# Repeat until found
```

## When to Ask for Help

**Ask for help when:**
1. 3+ fix attempts failed
2. Investigating for 2+ hours without progress
3. Suspecting architecture problem
4. Outside your expertise (concurrency, security, etc.)

**Before asking:**
1. Write down what you know
2. What you've tried
3. What you suspect
4. Minimal reproduction

**Better question:**
```
"I'm debugging a null pointer error in calculateTotal().

What I know:
• Error occurs at line 42 when processing items array
• Happens when array contains null
• Started after commit abc123

What I've tried:
• Added null check, still fails
• Logged items array, it's undefined
• Traced back to caller, it passes items correctly

What I suspect:
• Items is being mutated somewhere between caller and callee

Minimal reproduction:
[code]

Can you help me understand why items becomes undefined?"
```

## Debugging Checklist

Before attempting any fix:

- [ ] Read error message completely
- [ ] Located where error occurs
- [ ] Understand what code is trying to do
- [ ] Identified why it's failing
- [ ] Compared working vs. failing cases
- [ ] Formed hypothesis about root cause
- [ ] Tested hypothesis
- [ ] Confirmed root cause
- [ ] Written test for the bug
- [ ] Ready to fix

**If ANY checkbox unchecked → Keep investigating, don't fix yet**

## Quick Reference

```
┌──────────────────────────────────────────┐
│ DEBUGGING QUICK REFERENCE                │
├──────────────────────────────────────────┤
│ When encountering a bug:                 │
│                                          │
│ 1. INVESTIGATE                           │
│    → Read error completely               │
│    → Locate where it fails               │
│    → Understand why                      │
│                                          │
│ 2. PATTERN ANALYSIS                      │
│    → What works?                         │
│    → What fails?                         │
│    → What's different?                   │
│                                          │
│ 3. HYPOTHESIS                            │
│    → Form theory                         │
│    → Design test                         │
│    → Confirm/refine                      │
│                                          │
│ 4. FIX                                   │
│    → Write test for bug (RED)            │
│    → Fix root cause (GREEN)              │
│    → Verify with evidence                │
│    → All tests pass                      │
│                                          │
│ ONLY THEN claim fixed                    │
└──────────────────────────────────────────┘

RED FLAGS:
• "Quick fix" → INVESTIGATE FIRST
• "Try this" → HYPOTHESIS FIRST
• "Probably X" → CONFIRM FIRST
• 3+ failed fixes → QUESTION ARCHITECTURE
```

## The Three Questions

Before claiming a bug is fixed, answer these:

1. **What was the root cause?**
   - Not: "I changed X and it worked"
   - Yes: "The root cause was Y because Z"

2. **How do I know it's fixed?**
   - Not: "Should be fixed now"
   - Yes: "Test passes, here's the output"

3. **How will I prevent this in the future?**
   - Not: "I'll be more careful"
   - Yes: "Added test to catch this pattern"

---

**Remember:** Debugging is not trial-and-error. It's systematic investigation guided by evidence and logic.

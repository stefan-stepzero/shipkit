# Test-Driven Development (TDD) Reference

Complete guide to the RED-GREEN-REFACTOR cycle for implementation.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

This is not a suggestion. This is not a best practice. This is the law.

Write code before the test? Delete it. Start over.

## The Three Phases

### 🔴 RED - Write a Failing Test First

**What:**
Write a test that describes the behavior you want to implement.

**Why:**
- Proves the test actually works (if it passes immediately, the test is broken)
- Defines the interface before implementation (design-first)
- Creates a clear goal for the implementation
- Prevents false confidence from broken tests

**How:**
1. Think about what behavior you need
2. Write a test that uses that behavior
3. Run the test
4. Watch it FAIL
5. Read the failure message (does it make sense?)

**Example (JavaScript):**
```javascript
// ❌ RED - This should FAIL
test('calculateTotal sums item prices', () => {
  const items = [
    { price: 10 },
    { price: 20 },
    { price: 30 }
  ];

  const total = calculateTotal(items);

  expect(total).toBe(60);
});

// Run: npm test
// Expected: FAIL - calculateTotal is not defined
```

**Red Flags:**
- Test passes immediately → Test is broken, fix it
- No test run before coding → Stop, write test first
- "I'll test it after" → No, test BEFORE
- "Quick fix, I'll test later" → Delete the code, start with test

### 🟢 GREEN - Write Minimal Code to Pass

**What:**
Write the SIMPLEST code that makes the test pass. Nothing more.

**Why:**
- Prevents over-engineering
- Keeps focus on solving the actual problem
- Reveals what's truly needed (vs. what we think we need)
- Makes refactoring safer (smaller changes)

**How:**
1. Write the minimal code
2. Run the test
3. Watch it PASS
4. Run ALL tests
5. Verify no regressions

**Example (JavaScript):**
```javascript
// ✅ GREEN - Minimal implementation
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Run: npm test
// Expected: PASS - all tests green
```

**Red Flags:**
- Adding features not tested → Remove them
- "While I'm here..." improvements → Stop, refactor phase only
- Premature optimization → Just make it work first
- Extra parameters "for future use" → YAGNI, remove them

**Common Temptations to Resist:**

❌ **Don't do this:**
```javascript
// TOO MUCH - not all of this is tested
function calculateTotal(items, taxRate = 0, discountCode = null) {
  let total = items.reduce((sum, item) => sum + item.price, 0);

  if (taxRate) {
    total *= (1 + taxRate);
  }

  if (discountCode) {
    total *= 0.9; // 10% discount
  }

  return total;
}
```

✅ **Do this instead:**
```javascript
// MINIMAL - only what's tested
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

Add tax and discounts when you have TESTS for them.

### 🔵 REFACTOR - Clean Up While Tests Pass

**What:**
Improve the code structure without changing behavior.

**Why:**
- Removes duplication (DRY)
- Improves readability
- Simplifies complexity
- Prepares code for next feature

**How:**
1. Identify code smells
2. Make ONE improvement
3. Run tests → Must still PASS
4. Repeat until clean
5. Final test run → All PASS

**Example (JavaScript):**
```javascript
// Before refactor (works but has duplication)
function calculateTotal(items) {
  let sum = 0;
  for (let i = 0; i < items.length; i++) {
    sum = sum + items[i].price;
  }
  return sum;
}

// After refactor (cleaner, no duplication)
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Run: npm test
// Expected: PASS - behavior unchanged
```

**Common Refactorings:**
- Extract duplicated code into functions
- Rename variables for clarity
- Simplify complex conditionals
- Remove dead code
- Improve error messages

**Red Flags:**
- Tests fail after refactoring → Revert, smaller steps
- Changing behavior during refactor → That's a new feature, needs new test
- Skipping test runs → Run tests after EACH change
- "I'll refactor later" → Do it now while context is fresh

## The Full Cycle

```
1. 🔴 RED
   ↓
   Write failing test
   ↓
   Run test → FAIL
   ↓
2. 🟢 GREEN
   ↓
   Write minimal code
   ↓
   Run test → PASS
   ↓
   Run all tests → PASS
   ↓
3. 🔵 REFACTOR
   ↓
   Improve structure
   ↓
   Run tests → PASS
   ↓
   REPEAT for next behavior
```

## Working with Existing Code

**When modifying existing code:**

1. **First:** Write a test for current behavior (characterization test)
2. **Run it:** Should PASS (proves test works)
3. **Then:** Write test for NEW behavior
4. **Run it:** Should FAIL
5. **Modify code:** Make new test pass
6. **Run all tests:** Both old and new should PASS

**Example:**
```javascript
// Existing function (no tests)
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Step 1: Characterization test (current behavior)
test('calculateTotal works with existing behavior', () => {
  const items = [{ price: 10 }, { price: 20 }];
  expect(calculateTotal(items)).toBe(30); // PASSES
});

// Step 2: New test (desired behavior)
test('calculateTotal handles empty array', () => {
  expect(calculateTotal([])).toBe(0); // FAILS (function throws error)
});

// Step 3: Fix implementation
function calculateTotal(items) {
  if (!items || items.length === 0) return 0;
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Step 4: All tests PASS
```

## When Tests Fail

**If test fails during GREEN phase:**
1. Read the error message carefully
2. Check: Is the test correct?
3. Check: Is the implementation correct?
4. Fix the actual problem
5. Don't add "just in case" code

**If test fails during REFACTOR phase:**
1. REVERT the refactoring immediately
2. Take smaller steps
3. Run tests more frequently
4. One change at a time

**If multiple tests fail:**
1. Don't try to fix all at once
2. Comment out failing tests (temporarily)
3. Fix one test at a time
4. Uncomment and verify

## Common Mistakes

### Mistake 1: Writing Code Before Test

❌ **Wrong:**
```javascript
// Wrote this first
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Then wrote test
test('it works', () => {
  expect(calculateTotal([{ price: 10 }])).toBe(10);
});
```

✅ **Right:**
```javascript
// Write test FIRST
test('calculateTotal sums prices', () => {
  expect(calculateTotal([{ price: 10 }])).toBe(10);
});
// Run: FAIL - calculateTotal not defined

// THEN write code
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
// Run: PASS
```

### Mistake 2: Testing Too Much at Once

❌ **Wrong:**
```javascript
// One huge test
test('shopping cart does everything', () => {
  const cart = new ShoppingCart();
  cart.addItem({ id: 1, price: 10 });
  cart.addItem({ id: 2, price: 20 });
  cart.removeItem(1);
  cart.applyDiscount('SAVE10');
  expect(cart.total).toBe(18);
});
```

✅ **Right:**
```javascript
// Multiple focused tests
test('addItem increases total', () => {
  const cart = new ShoppingCart();
  cart.addItem({ id: 1, price: 10 });
  expect(cart.total).toBe(10);
});

test('removeItem decreases total', () => {
  const cart = new ShoppingCart();
  cart.addItem({ id: 1, price: 10 });
  cart.removeItem(1);
  expect(cart.total).toBe(0);
});

test('applyDiscount reduces total by 10%', () => {
  const cart = new ShoppingCart();
  cart.addItem({ id: 1, price: 20 });
  cart.applyDiscount('SAVE10');
  expect(cart.total).toBe(18);
});
```

### Mistake 3: Not Running Tests After Each Change

❌ **Wrong:**
```
Write test → Write code → Refactor → Refactor → Refactor → Run tests
                                                             ↑
                                                   Which change broke it?
```

✅ **Right:**
```
Write test → Run (FAIL) → Write code → Run (PASS) → Refactor → Run (PASS) → Refactor → Run (PASS)
             ↑             ↑            ↑            ↑           ↑            ↑           ↑
           Know it fails  Know it      Still        Know it's   Still        Know it's   Still
                          passes       working      safe        working      safe        working
```

## TDD Benefits

**Design Benefits:**
- Interface designed before implementation
- Simpler APIs (only what's needed)
- Loose coupling (tests force it)
- Better names (tests expose unclear names)

**Quality Benefits:**
- Bugs found immediately
- Regressions caught by tests
- Code is testable by design
- High test coverage (free)

**Workflow Benefits:**
- Clear next step (make test pass)
- Built-in progress tracking (passing tests)
- Safe refactoring (tests protect)
- Documentation (tests show usage)

## When NOT to Use TDD

**Legitimate exceptions:**
- Spiking/prototyping (exploring unknowns)
- Throwaway code (demos, experiments)
- Code you'll delete immediately

**But once you decide to keep it:**
1. Delete the spike
2. Write the test
3. Rebuild with TDD

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│ TDD QUICK REFERENCE                     │
├─────────────────────────────────────────┤
│ 🔴 RED                                  │
│ • Write test first                      │
│ • Run → Must FAIL                       │
│ • Read failure message                  │
├─────────────────────────────────────────┤
│ 🟢 GREEN                                │
│ • Write MINIMAL code                    │
│ • Run → Must PASS                       │
│ • Run ALL tests → All PASS              │
├─────────────────────────────────────────┤
│ 🔵 REFACTOR                             │
│ • Clean up code                         │
│ • Run tests after EACH change           │
│ • All tests still PASS                  │
├─────────────────────────────────────────┤
│ REPEAT                                  │
└─────────────────────────────────────────┘

RED FLAGS:
• Code before test → DELETE IT
• Test passes immediately → FIX TEST
• Skipping test runs → RUN THEM
• "Quick fix" without test → STOP
```

## Further Reading

- Kent Beck: "Test-Driven Development by Example"
- Martin Fowler: "Refactoring"
- Uncle Bob: "The Three Laws of TDD"

---

**Remember:** TDD is not about testing. It's about design. The tests are a side effect of good design-first thinking.

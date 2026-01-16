# Dev Implement References

This folder contains extended guidance for implementing features with TDD, verification, and debugging discipline.

## Built-in References

### tdd-reference.md
Complete Test-Driven Development guide:
- The RED-GREEN-REFACTOR cycle
- The Iron Law: NO CODE WITHOUT TEST FIRST
- Working with existing code
- Common mistakes and how to avoid them
- Quick reference card

**Key principle:** Write failing test first, implement to pass, then refactor.

### verification-reference.md
Evidence-based completion verification:
- Evidence requirements (fresh, complete, relevant)
- Verification patterns for different scenarios
- Red flags to avoid ("should work", "looks good")
- Language-specific verification commands
- Manual verification when automated tests don't exist

**Key principle:** NO COMPLETION CLAIMS WITHOUT FRESH EVIDENCE.

### debugging-reference.md
Systematic root cause investigation:
- Four phases: Investigation → Pattern Analysis → Hypothesis → Fix
- The Iron Law: NO FIXES WITHOUT ROOT CAUSE FIRST
- Common debugging patterns
- When to ask for help (after 3 failed attempts)
- Debugging tools by language

**Key principle:** Find root cause BEFORE fixing, not after.

## How Claude Uses These

When you run `/dev-implement`, Claude will:
1. Read constitution.md for technical standards
2. Read all files in this folder for methodology
3. Execute tasks following TDD discipline
4. Apply two-stage review (spec compliance + code quality)
5. Verify completion with evidence before marking done
6. Use systematic debugging when issues arise

## Add Your Own References

Drop files here to customize guidance:

```
references/
├── tdd-reference.md           # Built-in
├── verification-reference.md  # Built-in
├── debugging-reference.md     # Built-in
├── README.md                  # This file
├── our-test-patterns.md       # Your team's testing conventions
├── code-review-checklist.md   # Your review standards
└── debugging-playbook.md      # Your common issues + solutions
```

Claude reads ALL files in this folder, so you can add:
- Team-specific testing patterns
- Language-specific best practices
- Common pitfalls in your codebase
- Debugging playbooks for recurring issues
- Code review checklists

## Integration with Other Skills

**dev-implement** automatically integrates these methodologies:

| Methodology | Reference File | When Used |
|-------------|---------------|-----------|
| TDD | tdd-reference.md | Every task |
| Verification | verification-reference.md | Before marking done |
| Debugging | debugging-reference.md | When tests fail |

You don't invoke these skills separately - they're built into the implementation workflow.

## Key Principles

All three methodologies share core principles:

1. **Discipline over speed** - Shortcuts create more work later
2. **Evidence over assumptions** - Show it works, don't assume
3. **Root cause over symptoms** - Fix the real problem
4. **Small steps over big leaps** - One change at a time

## The Iron Laws

**From TDD:**
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**From Verification:**
```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

**From Debugging:**
```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

These are not suggestions. These are laws.

## Quick Reference

### Before Writing Code
1. Read constitution.md (technical standards)
2. Write failing test (RED)
3. Consult constitution for patterns to follow

### After Writing Code
1. Test passes (GREEN)
2. Refactor to constitution standards (REFACTOR)
3. Spec compliance review
4. Code quality review
5. Verification with evidence
6. Mark complete

### When Tests Fail
1. STOP
2. Systematic debugging (find root cause)
3. Write focused test for the bug
4. Fix root cause
5. Verify with evidence

## Constitution Integration

**Critical:** Implementation must align with project constitution.

Before EVERY code write:
- Read `.shipkit/skills/dev-constitution/outputs/constitution.md`
- Follow architectural patterns specified
- Apply coding standards
- Meet testing requirements
- Validate against performance/security standards

**Red Flag:** Writing code without consulting constitution = violation

## For Subagent Mode

When dispatching implementation subagents, provide:
1. Task description
2. Relevant spec excerpts
3. Constitution standards that apply
4. Reference to these methodology files

**Subagent must follow same discipline:**
- TDD cycle (RED-GREEN-REFACTOR)
- Constitution compliance
- Evidence-based verification

## Common Mistakes

1. **Skipping constitution read** - STOP, read it NOW
2. **Code before test** - DELETE IT, write test first
3. **"Looks good" without evidence** - RUN the command
4. **Quick fix without debugging** - Find root cause first
5. **Skipping reviews** - Both reviews required

## Further Reading

Built-in references contain detailed guidance. Start there.

For deeper learning:
- Kent Beck: "Test-Driven Development by Example"
- Martin Fowler: "Refactoring"
- Robert C. Martin: "Clean Code"
- Michael Feathers: "Working Effectively with Legacy Code"

---

**Remember:** These methodologies work together as a system. TDD prevents bugs, verification proves completion, debugging fixes what slips through. All three enforce discipline that produces quality code.

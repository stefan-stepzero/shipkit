# AI-Assisted Development Gaps Inventory

Systematic catalog of problems in AI-assisted development.

---

## High-Level Gap Categories

| Category | Core Problem | Gap Type | Claude Code Native | Shipkit |
|----------|--------------|----------|-------------------|--------------|
| **A. Context/Memory** | Claude forgets | **True gap** | ❌ Only CLAUDE.md | ✅ Partial (.shipkit/*.md) |
| **B. Quality/Standards** | Inconsistent best practices | **Discipline** | ✅ Capability exists | ❌ No enforcement pattern |
| **C. Verification** | Doesn't consistently verify | **Discipline** | ✅ Tests, browser, linters | ❌ No verification habit |
| **D. Efficiency** | Token/time waste | **Mostly discipline** | ⚠️ Auto-summarization | ❌ No index/habits |
| **E. Continuity** | Transitions lose info | **Discipline** | ✅ Can checkpoint | ✅ Partial (project-status) |
| **F. Communication** | Misalignment | **Discipline** | ✅ Can ask/adjust | ⚠️ Skills ask questions |
| **G. Coordination** | Multi-agent conflict | **Mix** | ⚠️ Basic subagents | ❌ No coordination pattern |
| **H. Knowledge** | Outdated/incomplete | **Discipline** | ✅ Skills/MCP/web | ⚠️ External skills help |
| **I. Safety** | Prevent damage | **Mostly solved** | ✅ Permission system | N/A |
| **J. Workflow** | Sequencing work | **Discipline** | ⚠️ TodoWrite (basic) | ✅ Lite workflow skills |

### Legend
- ✅ Good coverage
- ⚠️ Partial/basic
- ❌ Not addressed

### Claude Code Native Capabilities

| Category | What Claude Code Provides |
|----------|--------------------------|
| Context | CLAUDE.md file, .claude/settings.json |
| Quality | Nothing built-in |
| Verification | Nothing built-in |
| Efficiency | Auto-summarization when context fills |
| Continuity | Auto-summarization, session history |
| Communication | Nothing systematic |
| Coordination | Subagent spawning (Task tool), basic parallelism |
| Knowledge | Skills system (.claude/skills/), MCP servers |
| Safety | Permission system, dangerous command warnings, sandbox mode |
| Workflow | TodoWrite tool for task tracking |

### Best Community Solutions

| Category | Solution | Source |
|----------|----------|--------|
| Context/Memory | Planning files, work logs | obra/superpowers |
| Quality/Standards | Domain skills that include quality steps | vercel-labs, anthropics/skills |
| Verification | verification-before-completion (workflow discipline) | obra/superpowers |
| Efficiency | No systematic solution yet | - |
| Continuity | finishing-a-development-branch | obra/superpowers |
| Communication | ask-questions-if-underspecified | trailofbits/skills |
| Coordination | dispatching-parallel-agents, subagent-driven-development | obra/superpowers |
| Knowledge | skills.sh ecosystem, MCP servers for APIs | Various |
| Safety | Claude Code native is sufficient | - |
| Workflow | writing-plans, executing-plans, brainstorming | obra/superpowers |

### Key Insight: Capability vs Discipline

**Most "gaps" are not missing capabilities but missing habits.**

After applying scrutiny to each category:

| Gap Type | Count | Examples |
|----------|-------|----------|
| **True capability gaps** | 1-2 | Memory persistence (A), task dependencies (J) |
| **Discipline gaps** | 7-8 | Quality (B), Verification (C), Efficiency (D), Communication (F), Knowledge (H), Workflow (J) |
| **Mostly solved** | 1 | Safety (I) - Claude Code handles this |
| **Mix** | 1 | Coordination (G) - basic capability, no patterns |

**Solutions for discipline gaps:**
1. Skill instructions that enforce habits ("after X, always do Y")
2. Checklists in context files (standards.md)
3. Phase gates ("verify before moving on")
4. Stored preferences (preferences.md)

**obra/superpowers** understands this - their `verification-before-completion` skill doesn't add capability, it enforces discipline.

---

## Category Details

### A. Context/Memory
> "What do I need to know?"

**True capability gap** - Claude literally cannot persist memory between sessions.

| Capability | Exists? | Gap |
|------------|---------|-----|
| Read files | ✅ Yes | - |
| Write files | ✅ Yes | - |
| Remember between sessions | ❌ No | True gap |

**Solution:** Persist to files. This IS a capability gap that requires workaround (files).

| Specific Gap | Shipkit Status |
|--------------|----------------|
| Project decisions | ✅ why.md, stack.md |
| Code structure | ❌ Needs codebase-index |
| User preferences | ❌ Needs preferences.md |
| Past corrections | ❌ Needs learnings.md |

**Verdict: Real capability gap requiring file-based workaround**

### B. Quality/Standards
> "Am I doing it right?"

**Not a capability gap - a workflow discipline gap.**

Claude *can* apply best practices but doesn't consistently do so unless instructed.

| Capability | Exists? | Gap |
|------------|---------|-----|
| Run linters/formatters | ✅ Yes | Not run automatically |
| Check accessibility | ✅ Lighthouse, axe | Not run consistently |
| Security scanning | ✅ Tools exist | Not part of workflow |
| Apply patterns | ✅ Knowledge exists | No enforcement |

**Real gap:** No habit/checklist that says "before finishing, run these quality checks"

| Specific Gap | Shipkit Status |
|--------------|----------------|
| Quality checklist | ❌ Needs standards.md with checks |
| Auto-run linters | ❌ Could be hook or skill step |
| Project-specific standards | ❌ Needs standards.md |

### C. Verification/Correctness
> "Did it actually work?"

**Not a capability gap - a workflow discipline gap.**

Claude Code has full verification capabilities:
- Run unit/integration tests (`npm test`)
- Browser automation (Chrome extension)
- Inspect live running app
- Run type checker, linter
- Check build succeeds

| Capability | Exists? | Gap |
|------------|---------|-----|
| Run tests | ✅ Yes | Not always run after changes |
| Test live app | ✅ Chrome extension | Not consistently used |
| Type checking | ✅ Yes | Not always checked |
| Build verification | ✅ Yes | Not always verified |

**Real gap:** No pattern for *when* and *what* to verify

| Specific Gap | Shipkit Status |
|--------------|----------------|
| "Verify before proceeding" habit | ❌ Needs skill instructions |
| Verification checklist | ❌ Needs standards.md |
| Phase gates | ❌ "Don't move on until verified" |

### D. Efficiency/Resources
> "Am I being wasteful?"

**Mostly discipline gap** - Claude can be efficient, but defaults to thorough exploration.

| Capability | Exists? | Gap |
|------------|---------|-----|
| Read index file first | ✅ Yes | No habit of checking for index |
| Be concise | ✅ Yes | Defaults to verbose |
| Skip unnecessary exploration | ✅ Yes | Defaults to thorough |
| Know remaining token budget | ❌ No | True capability gap (platform) |

**Real gaps:**
- No "check for index before exploring" discipline
- No user preference for verbosity level
- Token budget awareness (platform limitation)

| Specific Gap | Type | Shipkit Status |
|--------------|------|----------------|
| Codebase exploration loops | Discipline | ❌ Needs codebase-index + habit |
| Verbose explanations | Discipline | ❌ Needs preferences.md |
| Repeated work across sessions | Discipline | ⚠️ Partial (context files help) |
| Token budget awareness | True gap | ❌ Platform-level issue |

**Verdict: Mostly discipline, one true platform gap (token awareness)**

### E. Continuity/Handoffs
> "How do I pick up where I left off?"

**Mostly discipline gap** - Claude can write checkpoints and summaries.

| Capability | Exists? | Gap |
|------------|---------|-----|
| Write checkpoint/summary | ✅ Yes | No habit of doing it |
| Read previous state | ✅ Yes | No standard location |
| Detect context filling up | ❌ Partial | Auto-summarization exists but not controlled |
| Save before overflow | ✅ Yes | No trigger/habit |

**Real gaps:**
- No "checkpoint before context fills" discipline
- No standard checkpoint format/location
- Auto-summarization not user-controlled

| Specific Gap | Type | Shipkit Status |
|--------------|------|----------------|
| Session start | Discipline | ✅ shipkit-session-start hook |
| Phase transitions | Discipline | ✅ shipkit-project-status |
| Context overflow | Discipline | ❌ No checkpoint pattern |
| Multi-session tasks | Discipline | ❌ Needs active-task.md |

**Verdict: Discipline gap - capabilities exist, patterns don't**

### F. Communication/Understanding
> "Do I understand what you want?"

**Discipline/calibration gap** - Claude can ask questions and adjust style.

| Capability | Exists? | Gap |
|------------|---------|-----|
| Ask clarifying questions | ✅ Yes | Inconsistent (too many/few) |
| Adjust verbosity | ✅ Yes | No user preference stored |
| Confirm understanding | ✅ Yes | No habit |
| Know when to stop | ✅ Yes | Sometimes over-delivers |

**Real gaps:**
- No stored preference for communication style
- No calibration of when to ask vs assume
- Inconsistent application

| Specific Gap | Type | Shipkit Status |
|--------------|------|----------------|
| Clarifying requirements | Discipline | ✅ Skills ask questions |
| Over/under explaining | Discipline | ❌ Needs preferences.md |
| Knowing when done | Discipline | ❌ No pattern |
| Asking vs assuming | Calibration | ❌ No calibration stored |

**Verdict: Discipline + needs preferences.md for calibration**

### G. Coordination/Collaboration
> "How do we work together?"

**Mix of capability and discipline** - Basic coordination exists, advanced patterns don't.

| Capability | Exists? | Gap |
|------------|---------|-----|
| Spawn subagents | ✅ Task tool | - |
| Parallel execution | ✅ Yes | No coordination pattern |
| Share context between agents | ⚠️ Partial | Via files only |
| Prevent conflicts | ❌ No | No locking/coordination |
| Merge parallel work | ✅ Git exists | No pattern |

**Real gaps:**
- No coordination protocol between agents
- No conflict prevention (file locking)
- No pattern for merging parallel work

| Specific Gap | Type | Shipkit Status |
|--------------|------|----------------|
| Parallel subagents | Capability exists | ❌ No coordination pattern |
| Team conventions | Discipline | ❌ Could be in standards.md |
| Conflict prevention | True gap | ❌ No pattern |
| Shared context | Discipline | ⚠️ Via files (partial) |

**Verdict: Mix - basic capability exists, coordination patterns don't**

### H. Knowledge/Currency
> "What don't I know?"

**Mix of capability and discipline** - Can load knowledge, doesn't consistently do so.

| Capability | Exists? | Gap |
|------------|---------|-----|
| Load skills | ✅ .claude/skills/ | No habit of loading relevant ones |
| Fetch web content | ✅ WebFetch tool | No pattern for docs |
| Use MCP servers | ✅ Yes | Requires setup |
| Acknowledge knowledge limits | ✅ Yes | Inconsistent |

**Real gaps:**
- No habit of checking if knowledge is current
- No pattern for "load docs for this library"
- No awareness of what skills are available

| Specific Gap | Type | Shipkit Status |
|--------------|------|----------------|
| Library updates | Discipline | ⚠️ External skills help |
| API changes | Discipline | ❌ No pattern for loading docs |
| Domain expertise | Discipline | ⚠️ External skills help |
| Project-specific knowledge | Solved | ✅ .shipkit/ files |

**Verdict: Capability exists (skills, MCP, web), discipline gap in using them**

### I. Safety/Risk
> "Could this cause damage?"

**Largely solved at platform level** - Claude Code has comprehensive safety guardrails.

| Capability | Exists? | Gap |
|------------|---------|-----|
| Dangerous command warnings | ✅ Yes | - |
| Permission system | ✅ Yes | - |
| Sandbox mode | ✅ Yes | - |
| Git safety (no force push main) | ✅ Yes | - |
| Confirm destructive actions | ✅ Yes | Inconsistent application |
| Production awareness | ⚠️ Partial | No environment context |

**What Claude Code handles well:**
- Warns on destructive bash commands
- Permission prompts for risky operations
- Won't force push to main
- Sandbox mode for untrusted operations

**Real gaps:**
- No awareness of "this is production" vs "this is dev"
- No confirmation pattern for data deletion operations
- Security vulnerabilities are quality/discipline issue (covered in B)

| Specific Gap | Type | Shipkit Status |
|--------------|------|----------------|
| Destructive git operations | Solved | ✅ Claude Code has guardrails |
| Production deployments | Environment awareness | ❌ Needs environment.md |
| Data deletion | Discipline | ❌ No confirmation pattern |
| Security vulnerabilities | Discipline | Part of quality/standards |

**Verdict: Mostly solved by Claude Code. Remaining gaps are discipline or environment context.**

### J. Workflow/Process
> "What's the right order?"

**Capability exists, patterns vary** - Claude can plan and sequence, but needs structure.

| Capability | Exists? | Gap |
|------------|---------|-----|
| Task decomposition | ✅ Yes | No standard format |
| Phase awareness | ✅ Yes | No project phase tracking |
| TodoWrite tool | ✅ Yes | Basic, no dependencies |
| Sequential execution | ✅ Yes | - |
| Parallel execution | ✅ Task tool | No coordination pattern |
| Prioritization | ✅ Yes | No criteria stored |

**What Claude Code provides:**
- TodoWrite for task tracking
- Task tool for subagent decomposition
- Can create and follow plans

**Real gaps:**
- No standard planning format
- No phase tracking (which Shipkit solves)
- TodoWrite doesn't handle dependencies
- No prioritization criteria persistence

| Specific Gap | Type | Shipkit Status |
|--------------|------|----------------|
| Task decomposition | Discipline | ✅ shipkit-plan skill |
| Phase sequencing | Discipline | ✅ Lite workflow skills + project-status |
| Dependencies | True gap | ❌ TodoWrite lacks dependency support |
| Prioritization | Discipline | ❌ No criteria stored (needs priorities.md?) |
| Planning format | Discipline | ⚠️ Lite skills provide structure |

**Verdict: Mostly discipline - Shipkit workflow skills address this. One true gap: task dependencies.**

---

## Current Coverage

What Shipkit already solves:

| Problem | Solution | Status |
|---------|----------|--------|
| Project purpose/decisions | `why.md` | ✅ Solved |
| Technology choices | `stack.md` | ✅ Solved |
| Architecture decisions | `architecture.md` | ✅ Solved |
| Current phase/status | `project-status.md` | ✅ Solved |
| Phase-appropriate workflow | Lite skills | ✅ Solved |

---

## Identified Gaps

### 1. Code Structure Persistence

**Problem:** Claude re-explores the codebase every session.

**Symptoms:**
- Token waste on list → read → filter → repeat
- Same exploration every conversation
- Slow "let me understand the project" phase

**Potential Solution:** Codebase index file

**Status:** Documented in `CODEBASE-INDEX-DESIGN.md`

---

### 2. Phase-Appropriate External Skills

**Problem:** No way to load relevant external skills based on project phase.

**Symptoms:**
- All skills loaded all the time, or none
- User doesn't know which skills exist
- Skills.sh approach is popularity-based, not context-based

**Potential Solution:** Skill catalog + recommender + loader

**Status:** Documented in `SKILL-ECOSYSTEM-REDESIGN.md`

---

### 3. User Preferences Persistence

**Problem:** Claude re-learns user's working style every session.

**Examples of lost preferences:**
- Code style (tabs/spaces, naming conventions)
- Communication style (concise vs detailed explanations)
- Commit message format
- Testing approach (TDD, test after, minimal tests)
- Review thoroughness
- How much to ask vs assume

**Symptoms:**
- Claude asks same clarifying questions each session
- Output style inconsistent across sessions
- User repeatedly corrects same patterns

**Potential Solution:**
```markdown
# .shipkit/preferences.md

## Code Style
- Indentation: 2 spaces
- Quotes: single
- Naming: camelCase for functions, PascalCase for components

## Communication
- Be concise, skip explanations unless asked
- Don't ask for confirmation on small changes
- Group related changes in single commits

## Testing
- Write tests for new functions
- Don't test obvious getters/setters
- Prefer integration tests over unit tests
```

**Status:** Not yet designed

---

### 4. Learning from Corrections

**Problem:** When user corrects Claude, that learning is lost next session.

**Examples:**
- "Don't use that library, use X instead"
- "Our API returns data differently than you assumed"
- "That approach doesn't work in our codebase because..."
- "We tried that before, it failed because..."

**Symptoms:**
- Same mistakes repeated across sessions
- User frustration from re-explaining
- No institutional memory of failures

**Potential Solution:**
```markdown
# .shipkit/learnings.md

## Corrections Log

### 2025-01-23
- Don't use moment.js, use date-fns (moment is deprecated)
- API returns { data: [] } not { results: [] }
- Auth middleware must come before rate limiter

### 2025-01-20
- Don't refactor utils/ - it's intentionally simple
- Tests go in __tests__ folder, not .test.ts files
```

**Status:** Not yet designed

---

### 5. Context Window Overflow

**Problem:** Mid-task, context fills up. No graceful way to continue.

**Symptoms:**
- Claude's responses degrade as context fills
- User starts new session, loses all context
- Partial work with no clear handoff
- "I've lost track of what we were doing"

**Current state:**
- Automatic summarization exists but isn't controlled
- No explicit "checkpoint" pattern
- No way to say "save state, I'll continue later"

**Potential Solution:**
```markdown
# Checkpoint pattern

## Before context overflow:
/checkpoint
→ Saves current task state to .shipkit/checkpoint.md
→ Lists completed steps, pending steps, key decisions
→ Can be resumed in new session

## In new session:
/resume
→ Loads checkpoint
→ Claude continues from where it left off
```

**Status:** Not yet designed

---

### 6. Verification Before Proceeding

**Problem:** No systematic way to verify Claude's work before moving on.

**Symptoms:**
- Bugs discovered late
- Wrong assumptions compound
- User unsure if they should proceed
- "Did it actually work?"

**Current state:**
- Some skills have "verify" steps
- No universal pattern
- Relies on user to check

**Potential Solution:**
- Verification as a standard skill phase
- Automated checks where possible
- Explicit "confidence level" from Claude
- Checklists before phase transition

```markdown
## After implementation:
/verify
→ Runs relevant tests
→ Checks against spec
→ Lists assumptions made
→ Confidence: High/Medium/Low
→ Recommends: Proceed / Review needed / Blocked
```

**Status:** Not yet designed

---

### 7. External Documentation Loading

**Problem:** Claude's knowledge of libraries/APIs may be outdated.

**Symptoms:**
- Claude suggests deprecated APIs
- Incorrect function signatures
- Missing new features
- "Based on my knowledge..." disclaimers

**Examples:**
- React 19 features
- New Tailwind v4 syntax
- Latest Stripe API changes
- Library-specific patterns

**Potential Solution:**
- Fetch current docs into context
- Library-specific skills (some exist on skills.sh)
- Documentation index with URLs
- `/load-docs stripe` command

**Status:** Partially addressed by external skills, but no systematic approach

---

### 8. Token Budget Awareness

**Problem:** Claude doesn't know how much context space remains.

**Symptoms:**
- Verbose responses when space is tight
- No prioritization of what to keep
- Can't plan for multi-step tasks
- Surprised by context overflow

**Potential Solution:**
- Token budget indicator (system level)
- Claude adjusts verbosity based on remaining space
- Explicit "we have X tokens left" awareness
- Prioritization: what to keep vs summarize vs drop

**Status:** Likely needs Claude Code platform support, not just Shipkit

---

### 9. Multi-Session Task Continuity

**Problem:** Large tasks spanning multiple sessions lose continuity.

**Current state:**
- `project-status.md` helps at project level
- No task-level continuity
- "Where was I?" at start of each session

**Potential Solution:**
```markdown
# .shipkit/active-task.md

## Current Task
Implementing user authentication

## Progress
- [x] Database schema for users
- [x] Password hashing utility
- [ ] Login endpoint
- [ ] JWT token generation
- [ ] Middleware for protected routes

## Context
- Using bcrypt for passwords
- JWT with 24h expiry
- Refresh tokens stored in Redis

## Next Steps
1. Create POST /auth/login endpoint
2. Return JWT on successful login
```

**Status:** Not yet designed

---

### 10. Best Practices Enforcement

**Problem:** Claude knows many approaches but doesn't consistently apply best practices.

**Symptoms:**
- Inconsistent code quality
- Missing accessibility considerations
- Security anti-patterns
- Non-idiomatic code for the framework
- "It works but isn't production-ready"

**Examples by domain:**
| Domain | Best Practices Often Missed |
|--------|----------------------------|
| Frontend | Accessibility, responsive design, component patterns, performance |
| Backend | Error handling, input validation, API design, logging |
| Database | Schema normalization, indexing, query optimization |
| Security | OWASP top 10, auth patterns, secrets management |
| Testing | Coverage, test isolation, mocking patterns |
| DevOps | CI/CD patterns, infrastructure as code |

**Why this happens:**
- Claude has broad knowledge but no enforcement
- Training data includes both good and bad patterns
- No project-specific "our standards" reference
- Context doesn't include quality requirements

**Current solutions (external):**
- `vercel-react-best-practices` - React patterns
- `frontend-design` - UI/UX standards
- `better-auth-best-practices` - Auth patterns
- `expo/skills` - React Native patterns

**Potential Shipkit solution:**

```markdown
# .shipkit/standards.md

## Code Standards

### Frontend
- All interactive elements must be keyboard accessible
- Use semantic HTML (nav, main, section, not div soup)
- Mobile-first responsive design
- Loading states for async operations

### API Design
- RESTful conventions (plural nouns, HTTP verbs)
- Consistent error response format
- Input validation on all endpoints
- Rate limiting on public endpoints

### Security
- Never log sensitive data
- Parameterized queries only
- Auth middleware on protected routes
- HTTPS only in production

### Testing
- Unit tests for business logic
- Integration tests for API endpoints
- No tests for trivial getters/setters
```

**Or:** Domain-specific skills that get loaded based on stack.md

```
Stack: React + Node + PostgreSQL
→ Auto-load: react-best-practices, node-security, postgres-patterns
```

**Status:** Partially addressed by external skills, but no systematic approach

---

### 11. Parallel Workstream Coordination

**Problem:** Multiple related tasks happening in parallel (or with subagents) can conflict.

**Symptoms:**
- Duplicate work
- Conflicting changes
- Merge conflicts
- Inconsistent approaches

**Potential Solution:**
- Shared context between agents
- "Lock" on files being modified
- Coordination protocol
- Consistent decision-making

**Status:** Advanced problem, not yet scoped

---

## Priority Assessment

| Gap | Impact | Effort | Priority |
|-----|--------|--------|----------|
| Code structure persistence | High | Low | 🔴 High |
| User preferences | High | Low | 🔴 High |
| Learning from corrections | High | Low | 🔴 High |
| Best practices enforcement | High | Medium | 🔴 High |
| External skills loading | Medium | Medium | 🟡 Medium |
| Context overflow/checkpoint | High | Medium | 🟡 Medium |
| Verification patterns | Medium | Medium | 🟡 Medium |
| Multi-session continuity | Medium | Low | 🟡 Medium |
| External docs loading | Medium | High | 🟢 Low |
| Token budget awareness | Low | High | 🟢 Low |
| Parallel coordination | Low | High | 🟢 Low |

---

## Next Steps

1. **High priority, low effort** - Design preferences.md and learnings.md patterns
2. **Already in progress** - Codebase index, skill ecosystem
3. **Medium priority** - Checkpoint/resume pattern, verification
4. **Future** - External docs, token awareness, parallel coordination

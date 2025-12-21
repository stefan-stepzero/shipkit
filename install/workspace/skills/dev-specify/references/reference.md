# Feature Specification Reference

## Purpose

Feature specifications translate natural language feature descriptions into structured technical requirements, grounded in product artifacts and technical constraints.

**Key principle:** Extract from product artifacts (user stories, interaction design, brand guidelines) and technical constitution. Don't invent requirements.

---

## What Makes a Good Spec

### Clear Problem Statement
❌ **Vague:** "Users need better auth"
✅ **Clear:** "Users abandon signup (40% drop-off at password creation, per analytics) because password requirements are unclear and validation is inconsistent"

### Measurable Success Criteria
❌ **Unmeasurable:** "Improve user experience"
✅ **Measurable:** "Reduce signup drop-off from 40% to <15% (target from success metrics)"

### Testable Requirements
❌ **Untestable:** "Should be fast"
✅ **Testable:** "Login response time <500ms (p95), per constitution performance targets"

### Appropriate Scope
❌ **Too broad:** "Build authentication system" (multiple features)
✅ **Right-sized:** "Add OAuth login (Google, GitHub)" (single deliverable feature)

---

## Extracting from Product Artifacts

### From User Stories (prod-user-stories)

**What to extract:**
- Primary user story this feature implements
- Acceptance criteria → Functional requirements
- User personas → UX considerations
- Priority (MoSCoW) → Scope decisions

**Example:**
```
User Story: "As a mobile user, I want to save articles offline
            so I can read during my commute"

Extract to Spec:
- Problem: Mobile users lose access when offline
- Solution: Offline article storage
- User Journey: Save → Sync → Read offline
- Success: Users can access saved articles without network
```

### From Interaction Design (prod-interaction-design)

**What to extract:**
- Relevant user journey steps
- Screen flows
- Interaction patterns
- Component needs

**Example:**
```
Interaction Design: "Article Reading Journey"
Step 5: User bookmarks article for later

Extract to Spec:
- UI Requirements: Bookmark button (heart icon, per brand)
- Interaction: Single tap to save, visual feedback
- Edge case: Handle already-bookmarked articles
```

### From Brand Guidelines (prod-brand-guidelines)

**What to extract:**
- Visual style requirements
- Component usage
- Tone of voice for messaging
- Accessibility standards

**Example:**
```
Brand Guidelines: "Friendly, conversational tone. Icons: Feather set"

Extract to Spec:
- UI Requirements: Use Feather icons
- Error messages: "Oops! Couldn't save that. Try again?" (not "ERROR 401")
- Accessibility: WCAG AA minimum
```

### From Jobs-to-be-Done (prod-jobs-to-be-done)

**What to extract:**
- Core job this feature helps complete
- Forces (pushes/pulls)
- Anxieties/habits to address

**Example:**
```
JTBD: "When I'm researching, I want to save interesting articles,
       so I can read them deeply later without losing them"

Extract to Spec:
- Problem: Users fear losing interesting content
- Solution: One-click save
- Anxiety to address: "Will I remember where I saved this?"
  → Include search/tags in scope
```

### From Success Metrics (prod-success-metrics)

**What to extract:**
- Performance targets
- Reliability requirements
- Metrics to track

**Example:**
```
Success Metrics: "95% task completion rate, <200ms p95 latency"

Extract to Spec:
- Performance: Save article <200ms
- Success Criteria: 95% of save attempts succeed
- Metrics to track: Save success rate, save latency
```

### From Technical Constitution (dev-constitution)

**What to extract:**
- Tech stack constraints
- Architecture patterns to follow
- Quality standards (testing, security)
- Performance targets

**Example:**
```
Constitution: "REST APIs, JWT auth, 80% test coverage"

Extract to Spec:
- Technical Constraints: Use REST endpoint, JWT tokens
- Quality Standards: Unit + integration tests required
- Security: Validate JWT on server
```

---

## Spec Template Sections Explained

### 1. Overview
**Purpose:** High-level understanding in <5 minutes

**Problem:** What user/business problem exists?
- Extract from user stories (pain points)
- Extract from JTBD (job not being done well)
- Be specific (not "users are frustrated")

**Solution:** What are we building?
- One paragraph description
- High-level approach (not implementation details)

**Value:** Why is this worth building?
- User value (from user stories)
- Business value (from strategy/metrics)

### 2. User Stories
**Purpose:** Link spec to product requirements

**Primary User Story:** The main story this implements
- Copy directly from prod-user-stories
- Include acceptance criteria

**Related User Stories:** Supporting stories
- Secondary stories this partially addresses
- Future stories this enables

### 3. Scope
**Purpose:** Prevent scope creep, set boundaries

**In Scope:**
- Specific functionality included
- Clear, bulleted list
- Reference user story acceptance criteria

**Out of Scope:**
- Explicitly NOT included (prevents assumptions)
- Future considerations (but not this iteration)

### 4. User Experience
**Purpose:** Define user-facing behavior

**User Journey:**
- Extract from prod-interaction-design
- Show user's path through the feature
- Include entry/exit points

**Key Interactions:**
- User actions and system responses
- Happy path flow
- Critical decision points

**UI Requirements:**
- Visual style (from brand guidelines)
- Components needed (buttons, forms, modals)
- Responsive behavior (mobile/tablet/desktop)

### 5. Functional Requirements
**Purpose:** Testable behavior specifications

**Core Functionality:**
- Each requirement = one testable behavior
- Format: **[Name]**
  - Description: What it does
  - Acceptance: How to verify (Given-When-Then)

**Business Rules:**
- Constraints on behavior
- Validation logic
- State transitions

**Validation Rules:**
- Input validation
- Error conditions
- Data constraints

### 6. Non-Functional Requirements
**Purpose:** Quality attributes

**Performance:**
- Response time targets (from constitution/metrics)
- Throughput requirements
- Resource constraints

**Security:**
- Authentication requirements
- Authorization rules
- Data protection (encryption, PII handling)

**Reliability:**
- Uptime targets (from success metrics)
- Error handling approach
- Degraded mode behavior

**Accessibility:**
- WCAG level (from brand guidelines)
- Keyboard navigation
- Screen reader support

### 7. Technical Constraints
**Purpose:** Development guardrails

Extract from dev-constitution:
- Tech stack to use
- Architecture patterns to follow
- Quality standards (testing, coverage)
- Performance targets

### 8. Dependencies
**Purpose:** Identify blockers and prerequisites

**External Dependencies:**
- Third-party services (APIs, libraries)
- Accounts/credentials needed
- Vendor limitations

**Internal Dependencies:**
- Features that must exist first
- Shared components required
- Database schema changes

### 9. Data Requirements
**Purpose:** High-level data needs

**Data Models:**
- Key entities (defer schema details to dev-plan)
- Relationships
- Critical fields

**Data Flow:**
- Where data comes from
- How it's processed
- Where it's stored
- How it's presented

### 10. Edge Cases & Error Handling
**Purpose:** Handle the unhappy paths

**Edge Cases:**
- Unusual but valid scenarios
- Boundary conditions
- Race conditions

**Error States:**
- What can go wrong
- User-facing error messages
- Recovery actions

### 11. Success Criteria
**Purpose:** Definition of done

**Done When:**
- Checklist of completion criteria
- Link to user story acceptance criteria
- Include testing/review requirements

**Metrics:**
- What to measure (from success metrics)
- Success thresholds
- How to track

### 12. Open Questions
**Purpose:** Track ambiguities

Use `[NEEDS_CLARIFICATION: question]` markers:
- Questions for product team
- Technical unknowns
- Decisions deferred to dev-plan

Run `/dev-specify --clarify` to resolve these.

---

## Spec Quality Checklist

Before finalizing a spec, verify:

**Grounded in Artifacts:**
- [ ] References specific user stories from prod-user-stories
- [ ] Extracts UI requirements from interaction-design
- [ ] Follows brand guidelines visual/tone direction
- [ ] Aligns with technical constitution constraints
- [ ] Includes success metrics targets

**Clear and Testable:**
- [ ] Problem statement is specific (not vague)
- [ ] Requirements are testable (Given-When-Then)
- [ ] Success criteria are measurable
- [ ] Scope is well-defined (in/out explicit)

**Appropriate Detail Level:**
- [ ] High-level (not implementation code)
- [ ] Enough detail for dev-plan to design architecture
- [ ] Defers technical decisions to dev-plan
- [ ] Defers task breakdown to dev-tasks

**Complete:**
- [ ] All template sections filled (or marked N/A with reason)
- [ ] Dependencies identified
- [ ] Edge cases considered
- [ ] Error handling specified

**Clarified:**
- [ ] No [NEEDS_CLARIFICATION] markers left (or explicitly deferred)
- [ ] Assumptions documented
- [ ] Open questions tracked

---

## Common Mistakes

### ❌ Inventing Requirements
**Bad:** Adding features not in user stories
**Why:** Scope creep, not grounded in user needs
**Fix:** Only spec what's in user stories + product artifacts

### ❌ Over-Specifying Technical Details
**Bad:** "Use PostgreSQL JSONB column with GIN index for tags"
**Why:** That's architecture (belongs in dev-plan)
**Fix:** "Store tags for search/filter" (dev-plan chooses implementation)

### ❌ Under-Specifying User Behavior
**Bad:** "User can search articles"
**Why:** Too vague, not testable
**Fix:** "User enters search term → sees results <2s, ranked by relevance, with highlights"

### ❌ Ignoring Product Artifacts
**Bad:** Making up user journeys without checking interaction-design
**Why:** Inconsistent with product vision
**Fix:** Extract journey from prod-interaction-design, adapt to feature

### ❌ Missing Error Handling
**Bad:** Only specifying happy path
**Why:** Real users encounter errors
**Fix:** Specify error states, user messages, recovery actions

### ❌ Vague Success Criteria
**Bad:** "Works well"
**Why:** Unmeasurable, subjective
**Fix:** "95% save success rate, <200ms p95 latency" (from metrics)

---

## [NEEDS_CLARIFICATION] Markers

When requirements are ambiguous, add clarification markers:

```markdown
### Authentication
Users can log in with email/password or OAuth.

[NEEDS_CLARIFICATION: Which OAuth providers? Google? GitHub? Facebook?]
[NEEDS_CLARIFICATION: Password requirements? From constitution or custom?]
```

**When to use:**
- User story is vague on detail
- Multiple valid interpretations exist
- Technical approach unclear (but that's okay - dev-plan will decide)
- Dependency on external decision

**How to resolve:**
Run `/dev-specify --clarify --spec N-feature-name`
- Claude reads spec
- Asks user the clarification questions
- Updates spec with answers
- Removes markers

---

## Working with --clarify

**Initial spec creation:**
```bash
/dev-specify "Add user authentication"
# Creates specs/1-user-authentication/spec.md
# May include [NEEDS_CLARIFICATION] markers for ambiguities
```

**Resolve clarifications:**
```bash
/dev-specify --clarify --spec 1-user-authentication
# Claude finds [NEEDS_CLARIFICATION] markers
# Asks questions interactively
# Updates spec with answers
```

**Iterative refinement:**
- You can run --clarify multiple times
- Each run resolves more questions
- Goal: Zero [NEEDS_CLARIFICATION] markers before dev-plan

---

## Working with --update

**Update existing spec:**
```bash
/dev-specify --update --spec 1-user-authentication
# Archives old version to spec-YYYYMMDD-HHMMSS.md.bak
# Claude helps update spec with new information
```

**When to update:**
- User stories changed
- Product requirements evolved
- After user feedback
- Scope adjustments needed

**Auto-archiving:**
- Old versions saved with timestamp
- Can compare changes: `diff spec.md spec-20250115-143022.md.bak`
- Maintains change history

---

## Examples

### Good Spec Excerpt

```markdown
## Problem
Mobile users (60% of traffic, per analytics) abandon article saves when offline.
Currently save button shows generic error "Network unavailable" with no recovery.
User story #7: "As a mobile user, I want to save articles offline..."

## Solution
Queue article saves locally when offline, auto-sync when connection restores.
Provide clear feedback on sync status.

## Functional Requirements

1. **Offline Save Queueing**
   - Description: When user taps save while offline, queue operation locally
   - Acceptance:
     - Given: User is offline
     - When: User taps save button
     - Then: Article is queued, UI shows "Saved (will sync)"

2. **Automatic Sync**
   - Description: When connection restores, sync queued saves to server
   - Acceptance:
     - Given: User has queued saves and comes online
     - When: Connection detected
     - Then: Queued saves sync to server within 5s, UI updates to "Saved"

## Success Criteria
- [ ] Users can save articles offline (verified in airplane mode)
- [ ] Queued saves auto-sync when online (verified in network simulator)
- [ ] <5% sync failures (metric to track)
```

### Bad Spec Excerpt

```markdown
## Problem
Users want to save stuff

## Solution
Build a save feature

## Requirements
- Clicking save should save the thing
- It should work
- Make it fast
```

**Why bad:**
- Vague problem (what users? what stuff?)
- No grounding in user stories
- Untestable requirements ("work", "fast")
- No success criteria
- No technical constraints
- No error handling

---

## Quick Reference

| Section | Extract From | Detail Level |
|---------|-------------|--------------|
| Problem | User stories, JTBD | Specific |
| User Stories | prod-user-stories | Direct copy |
| Scope | User story acceptance criteria | Explicit in/out |
| User Journey | prod-interaction-design | User's path |
| UI Requirements | Brand guidelines, interaction design | Components needed |
| Functional Reqs | User stories | Testable (Given-When-Then) |
| Performance | Success metrics, constitution | Measurable targets |
| Security | Constitution, user stories | Auth/data protection |
| Technical Constraints | dev-constitution | Tech stack, patterns |
| Dependencies | User stories, architecture | Blockers |
| Success Criteria | User stories, success metrics | Measurable done |

---

## Remember

1. **Extract, don't invent** - Requirements come from product artifacts
2. **High-level, not implementation** - Defer technical decisions to dev-plan
3. **Testable** - Every requirement should have clear acceptance criteria
4. **Complete** - Address edge cases, errors, non-functionals
5. **Use markers** - [NEEDS_CLARIFICATION] for ambiguities, resolve with --clarify

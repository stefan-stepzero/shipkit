# User Stories

**Product:** [Product Name]
**Created:** [Date]
**Last Updated:** [Date]
**Stage:** [POC/MVP/Established]
**Type:** [B2C/B2B]

---

## Overview

**Purpose of This Document:**
Translate interaction design journeys and product requirements into actionable user stories that guide development. Each story describes a specific piece of value from the user's perspective.

**Source Documents:**
- Interaction Design: `.shipkit/skills/prod-interaction-design/outputs/interaction-design.md`
- Personas: `.shipkit/skills/prod-personas/outputs/personas.md`
- Jobs to Be Done: `.shipkit/skills/prod-jobs-to-be-done/outputs/jobs-to-be-done.md`

---

## User Story Format

All stories follow this structure:

```
As a [persona]
I want to [action]
So that [benefit/outcome]

Acceptance Criteria:
- [ ] Given [context], when [action], then [expected result]
- [ ] [Additional criteria]
- [ ] [Additional criteria]

Priority: [Must Have / Should Have / Nice to Have]
Estimated Effort: [Small / Medium / Large / Extra Large]
Dependencies: [Other stories this depends on]
```

---

## Epic 1: [Epic Name - e.g., User Onboarding]

**Goal:** [What this epic accomplishes]
**Success Metric:** [How we measure success]
**User Journey Stage:** [Which stage from interaction-design.md]

### Story 1.1: [Story Title]

**As a** [persona name]
**I want to** [specific action/capability]
**So that** [clear benefit or outcome]

**Acceptance Criteria:**
- [ ] Given [initial state/context], when [user action], then [observable result]
- [ ] Given [edge case scenario], when [action], then [how system handles it]
- [ ] [Non-functional requirement - e.g., loads in <2 seconds]
- [ ] [Error handling - what happens when things go wrong]
- [ ] [Accessibility requirement if applicable]

**Priority:** [Must Have / Should Have / Nice to Have]

**Estimated Effort:** [S / M / L / XL]
- S (Small): <1 day
- M (Medium): 1-3 days
- L (Large): 3-5 days
- XL (Extra Large): 5-10 days (consider splitting)

**Dependencies:**
- [Story ID or description of prerequisite]

**Technical Notes:**
- [Implementation hints, constraints, or technical considerations]
- [APIs, integrations, or third-party services needed]

**UI/UX Notes:**
- [Screen/component affected]
- [Key interaction patterns]
- [Reference to wireframes/designs if available]

**Test Scenarios:**
1. **Happy Path:** [Describe ideal user flow]
2. **Edge Cases:** [Unusual but valid scenarios]
3. **Error Conditions:** [What can go wrong and how we handle it]

**Definition of Done:**
- [ ] Feature implemented and working
- [ ] Unit tests written and passing
- [ ] Integration tests cover key scenarios
- [ ] Code reviewed and approved
- [ ] Deployed to staging environment
- [ ] Tested by product owner
- [ ] Documentation updated
- [ ] Accessibility verified

---

### Story 1.2: [Next Story in Epic]

[Repeat structure above]

---

## Epic 2: [Next Epic - e.g., Core Workflow]

[Repeat epic structure]

---

## Story Backlog (Unprioritized)

Stories identified but not yet prioritized or assigned to epics.

### [Story Title]

**As a** [persona]
**I want to** [action]
**So that** [benefit]

**Why This Matters:**
[Context on user need or business value]

**Open Questions:**
- [Question 1]
- [Question 2]

---

## Context-Specific Guidance

### For POC Stage

**Focus:**
- Prove core value proposition quickly
- Minimal features to demonstrate concept
- Manual workarounds acceptable
- Speed over polish

**Story Prioritization:**
- Must Have: Only stories that prove/disprove core hypothesis
- Defer: Everything else (even if "important")

**Example Must-Have Stories:**
- User can complete core job-to-be-done
- User experiences "aha!" moment
- User can see value in <5 minutes

**Acceptance Criteria Simplification:**
- Happy path only (skip edge cases)
- Manual data entry okay (skip automation)
- Basic error messages (skip recovery)
- Desktop only (skip mobile)

---

### For MVP Stage

**Focus:**
- Complete happy path for core workflows
- Essential error handling
- Basic polish and professionalism
- Ready for early adopters

**Story Prioritization:**
- Must Have: Core workflows end-to-end
- Should Have: Important error handling, onboarding
- Nice to Have: Convenience features, advanced capabilities

**Example Must-Have Stories:**
- User can sign up and get started
- User can complete all steps in core workflow
- User can recover from common errors
- User data is saved and persistent

**Acceptance Criteria Expansion:**
- Happy path + common errors
- Automated workflows where it saves significant time
- Clear error messages with recovery paths
- Responsive design (mobile-friendly)

---

### For Established Products

**Focus:**
- Feature completeness
- Edge case handling
- Performance optimization
- Advanced user needs

**Story Prioritization:**
- Must Have: Feature parity with competitors, critical gaps
- Should Have: Power user features, optimizations
- Nice to Have: Experimental features, nice-to-haves

**Acceptance Criteria Rigor:**
- All user paths covered
- Comprehensive error handling
- Performance benchmarks met
- Accessibility compliance
- Security requirements
- Analytics instrumentation

---

## Story Templates by Type

### Authentication Story Template

**As a** [persona]
**I want to** sign in with [method]
**So that** I can access my account securely

**Acceptance Criteria:**
- [ ] Given valid credentials, when I submit login form, then I'm redirected to dashboard
- [ ] Given invalid credentials, when I submit, then I see clear error message
- [ ] Given forgotten password, when I click "Forgot", then I receive reset email within 5 minutes
- [ ] Session expires after [X] minutes of inactivity
- [ ] Password must meet security requirements (8+ chars, mix of types)
- [ ] Account locked after 5 failed attempts

---

### CRUD Story Template

**As a** [persona]
**I want to** create/read/update/delete [resource]
**So that** I can [manage my data]

**Acceptance Criteria:**
**Create:**
- [ ] Given valid input, when I submit form, then [resource] is created and I see confirmation
- [ ] Given invalid input, when I submit, then I see validation errors inline
- [ ] Given required fields empty, when I submit, then I see "required" indicators

**Read:**
- [ ] Given [resources] exist, when I view list, then I see all my [resources] sorted by [date]
- [ ] Given no [resources], when I view list, then I see helpful empty state with "Create" CTA
- [ ] Given large dataset, when I scroll, then more items load (infinite scroll or pagination)

**Update:**
- [ ] Given I edit [resource], when I save changes, then updates persist and I see confirmation
- [ ] Given unsaved changes, when I navigate away, then I see "unsaved changes" warning
- [ ] Auto-save every [X] seconds with "Saving..." indicator

**Delete:**
- [ ] Given I click delete, when I confirm, then [resource] is removed and I see confirmation
- [ ] Given I click delete, when I cancel, then [resource] remains unchanged
- [ ] Deleted items moved to trash (recoverable for 30 days) before permanent deletion

---

### Onboarding Story Template

**As a** new user
**I want to** get started quickly
**So that** I experience value before abandoning

**Acceptance Criteria:**
- [ ] Given first visit, when I land, then I see clear value proposition and "Get Started" CTA
- [ ] Given I sign up, when I complete form, then I'm in the product within 60 seconds
- [ ] Given I'm onboarding, when I complete setup, then I reach "aha!" moment within 5 minutes
- [ ] Given I'm stuck, when I look for help, then I see contextual tips at decision points
- [ ] Given I want to skip, when I click skip, then I can access core features immediately
- [ ] Progress indicator shows % complete during multi-step onboarding

---

### Search/Filter Story Template

**As a** [persona]
**I want to** search/filter [items]
**So that** I can find what I need quickly

**Acceptance Criteria:**
- [ ] Given I type query, when I pause typing (300ms), then results update automatically
- [ ] Given search results, when they load, then most relevant items appear first
- [ ] Given no matches, when I search, then I see "No results for '[query]'" with suggestions
- [ ] Given I apply filters, when I select options, then results narrow immediately
- [ ] Given active filters, when I view results, then filter pills show what's applied
- [ ] Given I want to clear, when I click "Clear all", then filters reset and all items show
- [ ] Search includes [fields to search: title, description, tags]
- [ ] Recent searches saved (show last 5 on focus)

---

### Import/Export Story Template

**As a** [persona]
**I want to** import/export data
**So that** I can [migrate data, backup, share]

**Acceptance Criteria:**
**Export:**
- [ ] Given I click export, when I select format (CSV/JSON/PDF), then download starts within 2 seconds
- [ ] Given large dataset (10,000+ items), when I export, then I see progress indicator
- [ ] Exported file includes all fields: [list fields]
- [ ] Filename format: [product]-export-YYYY-MM-DD.csv

**Import:**
- [ ] Given I upload file, when format is valid, then I see preview of data to import
- [ ] Given I upload file, when format is invalid, then I see specific error: "Expected columns: [list]"
- [ ] Given preview, when I confirm import, then I see progress (X of Y imported)
- [ ] Given duplicate items, when I import, then I can choose: skip, overwrite, or create new
- [ ] Given errors in rows, when import completes, then I see log of failed rows with reasons
- [ ] Rollback available if import creates issues

---

### Integration Story Template

**As a** [persona]
**I want to** connect with [third-party service]
**So that** I can [sync data, automate workflow]

**Acceptance Criteria:**
- [ ] Given I click connect, when I authorize, then I return to app with "Connected" status
- [ ] Given connection fails, when I retry, then I see specific error (API key invalid, etc.)
- [ ] Given successful connection, when data syncs, then I see last sync timestamp
- [ ] Given connection active, when I disconnect, then I see confirmation: "This will stop [effects]"
- [ ] Sync frequency: [real-time / every X minutes / manual]
- [ ] Given sync errors, when they occur, then I'm notified and can retry
- [ ] Data mapping: [how fields map between systems]

---

### Mobile-Specific Story Template

**As a** mobile user
**I want to** [action on mobile]
**So that** I can [accomplish goal on-the-go]

**Acceptance Criteria:**
- [ ] Given I'm on mobile, when I view page, then layout adapts to screen size (responsive)
- [ ] Given touch interface, when I tap buttons, then targets are minimum 44x44pt
- [ ] Given slow connection, when page loads, then critical content appears within 3 seconds
- [ ] Given I use one hand, when I navigate, then primary actions are in thumb zone (bottom)
- [ ] Given I'm offline, when I make changes, then they queue and sync when connection returns
- [ ] Given I rotate device, when orientation changes, then layout adjusts without data loss
- [ ] Works on iOS 14+ and Android 10+

---

## Prioritization Framework

### MoSCoW Method

**Must Have:**
- Critical to core value proposition
- Product doesn't work without it
- Blocks other essential features
- Legal/compliance requirement

**Should Have:**
- Important but not critical
- Has workaround if not included
- High value, reasonable effort
- Expected by users

**Could Have:**
- Nice improvements
- Small value add
- Easy to implement
- Low risk if skipped

**Won't Have (This Release):**
- Future considerations
- Out of scope for current stage
- Low value relative to effort
- Deferred to later versions

---

### Value vs Effort Matrix

```
High Value, Low Effort → Do First (Quick Wins)
High Value, High Effort → Plan Carefully (Major Features)
Low Value, Low Effort → Do Later (Fill Gaps)
Low Value, High Effort → Don't Do (Money Pit)
```

Map each story to a quadrant to guide prioritization.

---

### RICE Scoring

Score each story on:
- **Reach:** How many users affected? (per time period)
- **Impact:** How much does it improve their experience? (0.25 = minimal, 3 = massive)
- **Confidence:** How sure are we? (% as decimal)
- **Effort:** Person-months required

**RICE Score = (Reach × Impact × Confidence) / Effort**

Higher scores = higher priority.

---

## Story Sizing Guidelines

### Small (S): <1 day
- Simple UI change
- Add validation rule
- Update copy/labels
- Bug fix

**Example:**
- Change button text from "Submit" to "Save Changes"
- Add email format validation to form field

### Medium (M): 1-3 days
- New screen with standard components
- Simple integration
- Enhanced existing feature
- Multiple small stories bundled

**Example:**
- Create settings page with profile editing
- Add export to CSV functionality
- Implement basic search

### Large (L): 3-5 days
- Complex workflow
- New integration with learning curve
- Significant refactoring needed
- Multiple systems involved

**Example:**
- Build multi-step onboarding flow
- Integrate payment processing (Stripe)
- Implement role-based permissions

### Extra Large (XL): 5-10 days
- Major feature with many unknowns
- Significant architectural change
- High complexity/risk

**Action:** Break into smaller stories if possible.

**Example:**
- Build real-time collaboration system
- Implement full reporting dashboard
- Create mobile app from scratch

---

## Story Mapping

Visualize user journey horizontally, features vertically:

```
[User Journey Stages →]
Discovery | Evaluation | First Use | Regular Use | Power Use
    ↓          ↓            ↓            ↓            ↓
[Story 1.1]  [Story 2.1]  [Story 3.1]  [Story 4.1]  [Story 5.1]
[Story 1.2]  [Story 2.2]  [Story 3.2]  [Story 4.2]  [Story 5.2]
[Story 1.3]               [Story 3.3]  [Story 4.3]

Top row = MVP (must-have)
Second row = V1.1 (should-have)
Third row = V1.2 (nice-to-have)
```

This ensures you build horizontally across the journey, not vertically on one feature.

---

## Anti-Patterns to Avoid

### ❌ Technical Stories Without User Value

**Bad:**
- "As a developer, I want to refactor the database schema"

**Good:**
- "As a user, I want pages to load in <2 seconds, so that I don't get frustrated waiting"
  - Technical implementation: Requires database optimization, caching layer

**Why:** Stories should describe user value, not implementation details. Technical work gets captured in acceptance criteria or technical notes.

---

### ❌ Vague Acceptance Criteria

**Bad:**
- "Feature works correctly"
- "Looks good"
- "Is fast"

**Good:**
- "Given 1000 items, when page loads, then initial render completes within 2 seconds"
- "Given various screen sizes, when user resizes browser, then layout remains readable from 320px to 1920px width"

**Why:** Vague criteria lead to unclear requirements and misaligned expectations.

---

### ❌ Epics Disguised as Stories

**Bad:**
- "As a user, I want a complete reporting system, so that I can analyze my data"

**Good (Break into stories):**
- Story 1: "As a user, I want to view a dashboard with key metrics, so that I see status at a glance"
- Story 2: "As a user, I want to filter reports by date range, so that I can analyze specific periods"
- Story 3: "As a user, I want to export reports as PDF, so that I can share with stakeholders"

**Why:** Stories should be completable in one iteration. If too large, break them down.

---

### ❌ Solutions Instead of Problems

**Bad:**
- "As a user, I want a dropdown menu with 50 options..."

**Good:**
- "As a user, I want to select my country, so that I see relevant content"
  - **Acceptance:** Supports all 195 countries with search/autocomplete

**Why:** State the problem and outcome, not the solution. Gives flexibility in implementation.

---

### ❌ Missing the "So That" (Benefit)

**Bad:**
- "As a user, I want to change my password"

**Good:**
- "As a user, I want to change my password, so that I can maintain account security if compromised"

**Why:** The "so that" clarifies the value and helps prioritize.

---

## Story Refinement Checklist

Before a story is ready for development:

- [ ] **Independent:** Can be delivered independently (or dependencies noted)
- [ ] **Negotiable:** Details can be discussed (not a rigid contract)
- [ ] **Valuable:** Delivers value to user or business
- [ ] **Estimable:** Team can estimate effort
- [ ] **Small:** Can be completed in one iteration
- [ ] **Testable:** Has clear, verifiable acceptance criteria

If any item fails, refine the story further.

---

## Acceptance Criteria Best Practices

### Use Given-When-Then Format

**Structure:**
- **Given** [context/precondition]
- **When** [action/event]
- **Then** [observable outcome]

**Example:**
- **Given** I'm logged in with admin role
- **When** I navigate to user management
- **Then** I see a list of all users with edit/delete actions

### Cover Multiple Scenarios

**Happy Path:**
- Ideal conditions, everything works

**Alternative Paths:**
- Valid but less common scenarios

**Error Conditions:**
- Invalid input, failures, edge cases

**Edge Cases:**
- Boundary conditions, unusual but valid states

### Make Criteria Specific and Measurable

**Vague:** "Fast performance"
**Specific:** "Search results return within 500ms for 95% of queries"

**Vague:** "User-friendly"
**Specific:** "New users reach first value in <5 minutes without help"

---

## Cross-Functional Requirements

Some requirements apply across many stories:

### Performance
- Page load: <3 seconds on 3G connection
- API response: <500ms for 95th percentile
- Database queries: <100ms for most common operations

### Security
- All API endpoints require authentication
- SQL injection prevention (parameterized queries)
- XSS protection (sanitize user input)
- HTTPS only (no plain HTTP)

### Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation for all interactions
- Screen reader compatible (ARIA labels)
- Color contrast minimum 4.5:1

### Analytics
- Track page views for all major screens
- Track button clicks for primary CTAs
- Track errors and exceptions
- Track user journey completion rates

**Approach:** Document these once, reference in stories: "Must meet performance standards" or create a "Definition of Done" that applies to all stories.

---

## Story Dependencies

### Types of Dependencies

**Sequential:** Story B cannot start until Story A is complete
- Example: "User profile editing" depends on "User authentication"

**Data:** Story B needs data created by Story A
- Example: "Export projects" depends on "Create projects"

**Technical:** Story B needs infrastructure from Story A
- Example: "Real-time notifications" depends on "WebSocket connection"

### Managing Dependencies

**Visualize:** Use dependency arrows in story maps or project tools
**Minimize:** Challenge each dependency - is it really required?
**Plan:** Schedule dependent stories in same or consecutive sprints
**Communicate:** Make dependencies explicit in story description

---

## Vertical Slicing

**Goal:** Each story delivers end-to-end value across all layers (UI, logic, data).

**Bad (Horizontal Slice):**
- Sprint 1: Build database schema
- Sprint 2: Build API
- Sprint 3: Build UI
- **Problem:** No user value until Sprint 3

**Good (Vertical Slice):**
- Sprint 1: User can create basic project (simple UI + API + DB)
- Sprint 2: User can add tasks to project
- Sprint 3: User can assign tasks to team members
- **Benefit:** Shippable value every sprint

---

## Questions to Ask When Writing Stories

1. **Who is the user?** (Be specific - which persona?)
2. **What do they want to do?** (Action, not feature)
3. **Why do they want to do it?** (Benefit, outcome)
4. **How will we know it's done?** (Acceptance criteria)
5. **What can go wrong?** (Error scenarios)
6. **How is this different from [similar feature]?** (Clarity on scope)
7. **What happens if we don't build this?** (Validate importance)
8. **Can we start with less?** (Find the minimum viable version)

---

## Story Review Checklist

Before considering a story complete, verify:

### During Writing
- [ ] User and benefit are clear
- [ ] Acceptance criteria are specific and testable
- [ ] Dependencies are identified
- [ ] Effort is estimated
- [ ] Priority is assigned
- [ ] Story is sized appropriately (not too large)

### Before Development
- [ ] Team understands the story
- [ ] Designer has mocked up UI (if needed)
- [ ] Technical approach is agreed upon
- [ ] Test scenarios are defined
- [ ] Data requirements are clear

### After Development
- [ ] All acceptance criteria met
- [ ] Edge cases handled
- [ ] Tests written and passing
- [ ] Code reviewed
- [ ] Product owner accepted
- [ ] Documentation updated
- [ ] Deployed to production

---

## Change Log

| Date | Change | Rationale | Updated By |
|------|--------|-----------|------------|
| [Date] | [Story added/modified] | [Why] | [Name] |

---

**Next Steps:**
After user stories are complete, proceed to:
- `/prod-assumptions-and-risks` - Identify assumptions behind these stories and risks to delivery
- `/prod-success-metrics` - Define how we measure success of these stories

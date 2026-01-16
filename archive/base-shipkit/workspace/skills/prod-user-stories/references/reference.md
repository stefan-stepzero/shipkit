# User Stories Reference

Extended guidance for writing effective user stories with actionable acceptance criteria.

## Table of Contents

- INVEST Principles
- Writing Great User Stories
- Acceptance Criteria Patterns
- Story Splitting Techniques
- Prioritization Methods
- Common Mistakes

---

## INVEST Principles

Every good user story should be **INVEST**:

### Independent

**What it means:** Story can be developed and delivered independently.

**Why it matters:**
- Allows flexible prioritization
- Reduces dependencies and blockers
- Enables parallel development

**How to achieve it:**
- Avoid tight coupling between stories
- Each story delivers standalone value
- If dependencies exist, make them explicit

**Example:**
- ❌ **Dependent:** "Add pagination to user list" (depends on "Create user list")
- ✅ **Independent:** "Display users in a searchable, paginated list"

### Negotiable

**What it means:** Details are flexible, not a rigid contract.

**Why it matters:**
- Encourages collaboration
- Allows for better solutions during development
- Focuses on outcome, not prescription

**How to achieve it:**
- Describe the problem, not the solution
- Leave implementation details open
- Collaborate on the "how" during development

**Example:**
- ❌ **Rigid:** "Add a blue dropdown with 15 items sorted alphabetically"
- ✅ **Negotiable:** "User can select their country from a list"
  - Team can discuss: dropdown vs autocomplete, how to handle 195 countries

### Valuable

**What it means:** Delivers clear value to user or business.

**Why it matters:**
- Justifies the work
- Helps with prioritization
- Keeps team focused on outcomes

**How to achieve it:**
- Always include the "so that" clause
- Tie to user outcomes or business metrics
- Challenge stories that lack clear value

**Example:**
- ❌ **Not Valuable:** "As a developer, I want to refactor the codebase"
- ✅ **Valuable:** "As a user, I want pages to load in <2 seconds, so I don't abandon the site"
  - (Refactoring is the implementation approach, not the value)

### Estimable

**What it means:** Team can estimate the effort reasonably.

**Why it matters:**
- Enables planning
- Reveals ambiguity or unknowns
- Helps with capacity forecasting

**How to achieve it:**
- Provide enough detail
- Break down if too vague
- Spike (time-boxed research) if unknowns exist

**Example:**
- ❌ **Not Estimable:** "Improve search"
- ✅ **Estimable:** "Add autocomplete suggestions to search, showing top 5 recent + top 5 popular results"

### Small

**What it means:** Can be completed in one iteration (sprint).

**Why it matters:**
- Faster feedback
- Easier to estimate
- More frequent delivery

**How to achieve it:**
- Break large stories into smaller pieces
- Vertical slicing (end-to-end thin features)
- Aim for 1-5 days of work

**Example:**
- ❌ **Too Large:** "Build complete user management system"
- ✅ **Small:**
  - Story 1: "Admin can view list of users"
  - Story 2: "Admin can search users by email"
  - Story 3: "Admin can deactivate a user account"

### Testable

**What it means:** Clear criteria to verify it's done.

**Why it matters:**
- Shared understanding of "done"
- Prevents scope creep
- Enables automated testing

**How to achieve it:**
- Write specific acceptance criteria
- Use Given-When-Then format
- Include measurable outcomes

**Example:**
- ❌ **Not Testable:** "Search should be fast"
- ✅ **Testable:** "Given 10,000 items, when user types query, then results appear within 500ms"

---

## Writing Great User Stories

### The Basic Template

```
As a [persona/role]
I want to [action/capability]
So that [benefit/outcome]
```

### Picking the Right Persona

**Use specific personas, not generic roles:**
- ❌ "As a user"
- ✅ "As a project manager coordinating remote teams"

**Why:** Different personas have different needs, contexts, and pain points.

**From your personas.md:**
- Use actual persona names: "As Sarah (Engineering Manager)"
- Provides context on technical savviness, time constraints, goals

### Defining the Action

**Be specific about what they want to do:**
- ❌ "I want to manage my account"
- ✅ "I want to update my email address"

**Focus on capability, not interface:**
- ❌ "I want a button to export data"
- ✅ "I want to export my data as CSV"

### Articulating the Benefit

**Always include "so that" - it clarifies value:**
- ❌ "I want to change my password" (missing "why")
- ✅ "I want to change my password, so that I can secure my account if I suspect it's compromised"

**Benefit should be user-centric:**
- ❌ "So that the database is normalized"
- ✅ "So that my data loads faster"

---

## Acceptance Criteria Patterns

### Given-When-Then (Gherkin)

**Format:**
```
Given [context/precondition]
When [action/trigger]
Then [expected outcome]
```

**Examples:**

**Login:**
```
Given I'm on the login page
When I enter valid credentials and click "Sign In"
Then I'm redirected to my dashboard
```

**Error handling:**
```
Given I'm on the login page
When I enter an invalid password 3 times
Then I see "Too many attempts. Try again in 15 minutes"
And my account is temporarily locked
```

**Edge case:**
```
Given I'm uploading a 100MB file
When the upload reaches 50%
And my internet disconnects
Then when I reconnect, the upload resumes from 50%
```

### Checklist Format

**When Given-When-Then feels awkward, use simple checklist:**

```
Acceptance Criteria:
- [ ] Email field validates format (user@domain.com)
- [ ] Password requires: 8+ chars, 1 uppercase, 1 number, 1 special char
- [ ] "Show password" toggle reveals/hides password
- [ ] "Remember me" checkbox persists session for 30 days
- [ ] Link to "Forgot password" flow works
```

### Quantifiable Criteria

**Include specific metrics when relevant:**

**Performance:**
- "Page loads in <3 seconds on 3G connection"
- "Search returns results in <500ms for 95% of queries"
- "Supports 1000 concurrent users"

**Scale:**
- "Handles datasets up to 100,000 rows"
- "Supports files up to 50MB"
- "Pagination shows 20 items per page"

**Accuracy:**
- "Calculation accurate to 2 decimal places"
- "Geolocation within 100 meters"
- "Auto-save every 30 seconds"

---

## Story Splitting Techniques

### Why Split Stories?

- Story too large to complete in one iteration
- Reduces risk (smaller pieces = faster feedback)
- Enables earlier delivery of partial value

### Splitting by Workflow Steps

**Large story:** "User can purchase a product"

**Split into steps:**
1. "User can add items to cart"
2. "User can enter shipping information"
3. "User can enter payment information"
4. "User receives order confirmation email"

### Splitting by CRUD Operations

**Large story:** "Admin can manage users"

**Split by operation:**
1. "Admin can view list of all users"
2. "Admin can create a new user"
3. "Admin can edit user details"
4. "Admin can delete a user"

### Splitting by Happy Path vs Edge Cases

**First story (happy path):**
- "User can upload profile picture (JPG/PNG, <5MB)"

**Second story (edge cases):**
- "User sees helpful error if file format unsupported or size exceeds limit"

### Splitting by User Roles

**Large story:** "Users can collaborate on documents"

**Split by role:**
1. "Owner can share document with others"
2. "Editor can make changes to shared document"
3. "Viewer can view shared document (read-only)"
4. "Owner can change permissions for collaborators"

### Splitting by Data Variations

**Large story:** "User can import data"

**Split by format:**
1. "User can import CSV files"
2. "User can import JSON files"
3. "User can import Excel files"

### Splitting by Interface (Mobile vs Desktop)

**Split by platform:**
1. "User can search products on desktop (full filters)"
2. "User can search products on mobile (streamlined interface)"

### Splitting by Performance

**First story (basic functionality):**
- "User can view list of 100 items"

**Second story (optimization):**
- "User can view list of 10,000+ items with pagination/virtualization"

---

## Prioritization Methods

### MoSCoW

**Must Have:**
- Product fails without it
- Legal/regulatory requirement
- Core value proposition

**Should Have:**
- Important but not critical
- Workaround exists
- High value

**Could Have:**
- Nice to have
- Small value add
- Low priority

**Won't Have (this time):**
- Out of scope
- Future consideration

### Kano Model

**Basic Needs (Must-haves):**
- Users expect these
- Absence causes dissatisfaction
- Presence doesn't delight
- **Example:** Login, password reset

**Performance Needs (More is better):**
- Linear satisfaction
- Faster/better = happier users
- **Example:** Load speed, search relevance

**Delighters (Wow factors):**
- Unexpected features
- Presence creates delight
- Absence doesn't cause dissatisfaction
- **Example:** Fun animations, Easter eggs

**Prioritization:**
1. Basic needs first (avoid dissatisfaction)
2. Performance needs next (optimize satisfaction)
3. Delighters last (create advocates)

### Value vs Effort (2×2 Matrix)

**High Value, Low Effort = Quick Wins**
- Do first
- Fast ROI

**High Value, High Effort = Strategic**
- Plan carefully
- Big bets

**Low Value, Low Effort = Fill-ins**
- Do when capacity available
- Nice improvements

**Low Value, High Effort = Avoid**
- Don't do
- Money pit

### RICE Score

**Formula:** (Reach × Impact × Confidence) / Effort

**Reach:** Number of users affected per time period
- Example: 5,000 users per quarter

**Impact:** How much it helps (scale)
- 3 = Massive impact
- 2 = High impact
- 1 = Medium impact
- 0.5 = Low impact
- 0.25 = Minimal impact

**Confidence:** How sure are you?
- 100% = High confidence
- 80% = Medium confidence
- 50% = Low confidence

**Effort:** Person-months required
- Example: 2 person-months

**Example:**
- Reach: 10,000 users/quarter
- Impact: 2 (high)
- Confidence: 80%
- Effort: 1 person-month
- **RICE = (10,000 × 2 × 0.8) / 1 = 16,000**

Higher score = higher priority.

---

## Common Mistakes

### Mistake 1: Writing Technical Stories

**Bad:**
```
As a developer
I want to upgrade to React 18
So that we use the latest framework
```

**Good:**
```
As a user
I want pages to load faster
So that I spend less time waiting

Technical implementation:
- Upgrade to React 18 for Suspense + streaming SSR
- Expected improvement: 30% faster initial load
```

**Fix:** Technical work should support user value. Frame as user benefit, capture technical approach in notes.

### Mistake 2: Solution-First Instead of Problem-First

**Bad:**
```
As a user
I want a carousel on the homepage with 5 slides
```

**Good:**
```
As a new visitor
I want to quickly understand what the product does
So that I can decide if it's relevant to me

Design exploration needed:
- Consider: hero section, carousel, video, interactive demo
- Optimize for clarity and engagement
```

**Fix:** Describe the problem and desired outcome, not the solution.

### Mistake 3: Too Vague

**Bad:**
```
As a user
I want better search
So that I can find things
```

**Good:**
```
As a researcher
I want to search by keyword across all documents
So that I can find relevant research quickly

Acceptance criteria:
- Search includes: title, author, abstract, tags
- Results ranked by relevance (TF-IDF or similar)
- Returns results in <500ms for 95% of queries
- Handles typos (fuzzy matching)
```

**Fix:** Add specific details and measurable acceptance criteria.

### Mistake 4: Epics Disguised as Stories

**Bad:**
```
As a user
I want a complete analytics dashboard
```

**Good (Break it down):**
```
Epic: Analytics Dashboard

Story 1: View key metrics at a glance
Story 2: Filter data by date range
Story 3: Export reports as PDF
Story 4: Schedule automated email reports
Story 5: Create custom metric widgets
```

**Fix:** If story takes >1 iteration, it's too big. Break it down.

### Mistake 5: Lack of Acceptance Criteria

**Bad:**
```
As a user
I want to reset my password

(No acceptance criteria)
```

**Good:**
```
As a user
I want to reset my password
So that I can regain access if I forget it

Acceptance criteria:
- [ ] "Forgot password" link on login page
- [ ] Enter email → receive reset link within 5 minutes
- [ ] Reset link expires after 24 hours
- [ ] New password meets requirements (8+ chars, etc.)
- [ ] After reset, old password no longer works
- [ ] User is logged in automatically after reset
```

**Fix:** Always include specific, testable acceptance criteria.

### Mistake 6: Missing the "So That"

**Bad:**
```
As a user
I want to export data
```

**Good:**
```
As a user
I want to export my data as CSV
So that I can analyze it in Excel
```

**Fix:** Always include the benefit/outcome. It clarifies value and helps with prioritization.

---

## Story Templates for Common Scenarios

### Feature Flags

```
As a product manager
I want to enable [feature] for beta users only
So that we can test before full rollout

Acceptance criteria:
- [ ] Feature hidden by default
- [ ] Admin can enable for specific users/organizations
- [ ] Feature visibility toggleable without deployment
- [ ] Analytics track usage of feature-flagged functionality
```

### A/B Testing

```
As a product manager
I want to A/B test [two variants]
So that we can determine which performs better

Acceptance criteria:
- [ ] 50% of users see variant A, 50% see variant B
- [ ] User always sees same variant (consistent)
- [ ] Track conversion rate for each variant
- [ ] Stat sig calculator determines winner (95% confidence)
```

### Accessibility

```
As a user with [disability]
I want to [accomplish task]
So that I can use the product independently

Acceptance criteria:
- [ ] Screen reader announces all interactive elements
- [ ] Keyboard navigation works (Tab, Enter, Esc)
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Focus indicators visible
- [ ] Alt text for all meaningful images
```

### Performance

```
As a user on slow connection
I want pages to load quickly
So that I don't abandon the site

Acceptance criteria:
- [ ] Initial page render <3 seconds on 3G
- [ ] Largest Contentful Paint (LCP) <2.5 seconds
- [ ] First Input Delay (FID) <100ms
- [ ] Cumulative Layout Shift (CLS) <0.1
- [ ] Lighthouse score >90
```

---

## Conversion from Interaction Design

### From Journey Stages to Stories

**Interaction Design Journey Stage:**
- **Stage 3: First Use / Onboarding**
- Entry: User signs up
- "Aha!" moment: Complete first task in <5 minutes
- Potential friction: Complex setup process

**Convert to User Stories:**

**Story 1:**
```
As a new user
I want to sign up with my Google account
So that I can get started in seconds

AC:
- [ ] "Sign up with Google" button on homepage
- [ ] OAuth flow completes without errors
- [ ] User lands in product within 30 seconds
```

**Story 2:**
```
As a new user
I want guided setup to create my first project
So that I reach value quickly without getting lost

AC:
- [ ] 3-step wizard: Name project → Add task → Mark complete
- [ ] Each step <30 seconds to complete
- [ ] Skip option available
- [ ] Celebration message on completion
```

### From Interaction Patterns to Stories

**Interaction Pattern:**
- Loading states: Skeleton screens for content-heavy pages

**Convert to Story:**
```
As a user waiting for data to load
I want to see skeleton placeholders
So that I know the page is working (not broken)

AC:
- [ ] Skeleton matches layout of actual content
- [ ] Shows for any load >300ms
- [ ] Animates subtly to indicate progress
```

---

## Tips for Success

1. **Collaborate:** Write stories with PM, designer, and engineers together
2. **Refine regularly:** Review and improve stories before starting work
3. **Keep visible:** Use story maps or boards to visualize the whole picture
4. **Review completed stories:** Learn what worked and what didn't
5. **Link to designs:** Attach wireframes, mockups, or prototypes
6. **Reference research:** Link to user interviews, usability tests, analytics
7. **Update as you learn:** Stories evolve as you build and test
8. **Delete ruthlessly:** Remove stories that no longer matter

---

## Resources

- *User Stories Applied* by Mike Cohn (the definitive guide)
- *User Story Mapping* by Jeff Patton (visualizing the journey)
- Mountain Goat Software (blog/articles by Mike Cohn)
- Roman Pichler (product management blog)

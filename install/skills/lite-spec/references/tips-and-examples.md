# Tips for Effective Specs and Common Examples

Practical guidance for writing clear, actionable specifications.

---

## Writing Tips

### Tip 1: Keep It Actionable

**Bad:**
```markdown
**Then**: Works well
```

**Good:**
```markdown
**Then**:
- Response time < 200ms
- Loading spinner disappears
- Results render with smooth fade-in
```

**Why:** "Works well" is subjective. Specific metrics and behaviors are testable.

---

### Tip 2: Avoid Vague Language

**Vague → Specific:**
- ❌ "Fast response" → ✅ "Responds in <200ms"
- ❌ "Good UX" → ✅ "Smooth 300ms fade-in transition"
- ❌ "Error handling" → ✅ "Show error toast: 'Invalid email format'"
- ❌ "User-friendly" → ✅ "Clear CTA: 'Create your first recipe'"

---

### Tip 3: Specify Exact UI Feedback

**Bad:**
```markdown
**Then**: User sees confirmation
```

**Good:**
```markdown
**Then**: Success toast appears: "Recipe shared successfully" (auto-dismiss after 3 seconds)
```

**Why:** Developer knows exact text, styling cue (toast), and timing.

---

### Tip 4: Apply ALL Edge Case Categories

**Don't skip categories - every feature needs all 6:**
1. Loading states
2. Error states
3. Empty/missing states
4. Permission states
5. Boundary conditions
6. Data consistency

**Even if some don't apply:**
```markdown
### Empty States
- [ ] N/A for this feature (operates on existing recipes only)
```

**Why:** Systematic thinking prevents gaps. Documenting "N/A" shows you considered it.

---

### Tip 5: Prioritize Ruthlessly

**Must Have criteria:**
- MVP cannot ship without this
- Core user value
- Blocking other features

**Should Have criteria:**
- Improves UX but not critical
- Can be deferred to v2
- Nice polish

**Won't Have criteria:**
- Explicitly excluded
- Prevents scope creep
- Documents what we're NOT doing

**Example:**
```markdown
### Must Have
✓ Generate unique share token
✓ Public URL works for unauthenticated users
✓ Owner can revoke share anytime

### Should Have
- Share expiration dates
- View count analytics
- Password-protected shares

### Won't Have (this iteration)
- Social media preview cards
- Share to specific users (not public)
- Collaborative editing via share link
```

---

### Tip 6: Include Technical Context

**Always document:**
- Database changes needed
- API endpoints required
- Tech constraints from stack.md
- Third-party integrations

**Example:**
```markdown
## Technical Notes

**Database changes:**
- Add `share_token` (varchar, unique, nullable) to `recipes` table
- Add `is_public` (boolean, default false) to `recipes` table
- Add `share_created_at` (timestamp, nullable) to `recipes` table

**API endpoints:**
- POST `/api/recipes/:id/share` - Generate share token
- DELETE `/api/recipes/:id/share` - Revoke token
- GET `/recipes/shared/:token` - Public access endpoint

**Tech constraints:**
- Must use Supabase RLS for public access (from stack.md)
- Share tokens must be cryptographically random (crypto.randomUUID)
- Public endpoint bypasses auth middleware
```

---

## Common Scenarios

### Scenario 1: New Feature from Scratch

**Context:** User describes feature idea, no prior context

**Process:**
1. Ask: "What's the core user goal?"
2. Ask: "Any specific edge cases?"
3. Read stack.md, schema.md if available
4. Generate spec with Given/When/Then
5. Apply all 6 edge case categories
6. Prioritize Must/Should/Won't

**Example:**
```
User: "I want to add recipe sharing"

Claude:
1. Ask: "What's the core user goal with sharing?"
   User: "Let users share recipes publicly via link"
2. Ask: "Any specific edge cases?"
   User: "Handle revocation, expired links"
3. Read .shipkit-lite/stack.md (Next.js + Supabase)
4. Read .shipkit-lite/schema.md (recipes table)
5. Generate spec with:
   - User story (recipe author shares publicly)
   - Given/When/Then (toggle share, generate token)
   - All 6 edge case categories
   - Must Have: toggle, token, public page
   - Technical: Add share_token field to recipes
6. Save to .shipkit-lite/specs/active/recipe-sharing.md
7. Suggest: /lite-plan next
```

---

### Scenario 2: Clarify Existing Idea

**Context:** User has vague idea, needs refinement

**Process:**
1. Ask clarifying questions (scope, specifics)
2. Narrow down to concrete behaviors
3. Generate detailed scenarios

**Example:**
```
User: "We need better search"

Claude:
1. Ask: "What should search cover? Recipes, users, both?"
   User: "Just recipes"
2. Ask: "What should be searchable? Title, ingredients, tags?"
   User: "All of those"
3. Ask: "Any specific requirements?"
   User: "Fast, show results as they type"
4. Read stack.md (understand search tech available)
5. Generate spec with:
   - User story (find recipes quickly)
   - Given/When/Then (type query, see results)
   - Edge cases: no results, slow queries, typos
   - Must Have: real-time search, highlight matches
   - Technical: Add search index, API endpoint
6. Save spec
7. Suggest: /lite-plan or /lite-architecture-memory (search approach is architectural decision)
```

---

### Scenario 3: No Stack Context Available

**Context:** User hasn't run `/lite-project-context` yet

**Process:**
1. Detect missing stack.md
2. Ask user directly about tech choices
3. Generate spec with assumptions
4. Suggest running `/lite-project-context` after

**Example:**
```
User: "Spec a login feature"

Claude:
1. Check .shipkit-lite/stack.md (doesn't exist)
2. Ask: "What's your auth approach? Email/password, OAuth, magic link?"
   User: "Email/password for now"
3. Ask: "Any specific security requirements?"
   User: "Standard stuff - secure password, remember me"
4. Generate spec with:
   - User story (access account securely)
   - Given/When/Then (enter credentials, get authenticated)
   - Edge cases: wrong password, account locked, forgot password
   - Must Have: secure login, remember me, password reset
   - Technical: Auth table, session management, bcrypt
5. Save spec
6. Suggest: Run /lite-project-context first to generate stack.md, or proceed with /lite-plan
```

---

## When to Upgrade to Full /dev-specify

**Use lite-spec for:**
- ✅ POC/MVP features
- ✅ Quick iterations
- ✅ Small team or solo dev
- ✅ Simple features (CRUD, forms, dashboards)

**Upgrade to /dev-specify when:**
- ❌ Complex multi-system integration
- ❌ Formal compliance requirements (SOC2, HIPAA, GDPR)
- ❌ Multiple stakeholder sign-off needed
- ❌ Generated code from specs required
- ❌ BDD/automated testing framework integration

---

## Spec Quality Checklist

**Before saving any spec, verify:**
- [ ] User story clearly states WHO, WHAT, WHY
- [ ] At least 2-3 Given/When/Then scenarios
- [ ] ALL 6 edge case categories applied
- [ ] Must Have / Should Have / Won't Have prioritization
- [ ] Technical notes include database/API changes
- [ ] Next steps suggest appropriate skills
- [ ] Specific UI feedback messages (not vague "user knows")
- [ ] Error scenarios documented with rollback behavior
- [ ] Permission checks included
- [ ] Boundary conditions tested

---

## Real-World Examples

### Example 1: CRUD Feature

```markdown
# Recipe CRUD Operations

**User Story:**
As a recipe author, I want to create, edit, and delete my recipes, so I can manage my content.

## Core Scenarios

**Scenario 1: Create Recipe**
**Given**: User is logged in and on dashboard
**When**: User clicks "New Recipe" button
**Then**:
- Empty recipe form appears
- Title field has autofocus
- Save button is disabled until title entered
- Cancel button returns to dashboard

**Scenario 2: Edit Recipe**
**Given**: User owns a recipe
**When**: User clicks "Edit" button
**Then**:
- Recipe form loads with existing values
- Save button enabled
- Success toast on save: "Recipe updated"
- User redirected to recipe view page

**Scenario 3: Delete Recipe**
**Given**: User owns a recipe
**When**: User clicks "Delete" and confirms modal
**Then**:
- Confirmation modal appears: "Delete [Recipe Title]? This cannot be undone."
- On confirm: Recipe soft-deleted, user redirected to dashboard
- Success toast: "Recipe deleted"
- Undo option available for 10 seconds

## Edge Cases

### Loading States
- [x] Show skeleton during recipe load
- [x] Disable Save during API call
- [x] Handle timeout >5s with retry

### Error States
- [x] Network failure → Revert form, show error
- [x] Validation errors → Inline feedback on fields
- [x] 404 on edit → "Recipe not found" message

### Permission States
- [x] Non-owner sees "View only" message
- [x] Unauthenticated → Redirect to login

### Boundary Conditions
- [x] Title max 100 chars (show counter)
- [x] Description max 5000 chars
- [x] Rate limit: Max 10 creates per hour

### Data Consistency
- [x] Refresh recipe list after delete
- [x] Optimistic update on edit (revert on failure)
```

---

### Example 2: Integration Feature

```markdown
# Lemon Squeezy Payment Integration

**User Story:**
As a user, I want to upgrade to Pro via Lemon Squeezy, so I can access premium features.

## Core Scenarios

**Scenario 1: Initiate Checkout**
**Given**: User is on pricing page
**When**: User clicks "Upgrade to Pro" button
**Then**:
- Lemon Squeezy checkout URL generated
- User redirected to Lemon Squeezy-hosted checkout
- Custom data includes user_id for webhook matching

**Scenario 2: Successful Payment**
**Given**: User completed Lemon Squeezy payment
**When**: order_created webhook received
**Then**:
- Webhook confirms payment
- User role updated to "pro"
- Success page shows: "Welcome to Pro!"
- Email sent via Resend: "Payment confirmation"

**Scenario 3: Failed Payment**
**Given**: User's payment failed at Lemon Squeezy
**When**: User clicks "Cancel" or payment fails
**Then**:
- User sees "Payment cancelled" message
- Retry button available
- User role unchanged (still "free")

## Edge Cases

### Error States
- [x] Webhook failure → Lemon Squeezy retries automatically
- [x] Card declined → Show error message from checkout
- [x] Network timeout → Show "Try again" with support link

### Permission States
- [x] Already Pro user → Redirect to Lemon Squeezy customer portal
- [x] Unauthenticated → Redirect to login first

### Data Consistency
- [x] Webhook idempotency (check order_id before processing)
- [x] Handle event ordering (order_created before subscription_created)

## Technical Notes

**Lemon Squeezy Integration:**
- Use Lemon Squeezy Checkout (hosted - MoR handles tax)
- Webhook endpoint: POST `/api/webhooks/lemonsqueezy`
- Verify webhook signature with LEMONSQUEEZY_WEBHOOK_SECRET
- Store Lemon Squeezy customer_id in users table

**Database changes:**
- Add `lemonsqueezy_customer_id` (varchar, nullable) to users
- Add `lemonsqueezy_subscription_id` (varchar, nullable) to users
- Add `role` (enum: free, pro) to users (default: free)
```

---

**Remember:** Clear specs prevent rework. Spend time upfront clarifying requirements to save time during implementation.

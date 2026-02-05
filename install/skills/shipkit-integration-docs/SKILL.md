---
name: shipkit-integration-docs
description: "Use when needing current API patterns for external services. Triggers: 'fetch docs', 'integration help', 'current API patterns', 'how to use [service]'."
---

# shipkit-integration-docs - Live Documentation Integration Safety

**Purpose**: Prevent common integration mistakes by fetching current security best practices from official documentation, caching them locally, and providing real-time warnings based on up-to-date patterns.

---

## When to Invoke

**Auto-invoked by implement** when external service keywords detected:
- "lemonsqueezy", "lemon squeezy", "webhook", "payment", "subscription"
- "supabase", "RLS", "auth", "postgres"
- "openai", "api", "llm", "embedding"
- "resend", "email", "transactional"
- "prisma", "orm", "migration"

**Manual invocation**:
- User: "Check my Lemon Squeezy integration"
- User: "Review this webhook handler"
- User: "Is my Supabase auth secure?"

**During**:
- Implementation (natural capability) - Real-time integration guidance
- Code review - Security audit of service integrations

---

## Prerequisites

**Check before starting**:
- Stack defined: `.shipkit/stack.md` (from shipkit-project-context)
  - Confirms which services are officially in use
- Code exists: Service integration code to review

**Optional but helpful**:
- Architecture decisions: `.shipkit/architecture.md`
- Implementation docs: `.shipkit/implementations.md`

---

## Process

### Step 0: Check for Queue (Auto-Detect Mode)

**First, check if running in queue-driven mode**:

Read file (if exists): `.shipkit/.queues/fetch-integration-docs.md`

**If queue file exists and has pending items**:
1. Parse the `## Pending` section for services needing docs
2. For each pending service:
   - Fetch current integration patterns (Step 3 logic)
   - Save to `references/[service]-patterns.md`
   - Move item from Pending to Completed in queue
3. Skip Step 1 questions (services already identified)
4. Continue with Step 3-4 for each service

**If queue file doesn't exist or is empty**:
- Continue to Step 1 (manual mode - ask user questions)

---

### Step 1: Detect Service Integration Context (Manual Mode)

**Before loading anything**, ask user 2-3 questions:

1. **Which service are you integrating?**
   - If auto-invoked: "I detected [service] keywords. Is this a [service] integration?"
   - If manual: "Which service? (Lemon Squeezy, Supabase, OpenAI, Resend, Prisma, other)"

2. **What integration type?**
   - "Webhooks/callbacks?"
   - "API calls?"
   - "Authentication/authorization?"
   - "File uploads/downloads?"
   - "Database operations?"

3. **Security concerns?**
   - "Is this handling sensitive data?"
   - "Are webhooks involved?"
   - "Does this bypass auth?"

**Why ask first**: Don't load irrelevant reference content. Target the specific integration.

---

### Step 2: Verify Service in Stack

**Check if service is documented**:

```bash
# Read to confirm service is approved
.shipkit/stack.md
```

**If service NOT in stack.md**:
```
⚠️ [Service] not documented in stack.md

This integration adds a new external dependency.

Options:
1. Document it: /shipkit-project-context (re-scan)
2. Add manually to stack.md
3. Proceed anyway (not recommended)

Should I proceed?
```

**If service IS in stack.md**:
```
✅ [Service] confirmed in stack.md
Loading integration patterns...
```

### Verification Requirements

Before claiming any service state, verify with tool calls:

| Claim | Required Verification |
|-------|----------------------|
| "Service in stack.md" | `Grep: pattern="service-name" path=".shipkit/stack.md"` returns match |
| "Patterns file fresh" | `Read: references/[service]-patterns.md`, parse "Last Updated" as ISO 8601 |
| "7 days since update" | Compare parsed date to current date mathematically |
| "WebFetch succeeded" | Check response contains expected sections (Red Flags, Best Practices) |

**Verification sequence:**

```
1. Service lookup:
   - Grep: pattern="[service-name]" path=".shipkit/stack.md"
   - If 0 matches → service not in stack, warn user
   - If matches → proceed with confidence

2. Freshness check:
   - Read: file_path="references/[service]-patterns.md"
   - Extract "Last Updated" timestamp
   - Parse as ISO 8601 (expect YYYY-MM-DDTHH:MM:SSZ)
   - If unparseable → treat as stale, trigger refresh
   - Calculate days since: (today - timestamp) / 86400000
   - If > 7 days → stale, trigger refresh

3. WebFetch validation:
   - After fetch, verify response contains:
     - "## Red Flags" section
     - "## Security Best Practices" section
     - "## Verification Checklist" section
   - If missing sections → warn user, suggest manual verification
```

**Service name matching:**
- Case-insensitive search
- If not found, suggest similar names from stack.md
- Common variations: "lemon squeezy" vs "lemonsqueezy", "supabase-js" vs "supabase"

**Timestamp format requirements:**
- Expect ISO 8601: `2025-01-15T10:30:00Z`
- If format varies, attempt flexible parsing
- If unparseable, log warning and treat as stale

**See also:** `shared/references/VERIFICATION-PROTOCOL.md` for standard verification patterns.

---

### Step 3: Fetch or Load Service Documentation

**Check documentation freshness before loading**:

1. **Check if reference file exists**: `references/[service]-patterns.md`
2. **Check timestamp**: Look for "Last Updated" metadata in file
3. **Determine if refresh needed**:
   - File doesn't exist → Fetch fresh
   - File > 7 days old → Fetch fresh
   - File < 7 days old → Use cached

**If fetching fresh documentation**:

```
🔍 Fetching latest [Service] integration patterns...

Using WebFetch to retrieve:
- Official [Service] documentation (security best practices)
- Common pitfalls from [Service] community/Stack Overflow
- Latest API changes that affect security

This will take ~10-15 seconds...
```

**Documentation sources by service (Solo Dev MVP Stack 2025)**:

| Service | Documentation URL | Focus Areas |
|---------|------------------|-------------|
| Lemon Squeezy | https://docs.lemonsqueezy.com/guides/developer-guide/webhooks | Webhook signature validation, order events, subscriptions |
| Supabase | https://supabase.com/docs/guides/auth | RLS policies, Row Level Security, auth helpers |
| OpenAI | https://platform.openai.com/docs/guides/safety-best-practices | API key management, prompt injection prevention |
| Resend | https://resend.com/docs/api-reference/webhooks | Email event webhooks, domain verification |
| Prisma | https://www.prisma.io/docs/guides/migrate | Migrations, schema changes, type safety |

**WebFetch prompt template**:

```
Extract security best practices and common pitfalls for [Service] [integration-type].

Focus on:
1. Authentication/authorization patterns
2. Webhook signature validation (if applicable)
3. API key security
4. Common mistakes developers make
5. Red flags that indicate security issues

Format as:
## Red Flags (Common Mistakes)
- Issue 1: [description]
  - Why dangerous: [explanation]
  - Fix: [code example]

## Security Best Practices
- Practice 1: [description]
  - Example: [code]

## Verification Checklist
- [ ] Check 1
- [ ] Check 2
```

**After fetching, save to references/**:

```markdown
# [Service] Integration Patterns

**Last Updated**: [current timestamp]
**Source**: [documentation URLs]
**Next Refresh**: [timestamp + 7 days]

---

[Extracted patterns from WebFetch]
```

**Use Write tool** to save: `references/[service]-patterns.md`

---

### Step 4: Load and Apply Patterns

**After ensuring fresh documentation**, load relevant patterns:

Read `references/[service]-patterns.md` and extract:
- Red Flags matching the current integration type
- Security best practices
- Verification checklist

**Progressive disclosure**: Only show patterns relevant to user's specific integration type (webhook vs API call vs auth)

---

---

## Caching Strategy

**7-day freshness window**:
- Reference files cached for 7 days
- Prevents redundant API documentation fetches
- Balance between staying current and minimizing web requests

**Metadata format in cached files**:

```markdown
# [Service] Integration Patterns

**Last Updated**: 2025-12-29T10:30:00Z
**Source**: https://docs.lemonsqueezy.com/guides/developer-guide/webhooks
**Next Refresh**: 2026-01-05T10:30:00Z

---

[Patterns content]
```

**When to force refresh**:
- User says "get latest [service] docs"
- Cached file corrupt or missing sections
- Major version change detected (user mentions "v3", "new API", etc.)

---

---

## Tips for Effective Integration Guardrails

**Ask before loading**:
- Don't load all patterns speculatively
- Ask which service, then load that service only
- Keep token usage low

**Focus on critical issues**:
- Signature verification (webhooks)
- API key exposure (client-side)
- Missing auth checks (RLS, user verification)
- Not every style issue

**Provide actionable fixes**:
- Show correct code pattern
- Link to official docs
- Explain WHY it's wrong, not just THAT it's wrong

**When to upgrade to full /integration-guardrails**:
- Complex multi-service orchestration
- Custom service not covered here
- Automated testing needed
- Production security audit required

---

**Remember**: This skill prevents the most common and dangerous integration mistakes. It's not exhaustive, but it catches 80% of issues with minimal overhead.

---

## When This Skill Integrates with Others

### Before This Skill

**shipkit-spec** - Creates feature specification
- **When**: Spec mentions external services (Stripe, Supabase, etc.)
- **Why**: Spec triggers detection of services needing integration docs
- **Trigger**: `/shipkit-detect --mode=services` creates queue after spec

**shipkit-project-context** - Scans and documents tech stack
- **When**: Stack includes external services
- **Why**: Validates services are documented before fetching patterns
- **Trigger**: Stack check in Step 2 references `stack.md`

### After This Skill

**Implementation** (natural capability)
- **When**: Integration patterns loaded and ready
- **Why**: Implementation uses fetched patterns for secure integration
- **Trigger**: User proceeds to implement after reviewing patterns

**shipkit-verify** - Verifies implementation quality
- **When**: Integration implemented, needs security review
- **Why**: Uses cached patterns to verify implementation follows best practices
- **Trigger**: Post-implementation security audit

---

## Context Files This Skill Reads

**Required:**
- `.shipkit/stack.md` - Verifies service is in approved tech stack

**Optional:**
- `.shipkit/.queues/fetch-integration-docs.md` - Queue of services needing docs
- `.shipkit/architecture.md` - Architecture decisions affecting integration
- `references/[service]-patterns.md` - Cached integration patterns (if fresh)

---

## Context Files This Skill Writes

**Creates/Updates:**
- `references/[service]-patterns.md` - Cached integration patterns per service
  - **Write Strategy:** REPLACE (refreshed when >7 days old)

**Queue Processing:**
- `.shipkit/.queues/fetch-integration-docs.md` - Updates Pending/Completed sections
  - **Write Strategy:** UPDATE (move items between sections)

---

<!-- SECTION:success-criteria -->
## Success Criteria

Integration Docs is complete when:
- [ ] Service identified and verified in stack.md
- [ ] Documentation freshness checked (<7 days = use cached)
- [ ] Fresh patterns fetched via WebFetch (if needed)
- [ ] Patterns saved to `references/[service]-patterns.md`
- [ ] Red flags and best practices extracted for user's integration type
- [ ] Queue item moved from Pending to Completed (if queue-driven)
<!-- /SECTION:success-criteria -->

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->
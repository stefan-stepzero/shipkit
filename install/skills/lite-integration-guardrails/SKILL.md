---
name: lite-integration-guardrails
description: Prevents service integration mistakes by fetching live documentation from official sources, caching patterns in references/ with 7-day freshness, and warning about security pitfalls. Detects services (stripe, supabase, openai, s3, sendgrid), fetches latest best practices, saves snippets. Use when implementing external service integrations.
---

# integration-guardrails-lite - Live Documentation Integration Safety

**Purpose**: Prevent common integration mistakes by fetching current security best practices from official documentation, caching them locally, and providing real-time warnings based on up-to-date patterns.

---

## When to Invoke

**Auto-invoked by implement-lite** when external service keywords detected:
- "stripe", "webhook", "payment"
- "supabase", "RLS", "auth", "postgres"
- "openai", "api", "llm", "embedding"
- "s3", "upload", "storage"
- "sendgrid", "email", "transactional"
- "twilio", "sms", "phone"

**Manual invocation**:
- User: "Check my Stripe integration"
- User: "Review this webhook handler"
- User: "Is my Supabase auth secure?"

**During**:
- `/lite-implement` - Real-time integration guidance
- Code review - Security audit of service integrations

---

## Prerequisites

**Check before starting**:
- Stack defined: `.shipkit-lite/stack.md` (from project-context-lite)
  - Confirms which services are officially in use
- Code exists: Service integration code to review

**Optional but helpful**:
- Architecture decisions: `.shipkit-lite/architecture.md`
- Implementation docs: `.shipkit-lite/implementations.md`

---

## Process

### Step 1: Detect Service Integration Context

**Before loading anything**, ask user 2-3 questions:

1. **Which service are you integrating?**
   - If auto-invoked: "I detected [service] keywords. Is this a [service] integration?"
   - If manual: "Which service? (Stripe, Supabase, OpenAI, S3, SendGrid, Twilio, other)"

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
.shipkit-lite/stack.md
```

**If service NOT in stack.md**:
```
⚠️ [Service] not documented in stack.md

This integration adds a new external dependency.

Options:
1. Document it: /lite-project-context (re-scan)
2. Add manually to stack.md
3. Proceed anyway (not recommended)

Should I proceed?
```

**If service IS in stack.md**:
```
✅ [Service] confirmed in stack.md
Loading integration patterns...
```

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

**Documentation sources by service**:

| Service | Documentation URL | Focus Areas |
|---------|------------------|-------------|
| Stripe | https://docs.stripe.com/webhooks | Webhook signature validation, test mode detection |
| Supabase | https://supabase.com/docs/guides/auth | RLS policies, Row Level Security, auth helpers |
| OpenAI | https://platform.openai.com/docs/guides/safety-best-practices | API key management, prompt injection prevention |
| S3/AWS | https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html | Presigned URLs, bucket policies, CORS |
| SendGrid | https://docs.sendgrid.com/for-developers/tracking-events/getting-started-event-webhook-security | Webhook verification, SPF/DKIM setup |

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
**Source**: https://docs.stripe.com/webhooks, https://stripe.com/docs/security
**Next Refresh**: 2026-01-05T10:30:00Z

---

[Patterns content]
```

**When to force refresh**:
- User says "get latest [service] docs"
- Cached file corrupt or missing sections
- Major version change detected (user mentions "v3", "new API", etc.)

---

## Success Criteria

Integration check is complete when:
- [ ] Service detected and confirmed in stack.md
- [ ] Documentation fetched (if stale) OR loaded from cache (if fresh)
- [ ] Relevant patterns loaded (not all patterns)
- [ ] Code scanned for common mistakes
- [ ] Critical issues identified and explained
- [ ] Security checklist provided
- [ ] Fix recommendations given

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

---
name: lite-integration-guardrails
description: Prevents service integration mistakes through progressive reference loading. Detects service keywords (stripe, supabase, openai, etc), loads relevant patterns, warns about common security pitfalls in real-time. Use when user implements external service integrations.
---

# integration-guardrails-lite - Service Integration Safety

**Purpose**: Prevent common integration mistakes by detecting service usage, loading relevant patterns, and providing real-time warnings about security and implementation pitfalls.

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

### Step 3: Load Service-Specific Patterns

**Progressive disclosure**: Load ONLY relevant patterns inline based on service + integration type.

**Pattern structure for each service**:

```markdown
## [Service] Integration Patterns

**Common Mistakes:**
- [Mistake 1]
- [Mistake 2]
- [Mistake 3]

**Security Checklist:**
- [ ] [Security requirement 1]
- [ ] [Security requirement 2]

**Code Pattern:**
[code example inline]

**References:**
- [Official docs URL]
- [Best practices URL]
```

---

### Step 4: Service Integration Patterns (Inline)

**STRIPE INTEGRATION PATTERNS**

```markdown
## Stripe Integration Patterns

### Common Mistakes:

1. **Missing webhook signature verification**
   - Webhooks are PUBLIC endpoints
   - Anyone can POST fake events without verification
   - MUST verify signature using `stripe.webhooks.constructEvent()`

2. **Using client-side API keys**
   - Never expose secret keys in frontend code
   - Use publishable keys only client-side
   - Server-side: Use secret keys from env vars

3. **Not handling webhook retries**
   - Stripe retries failed webhooks
   - MUST make handlers idempotent
   - Store `event.id` to prevent duplicate processing

4. **Ignoring event versioning**
   - Webhook events change over time
   - Specify API version in dashboard
   - Handle missing fields gracefully

### Security Checklist:

- [ ] Webhook signature verified using `stripe.webhooks.constructEvent()`
- [ ] Secret keys stored in environment variables (not code)
- [ ] Publishable keys used client-side only
- [ ] Webhook endpoint uses raw body (not JSON parsed)
- [ ] Event IDs stored to prevent duplicate processing
- [ ] Payment amounts verified server-side (never trust client)
- [ ] HTTPS enforced for all webhook endpoints

### Code Pattern - Webhook Verification:

```javascript
// ✅ CORRECT - Verify webhook signature
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

app.post('/webhook', express.raw({type: 'application/json'}), (req, res) => {
  const sig = req.headers['stripe-signature'];
  const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

  let event;
  try {
    // CRITICAL: Verify signature before trusting payload
    event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Now safe to process event
  switch (event.type) {
    case 'payment_intent.succeeded':
      const paymentIntent = event.data.object;
      // Handle successful payment
      break;
    // ... other event types
  }

  res.json({received: true});
});
```

```javascript
// ❌ WRONG - No signature verification
app.post('/webhook', (req, res) => {
  const event = req.body; // DANGEROUS - could be fake
  // ... processing unverified data
});
```

### Code Pattern - Client Payment Intent:

```javascript
// ✅ CORRECT - Create payment server-side
// Server:
app.post('/create-payment-intent', async (req, res) => {
  const { amount } = req.body;

  // CRITICAL: Verify amount server-side, never trust client
  const validAmount = validateAmount(amount);

  const paymentIntent = await stripe.paymentIntents.create({
    amount: validAmount,
    currency: 'usd',
  });

  res.json({ clientSecret: paymentIntent.client_secret });
});

// Client:
const response = await fetch('/create-payment-intent', {
  method: 'POST',
  body: JSON.stringify({ amount: 2000 }), // $20.00
});
const { clientSecret } = await response.json();
```

```javascript
// ❌ WRONG - Client creates payment
const stripe = Stripe('pk_test_...'); // Only publishable key
const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000, // DANGEROUS - user can modify this
});
```

### References:
- https://stripe.com/docs/webhooks/signatures
- https://stripe.com/docs/payments/payment-intents
- https://stripe.com/docs/keys
```

---

**SUPABASE INTEGRATION PATTERNS**

```markdown
## Supabase Integration Patterns

### Common Mistakes:

1. **Missing Row-Level Security (RLS) policies**
   - Tables without RLS are PUBLIC by default
   - Any authenticated user can read/write ALL rows
   - MUST enable RLS + create policies

2. **Bypassing RLS with service role**
   - Service role key BYPASSES all RLS
   - Never use in client code
   - Only use server-side when intentional

3. **Weak auth checks**
   - `auth.user()` can be null
   - MUST check user exists before database operations
   - Check user owns resource before updates

4. **Not using RLS policies for multi-tenancy**
   - Filter `user_id` in application code = WRONG
   - Let RLS enforce `user_id = auth.uid()` = RIGHT
   - Prevents data leaks from code bugs

### Security Checklist:

- [ ] RLS enabled on ALL tables (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`)
- [ ] RLS policies created for SELECT/INSERT/UPDATE/DELETE
- [ ] Service role key stored server-side only (not client)
- [ ] Anon key used client-side
- [ ] Auth checks before every protected operation
- [ ] User ownership verified in RLS policies (not app code)
- [ ] Foreign key constraints prevent orphaned records

### Code Pattern - RLS Policies:

```sql
-- ✅ CORRECT - Enable RLS + create policies
CREATE TABLE recipes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  title TEXT,
  content TEXT
);

-- CRITICAL: Enable RLS
ALTER TABLE recipes ENABLE ROW LEVEL SECURITY;

-- Policy: Users see only their recipes
CREATE POLICY "Users see own recipes"
  ON recipes
  FOR SELECT
  USING (auth.uid() = user_id);

-- Policy: Users create recipes for themselves
CREATE POLICY "Users create own recipes"
  ON recipes
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Policy: Users update only their recipes
CREATE POLICY "Users update own recipes"
  ON recipes
  FOR UPDATE
  USING (auth.uid() = user_id);

-- Policy: Users delete only their recipes
CREATE POLICY "Users delete own recipes"
  ON recipes
  FOR DELETE
  USING (auth.uid() = user_id);
```

```sql
-- ❌ WRONG - No RLS (table is public!)
CREATE TABLE recipes (
  id UUID PRIMARY KEY,
  user_id UUID,
  title TEXT
);
-- Missing: ALTER TABLE recipes ENABLE ROW LEVEL SECURITY;
```

### Code Pattern - Client Auth Check:

```javascript
// ✅ CORRECT - Check auth before operations
const { data: { user }, error: authError } = await supabase.auth.getUser();

if (!user) {
  throw new Error('Not authenticated');
}

// RLS enforces user_id = auth.uid(), but explicit check is good practice
const { data, error } = await supabase
  .from('recipes')
  .insert({
    user_id: user.id, // Explicit user_id
    title: 'My Recipe'
  });
```

```javascript
// ❌ WRONG - No auth check
const { data, error } = await supabase
  .from('recipes')
  .insert({ title: 'Recipe' }); // Missing user_id, auth not checked
```

### Code Pattern - Service Role (Server-Side Only):

```javascript
// ✅ CORRECT - Service role server-side only
// Server-side API route:
import { createClient } from '@supabase/supabase-js';

const supabaseAdmin = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY // BYPASSES RLS - server only!
);

// Use ONLY when you intentionally need to bypass RLS
const { data } = await supabaseAdmin
  .from('recipes')
  .select('*'); // Returns ALL rows regardless of user
```

```javascript
// ❌ WRONG - Service role in client code
const supabase = createClient(
  'https://xxx.supabase.co',
  'eyJhbGc...' // Service role key EXPOSED - security breach!
);
```

### References:
- https://supabase.com/docs/guides/auth/row-level-security
- https://supabase.com/docs/guides/auth
- https://supabase.com/docs/reference/javascript/auth-getuser
```

---

**OPENAI INTEGRATION PATTERNS**

```markdown
## OpenAI Integration Patterns

### Common Mistakes:

1. **Exposing API keys client-side**
   - API keys are SECRET
   - Never include in frontend code
   - Always proxy through your backend

2. **Not handling rate limits**
   - OpenAI has RPM/TPM limits
   - MUST implement retry logic with exponential backoff
   - Handle 429 status codes

3. **Missing input validation**
   - User input goes to LLM
   - MUST validate/sanitize prompts
   - Prevent prompt injection attacks

4. **Not streaming long responses**
   - Large completions can timeout
   - Use streaming for better UX
   - Handle partial responses

### Security Checklist:

- [ ] API key stored in environment variables (not code)
- [ ] API calls made server-side only (not client)
- [ ] User input validated/sanitized before sending to OpenAI
- [ ] Rate limit handling implemented (retry with backoff)
- [ ] Costs monitored (set usage limits in OpenAI dashboard)
- [ ] Error handling for API failures
- [ ] Streaming used for long completions (optional)

### Code Pattern - Server-Side Proxy:

```javascript
// ✅ CORRECT - Server-side API route
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY, // Server-side only
});

app.post('/api/chat', async (req, res) => {
  const { message } = req.body;

  // CRITICAL: Validate input
  if (!message || message.length > 1000) {
    return res.status(400).json({ error: 'Invalid message' });
  }

  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: message }],
    });

    res.json({ response: completion.choices[0].message.content });
  } catch (error) {
    // Handle rate limits
    if (error.status === 429) {
      return res.status(429).json({ error: 'Rate limit exceeded, try again' });
    }
    res.status(500).json({ error: 'OpenAI error' });
  }
});
```

```javascript
// ❌ WRONG - Client-side API call
const openai = new OpenAI({
  apiKey: 'sk-proj-...' // EXPOSED - security breach!
});

const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: userInput }],
});
```

### Code Pattern - Streaming:

```javascript
// ✅ CORRECT - Stream long responses
app.post('/api/chat-stream', async (req, res) => {
  const { message } = req.body;

  const stream = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: message }],
    stream: true,
  });

  res.setHeader('Content-Type', 'text/event-stream');

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    res.write(`data: ${JSON.stringify({ content })}\n\n`);
  }

  res.end();
});
```

### References:
- https://platform.openai.com/docs/guides/production-best-practices
- https://platform.openai.com/docs/guides/rate-limits
- https://platform.openai.com/docs/api-reference/streaming
```

---

**S3/STORAGE INTEGRATION PATTERNS**

```markdown
## S3/Storage Integration Patterns

### Common Mistakes:

1. **Public buckets**
   - Default to PRIVATE buckets
   - Use signed URLs for temporary access
   - Never make buckets public unless intentional

2. **Missing file validation**
   - Validate file types (MIME + extension)
   - Limit file sizes
   - Scan for malware (if handling user uploads)

3. **Not using pre-signed URLs**
   - Don't proxy uploads through your server
   - Generate pre-signed POST URLs
   - Let client upload directly to S3

4. **Missing access controls**
   - Not checking user owns file before generating URL
   - Not setting expiration on signed URLs
   - Not using IAM roles properly

### Security Checklist:

- [ ] Bucket is PRIVATE (not public)
- [ ] Pre-signed URLs used for uploads (not server proxy)
- [ ] File type validation (MIME + extension)
- [ ] File size limits enforced
- [ ] User ownership verified before access
- [ ] Signed URL expiration set (short TTL)
- [ ] IAM roles used (not hardcoded credentials)

### Code Pattern - Pre-Signed Upload URL:

```javascript
// ✅ CORRECT - Generate pre-signed POST URL
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

const s3Client = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

app.post('/api/upload-url', async (req, res) => {
  const { fileName, fileType } = req.body;

  // CRITICAL: Validate file type
  const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
  if (!allowedTypes.includes(fileType)) {
    return res.status(400).json({ error: 'Invalid file type' });
  }

  const command = new PutObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: `uploads/${userId}/${fileName}`,
    ContentType: fileType,
  });

  // Generate URL that expires in 5 minutes
  const signedUrl = await getSignedUrl(s3Client, command, { expiresIn: 300 });

  res.json({ uploadUrl: signedUrl });
});

// Client uploads directly to S3:
const response = await fetch('/api/upload-url', {
  method: 'POST',
  body: JSON.stringify({ fileName: 'photo.jpg', fileType: 'image/jpeg' }),
});
const { uploadUrl } = await response.json();

await fetch(uploadUrl, {
  method: 'PUT',
  body: file,
  headers: { 'Content-Type': 'image/jpeg' },
});
```

```javascript
// ❌ WRONG - Proxy upload through server
app.post('/api/upload', async (req, res) => {
  const file = req.file; // Server receives entire file
  await s3.putObject({
    Bucket: 'my-bucket',
    Key: file.name,
    Body: file.buffer, // Wastes server bandwidth
  });
});
```

### References:
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html
```

---

### Step 5: Scan Code and Provide Warnings

**After loading patterns, scan code** (if provided):

```markdown
## Integration Analysis

**Code scanned**: [file paths]

**Findings**:

⚠️ CRITICAL - [Security issue found]
  Location: [file:line]
  Issue: [Description]
  Fix: [Code pattern to use]

⚠️ WARNING - [Best practice violation]
  Location: [file:line]
  Issue: [Description]
  Suggestion: [Improvement]

✅ GOOD - [Correct pattern found]
  Location: [file:line]
  Pattern: [What was done right]

**Security Checklist Status**:
- [ ] [Unchecked item 1]
- [x] [Checked item 2]
- [ ] [Unchecked item 3]
```

**Output to user**:
```
🔍 Integration Guardrails Analysis

Service: Stripe
Type: Webhooks

⚠️ CRITICAL ISSUES:
  1. Missing webhook signature verification in /api/webhook.js:12
     → Webhooks are UNAUTHENTICATED without signature verification
     → See pattern: stripe.webhooks.constructEvent()

⚠️ WARNINGS:
  2. API key in code in /lib/stripe.js:3
     → Move to environment variable

✅ GOOD:
  3. Using publishable key client-side in /components/CheckoutForm.js

Next: Fix critical issues before shipping.
```

---

### Step 6: Log Audit Entry and Suggest Next Step

**Write audit entry to outputs/integration-audit-log.md**:

```markdown
---
## Integration Audit - [Service] - [Timestamp]

**Service**: [Service name]
**Integration Type**: [Type]
**Files Scanned**: [file list]
**Invoked By**: [Manual / Auto-invoked by lite-implement]

### Findings

**CRITICAL Issues**: [count]
[List each critical issue with location and fix]

**WARNINGS**: [count]
[List each warning with location and suggestion]

**GOOD Patterns**: [count]
[List each good pattern found]

### Security Checklist Status
[Full checklist with checked/unchecked items]

### Recommended Actions
1. [Action 1]
2. [Action 2]

### Status
- [ ] Issues fixed
- [ ] Re-audit completed
- [ ] Approved for production

---

```

**Then suggest next step to user**:

```
✅ Integration guardrails check complete
📝 Audit logged to outputs/integration-audit-log.md

🔍 Service: [Service name]
📊 Status: [X critical / Y warnings / Z good]

🔧 Recommended actions:
  1. Fix critical issues immediately
  2. Review warnings before shipping
  3. Run tests to verify fixes

👉 Next options:
  1. /lite-implement - Fix issues found
  2. /lite-quality-confidence - Pre-ship verification
  3. /lite-architecture-memory - Log integration decisions

Continue implementing?
```

---

## What Makes This "Lite"

**Included**:
- ✅ Service keyword detection
- ✅ Progressive reference loading (only relevant patterns)
- ✅ Real-time warnings for common mistakes
- ✅ Inline code patterns (5 major services)
- ✅ Security checklist enforcement

**Not included** (vs full integration-guardrails):
- ❌ Comprehensive service library (only 5 core services)
- ❌ Custom reference file loading (patterns inline only)
- ❌ Automated code scanning (manual review)
- ❌ Integration testing automation
- ❌ Service-specific test generation

**Philosophy**: Cover 80% of integration mistakes with 20% of the complexity.

---

## Integration with Other Skills

**Before integration-guardrails-lite**:
- `/lite-project-context` - Generates stack.md with service list

**During integration-guardrails-lite**:
- Auto-invoked by `/lite-implement` when service keywords detected

**After integration-guardrails-lite**:
- `/lite-implement` - Fix issues found
- `/lite-quality-confidence` - Pre-ship verification
- `/lite-architecture-memory` - Log integration patterns

---

## Context Files This Skill Reads

**Always reads**:
- `.shipkit-lite/stack.md` - Confirms service is documented

**Conditionally reads**:
- `.shipkit-lite/architecture.md` - Past integration decisions
- `.shipkit-lite/implementations.md` - Existing integrations

---

## Context Files This Skill Writes

**Write Strategy: APPEND**

### Primary Output File

**File**: `outputs/integration-audit-log.md`

**Write Behavior**: APPEND - Each integration check adds a new timestamped entry to the audit log.

**Why APPEND?**
- Integration checks occur multiple times across project lifecycle
- Each service integration needs separate audit entry
- Historical record matters (want to see all past checks)
- Different services checked at different times
- Pattern: chronological audit trail, not single snapshot

**What Gets Logged**:
Each append adds one audit entry containing:
- Service name and integration type
- Files scanned
- Critical issues found (with locations and fixes)
- Warnings (with locations and suggestions)
- Good patterns identified
- Security checklist status
- Recommended actions
- Completion status checkboxes

**Entry Format**:
```markdown
---
## Integration Audit - [Service] - [Date/Time]

**Service**: [Stripe/Supabase/OpenAI/etc]
**Integration Type**: [Webhooks/API/Auth/Storage]
**Files Scanned**: [list of files]
**Invoked By**: [Manual / Auto-invoked by implement-lite]

### Findings

**CRITICAL Issues**: [count]
- [Issue 1 with location and fix]

**WARNINGS**: [count]
- [Warning 1 with location and suggestion]

**GOOD Patterns**: [count]
- [Pattern 1 with location]

### Security Checklist Status
- [ ] Unchecked item
- [x] Checked item

### Recommended Actions
1. [Action 1]
2. [Action 2]

### Status
- [ ] Issues fixed
- [ ] Re-audit completed
- [ ] Approved for production

---
```

**When to Write**:
- After completing Step 5 (code scan and warnings)
- Before suggesting next step (Step 6)
- Every time skill is invoked (auto or manual)

**Cross-References**:
Integration decisions can also be logged via:
- `/lite-architecture-memory` - Log integration architecture decisions
- `/lite-work-memory` - Log session-specific findings

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/lite-integration-guardrails` (or auto-invoked by implement-lite)
2. Claude asks which service + integration type
3. Claude reads stack.md (~200 tokens)
4. Claude loads ONLY relevant service patterns inline (~500-800 tokens)
5. Claude scans code (if provided)
6. Total context: ~700-1200 tokens (focused)

**Not loaded unless needed**:
- Other service patterns
- Unrelated specs/plans
- User tasks

---

## Supported Services

**Core Services** (inline patterns):
1. **Stripe** - Payments, webhooks, subscriptions
2. **Supabase** - Auth, RLS, database
3. **OpenAI** - LLM API, embeddings, chat
4. **S3/Storage** - File uploads, signed URLs
5. **SendGrid/Email** - Transactional email (basic pattern below)

**Additional Services** (basic warnings only):
- Twilio (SMS)
- Firebase
- Auth0
- Vercel Blob
- Cloudflare R2

---

## Additional Service Patterns

**SENDGRID/EMAIL INTEGRATION PATTERNS**

```markdown
## SendGrid/Email Integration Patterns

### Common Mistakes:

1. **API key in client code**
   - Email API keys are SECRET
   - Always send from server
   - Never expose in frontend

2. **Missing unsubscribe links**
   - Required by law (CAN-SPAM)
   - Use SendGrid suppression groups
   - Include unsubscribe link in footer

3. **Not validating email addresses**
   - Validate format before sending
   - Handle bounce notifications
   - Remove invalid emails

### Security Checklist:

- [ ] API key stored server-side only
- [ ] Email sent from backend (not client)
- [ ] Unsubscribe link included
- [ ] Email addresses validated
- [ ] Rate limiting implemented
- [ ] Bounce handling configured

### Code Pattern:

```javascript
// ✅ CORRECT - Server-side email
import sgMail from '@sendgrid/mail';

sgMail.setApiKey(process.env.SENDGRID_API_KEY); // Server-side

app.post('/api/send-email', async (req, res) => {
  const { to, subject, text } = req.body;

  // Validate email
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(to)) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  const msg = {
    to,
    from: 'noreply@example.com',
    subject,
    text,
    html: `<p>${text}</p><p><a href="https://example.com/unsubscribe">Unsubscribe</a></p>`,
  };

  await sgMail.send(msg);
  res.json({ sent: true });
});
```

### References:
- https://docs.sendgrid.com/for-developers/sending-email/api-getting-started
```

---

## Success Criteria

Integration check is complete when:
- [ ] Service detected and confirmed in stack.md
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

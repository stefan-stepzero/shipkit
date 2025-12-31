---
name: lite-post-spec-check
description: Hidden detection skill that scans specs for external service mentions (Stripe, Supabase, OpenAI, S3) and creates integration docs queue. Auto-triggered after /lite-spec completes. System skill - not user-invocable.
---

# lite-post-spec-check - Spec Service Detection

**Purpose**: Automatically detect external service integrations mentioned in specs and create queue for fetching current documentation.

**Type**: System skill (hidden from users, auto-triggered)

**Trigger**: After `/lite-spec` completes

---

## What This Skill Does

**Detection:**
1. Reads the most recently created spec in `.shipkit-lite/specs/active/`
2. Scans content for service keywords (Stripe, Supabase, OpenAI, S3, SendGrid, etc.)
3. Identifies which services are mentioned

**Queue Creation:**
1. If services detected, creates `.shipkit-lite/.queues/fetch-integration-docs.md`
2. Lists each service with context (where mentioned, what's needed)
3. Provides clear action items for `/lite-integration-docs`

**Output:**
- Queue file ready for `/lite-integration-docs` to process
- Terminal message suggesting next action

---

## When to Invoke

**Auto-triggered:**
- SessionStop hook after `/lite-spec` completes
- OR lite-milestone-detector routes to this skill

**Manual invocation:**
- Not intended for manual use
- Marked as system skill in manifest

---

## Detection Logic

**Services Detected:**

```python
SERVICES = {
    'stripe': ['stripe', 'payment', 'webhook', 'subscription', 'checkout'],
    'supabase': ['supabase', 'postgres', 'rls', 'auth', 'realtime'],
    'openai': ['openai', 'gpt', 'embedding', 'completion', 'chat'],
    's3': ['s3', 'bucket', 'upload', 'storage', 'cloudfront'],
    'sendgrid': ['sendgrid', 'email', 'smtp', 'transactional'],
    'twilio': ['twilio', 'sms', 'phone', 'messaging'],
    'clerk': ['clerk', 'authentication', 'user management'],
    'vercel': ['vercel', 'deployment', 'edge', 'serverless'],
}
```

**Detection Algorithm:**
1. Read spec markdown content
2. Lowercase and scan for keywords
3. If ANY keyword matches, flag that service
4. Collect all flagged services

---

## Queue File Format

**Creates:** `.shipkit-lite/.queues/fetch-integration-docs.md`

**Content:**
```markdown
# Integration Docs Needed

**Created:** 2025-12-30 14:32
**Reason:** Spec mentions external services

## Pending

- [ ] Stripe integration
  - Mentioned in: specs/active/payment-flow.md
  - Keywords found: stripe, webhook, payment
  - Need: Current webhook signature verification, payment intent patterns

- [ ] Supabase integration
  - Mentioned in: specs/active/payment-flow.md
  - Keywords found: supabase, auth, rls
  - Need: Current auth patterns, RLS policy examples

## Completed

<!-- Items move here after /lite-integration-docs fetches docs -->
```

---

## Process

**Step 1: Find Latest Spec**
```python
from pathlib import Path
import os

def find_latest_spec():
    specs_dir = Path('.shipkit-lite/specs/active')
    if not specs_dir.exists():
        return None

    specs = list(specs_dir.glob('*.md'))
    if not specs:
        return None

    # Return most recently modified spec
    latest = max(specs, key=lambda p: os.path.getmtime(p))
    return latest
```

**Step 2: Detect Services**
```python
def detect_services(spec_path):
    content = spec_path.read_text().lower()

    detected = {}
    for service, keywords in SERVICES.items():
        found_keywords = [kw for kw in keywords if kw in content]
        if found_keywords:
            detected[service] = found_keywords

    return detected
```

**Step 3: Create Queue**
```python
from datetime import datetime

def create_queue(detected_services, spec_path):
    if not detected_services:
        print("✓ No external services detected in spec")
        return

    queue_dir = Path('.shipkit-lite/.queues')
    queue_dir.mkdir(parents=True, exist_ok=True)

    queue_path = queue_dir / 'fetch-integration-docs.md'

    content = f"""# Integration Docs Needed

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Reason:** Spec mentions external services

## Pending

"""

    for service, keywords in detected_services.items():
        content += f"- [ ] {service.capitalize()} integration\n"
        content += f"  - Mentioned in: {spec_path.relative_to('.')}\n"
        content += f"  - Keywords found: {', '.join(keywords)}\n"
        content += f"  - Need: Current best practices and patterns\n\n"

    content += """## Completed

<!-- Items move here after /lite-integration-docs fetches docs -->
"""

    queue_path.write_text(content)

    print(f"✓ Created integration docs queue with {len(detected_services)} services")
    print(f"\n💡 Next: Run /lite-integration-docs to fetch current patterns")
```

---

## Script Location

**Detection script:** `scripts/detect-services.py`

**Invocation:**
```bash
python .claude/skills/lite-post-spec-check/scripts/detect-services.py
```

**Returns:**
- Exit 0: Success (queue created or no services detected)
- Exit 1: Error (spec not found, permissions issue)

---

## Integration with lite-whats-next

**After queue created:**
1. lite-whats-next scans `.shipkit-lite/.queues/`
2. Finds `fetch-integration-docs.md` queue
3. Suggests: "Run /lite-integration-docs - 3 services need current docs"
4. User runs skill, docs fetched, queue items marked complete

---

## When This Skill Integrates with Others

### Before This Skill

**lite-spec** - Creates specification
- **When**: Spec saved to specs/active/
- **Why**: Spec content is what we scan for service mentions
- **Trigger**: SessionStop after lite-spec completes

### After This Skill

**lite-integration-docs** - Fetches current service documentation
- **When**: Queue file exists with pending services
- **Why**: Prevents coding against outdated API patterns
- **Trigger**: lite-whats-next suggests it based on queue

---

## Context Files This Skill Reads

**Required:**
- `.shipkit-lite/specs/active/*.md` - Latest spec to scan

**Optional:**
- None

---

## Context Files This Skill Writes

**Writes:**
- `.shipkit-lite/.queues/fetch-integration-docs.md` - Queue for integration docs

**Write Strategy:** CREATE or APPEND
- If queue doesn't exist: Create new
- If queue exists: Append new services to Pending section

---

## Success Criteria

Detection is successful when:
- [ ] Latest spec scanned for service keywords
- [ ] All matching services identified
- [ ] Queue file created (if services found)
- [ ] Queue format matches template
- [ ] Terminal output suggests next action

---

## Edge Cases

**No spec exists:**
- Exit silently (nothing to detect)
- Don't create queue file

**Spec mentions service but already in queue:**
- Don't duplicate queue entries
- Update "Mentioned in" to include new spec

**Multiple specs created in session:**
- Only scan most recent spec
- Avoid re-detecting same services

---

**Remember**: This is a system skill - users never invoke it directly. It runs automatically after specs are created to enable proactive integration doc fetching.

---
name: lite-document-artifact
description: Centralizes markdown documentation in organized category structure. Categorizes content (api/guides/architecture/processes/reference), generates kebab-case filenames, creates .shipkit-lite/docs/category/filename.md, auto-updates docs/README.md index.
---

# document-artifact-lite - Centralized Documentation Creation

**Purpose**: Create well-organized, categorized documentation for technical decisions, guides, APIs, and processes - avoiding scattered docs across the project.

---

## When to Invoke

**User triggers**:
- "Document this decision"
- "Create architecture doc"
- "Write API guide"
- "Document this process"
- "Create reference doc"
- "Add documentation for..."

**After**:
- Complex architectural decision made (from architecture-memory-lite)
- API endpoint completed (from implement-lite)
- Process established (from any workflow)
- Reference material needed

---

## Prerequisites

**Optional but helpful**:
- Architecture decisions: `.shipkit-lite/architecture.md`
- Implementations: `.shipkit-lite/implementations.md`
- Stack info: `.shipkit-lite/stack.md`

**No strict prerequisites** - can create docs anytime.

---

## Process

### Step 1: Determine What to Document

**Before creating anything**, ask user 2-3 questions:

1. **What are you documenting?**
   - "What's the topic?" (be specific)
   - Examples: "Caching strategy", "User auth API", "Deployment runbook"

2. **Who is the audience?**
   - "Who will read this?"
   - Options: Developers, end users, DevOps, stakeholders, future maintainers

3. **What category does this fit?**
   - Auto-suggest based on topic keywords (see Category Detection below)
   - Let user confirm or override

**Why ask first**: Avoid generating wrong format/depth/category.

---

### Step 2: Category Detection Logic

**Use these rules to auto-categorize** (inline - no external files):

```
Topic Keywords → Category Mapping:

API-related:
  Keywords: "API", "endpoint", "REST", "GraphQL", "route", "schema", "webhook"
  → Category: api/
  → Template: API Reference

Architecture-related:
  Keywords: "architecture", "design decision", "pattern", "system design", "caching", "database design", "infrastructure"
  → Category: architecture/
  → Template: Architecture Decision Record (ADR)

Guide-related:
  Keywords: "how to", "guide", "tutorial", "walkthrough", "getting started", "setup"
  → Category: guides/
  → Template: Step-by-Step Guide

Process-related:
  Keywords: "process", "workflow", "runbook", "deployment", "release", "incident response", "onboarding"
  → Category: processes/
  → Template: Process Documentation

Reference-related:
  Keywords: "reference", "glossary", "conventions", "standards", "cheatsheet", "troubleshooting"
  → Category: reference/
  → Template: Reference Material
```

**Ask user to confirm**:
```
Based on "[topic]", I suggest category: [category]

Is this correct, or would you prefer a different category?
  1. api/
  2. guides/
  3. architecture/
  4. processes/
  5. reference/
```

---

### Step 3: Generate Filename (Kebab-Case)

**Convert topic to kebab-case filename**:

```
Input: "User Authentication API"
→ Lowercase: "user authentication api"
→ Replace spaces with hyphens: "user-authentication-api"
→ Remove special chars: "user-authentication-api"
→ Output: user-authentication-api.md

Input: "How to deploy to production"
→ Output: how-to-deploy-to-production.md

Input: "Caching Strategy Decision (Redis vs In-Memory)"
→ Output: caching-strategy-decision.md
```

**Show filename to user**:
```
Creating: .shipkit-lite/docs/[category]/[filename].md

Proceed?
```

---

### Step 4: Select Template Based on Category

**Each category has a corresponding template**:

See `references/` folder for complete templates:
- `template-api.md` - API Reference template (for api/ category)
- `template-adr.md` - Architecture Decision Record template (for architecture/ category)
- `template-guide.md` - Step-by-Step Guide template (for guides/ category)
- `template-process.md` - Process Documentation template (for processes/ category)
- `template-reference.md` - Reference Material template (for reference/ category)

Each template includes:
- Complete markdown structure
- All required sections
- Field placeholders
- Usage examples

---

### Step 5: Create Document Using Write Tool

**Use Write tool directly** to create:

**Location**: `.shipkit-lite/docs/[category]/[filename].md`

**Steps**:
1. Check if `.shipkit-lite/docs/` exists
   - If NO → Create directory structure first
2. Check if `.shipkit-lite/docs/[category]/` exists
   - If NO → Create category directory
3. Fill template with user's content
4. Write file using Write tool

**Example**:
```
Topic: "User Authentication API"
Category: api/
Filename: user-authentication-api.md
Path: .shipkit-lite/docs/api/user-authentication-api.md

[Use Write tool to create file with API Reference template filled]
```

---

### Step 6: Auto-Update docs/README.md Index

**After creating document, update the index**:

**Location**: `.shipkit-lite/docs/README.md`

**Index structure**:
```markdown
# Documentation Index

**Last Updated**: [Date]

---

## API Documentation

- [User Authentication API](api/user-authentication-api.md) - User login and token management
- [Payment Processing API](api/payment-processing-api.md) - Stripe integration endpoints

---

## Architecture Decisions

- [Caching Strategy](architecture/caching-strategy.md) - Decision to use Redis for session caching
- [Database Choice](architecture/database-choice.md) - PostgreSQL vs MySQL comparison

---

## Guides

- [How to Deploy to Production](guides/how-to-deploy-to-production.md) - Step-by-step deployment guide
- [Local Development Setup](guides/local-development-setup.md) - Getting started for new developers

---

## Processes

- [Deployment Runbook](processes/deployment-runbook.md) - Production deployment process
- [Incident Response](processes/incident-response.md) - Handling production issues

---

## Reference

- [Error Codes](reference/error-codes.md) - Complete list of application error codes
- [Environment Variables](reference/environment-variables.md) - All ENV vars and their purpose

---

**Total documents**: [Count]
```

**Update logic**:
1. Read existing `.shipkit-lite/docs/README.md` (if exists)
2. Find the correct category section (## API Documentation, ## Architecture Decisions, etc.)
3. Add new entry with link and brief description
4. Update "Last Updated" timestamp
5. Update "Total documents" count
6. Write updated README.md

**If README.md doesn't exist**: Create it with the structure above.

---

### Step 7: Suggest Next Step

**After document created**:

```
✅ Documentation created

📁 Location: .shipkit-lite/docs/[category]/[filename].md
📑 Index updated: .shipkit-lite/docs/README.md

📋 Summary:
  • Category: [category]
  • Template: [template type]
  • Filename: [filename].md

👉 Next options:
  1. Continue current work (if this was mid-implementation)
  2. /lite-architecture-memory - Log related architectural decision
  3. /lite-component-knowledge - Document related component
  4. Create another document

What would you like to do?
```

---

## What Makes This "Lite"

**Included**:
- ✅ 5 category types with inline templates
- ✅ Auto-categorization logic
- ✅ Kebab-case naming convention
- ✅ Auto-updating index (README.md)
- ✅ Simple directory structure

**Not included** (vs full document-artifact):
- ❌ Version control for docs (just latest version)
- ❌ Doc review workflow
- ❌ Automated diagram generation
- ❌ Multi-format exports (PDF, HTML)
- ❌ Doc linting/validation
- ❌ Search indexing

**Philosophy**: Organize docs well, make them discoverable via index, keep it simple.

---

## Category Selection Guide

**When unsure which category**:

| If documenting... | Use category... |
|------------------|----------------|
| REST/GraphQL endpoints, webhooks, API schemas | `api/` |
| Design decisions, patterns, system architecture | `architecture/` |
| How-to instructions, tutorials, walkthroughs | `guides/` |
| Workflows, runbooks, deployment steps, incident response | `processes/` |
| Conventions, glossaries, cheatsheets, troubleshooting | `reference/` |

**Can't decide?**: Ask user directly.

---

## Integration with Other Skills

**Before document-artifact-lite**:
- `/lite-architecture-memory` - Makes architectural decision
- `/lite-implement` - Builds complex feature
- `/lite-component-knowledge` - Documents component (might need deeper guide)

**After document-artifact-lite**:
- Continue current workflow (usually go back to what you were doing)
- `/lite-architecture-memory` - If architectural decision needs logging
- `/lite-work-memory` - Log session progress

**When to use**:
- Complex decision needs full ADR (not just entry in architecture.md)
- API is stable enough to document formally
- Process needs documentation for team
- Guide needed for onboarding/troubleshooting

---

## Context Files This Skill Reads

**Optional** (to inform documentation):
- `.shipkit-lite/architecture.md` - Reference existing decisions
- `.shipkit-lite/implementations.md` - Reference existing components
- `.shipkit-lite/stack.md` - Tech stack context

---

## Context Files This Skill Writes

**Creates** (OVERWRITE AND REPLACE strategy):
- `.shipkit-lite/docs/[category]/[filename].md` - The documentation file
  - **Write Strategy**: OVERWRITE AND REPLACE
  - **Behavior**: Each document represents the current state. When updating, completely replace the old content.
  - **Why**: No version history within docs (this is "lite"). Each file is the latest version.
  - **History**: Not preserved in the file itself. If versioning is needed, upgrade to full `/document-artifact`.

**Updates** (APPEND strategy):
- `.shipkit-lite/docs/README.md` - Auto-updated index
  - **Write Strategy**: APPEND
  - **Behavior**: Add new entries to category sections. Preserve all existing links.
  - **Why**: This is a catalog that accumulates over time. Each new doc adds one entry.
  - **History**: Complete list of all documentation created, never remove entries.

**Never modifies**:
- architecture.md, implementations.md (read-only)

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/lite-document-artifact`
2. Claude asks what to document
3. Claude determines category (auto or manual)
4. Claude generates filename
5. **Optionally** reads:
   - architecture.md (if documenting decision)
   - implementations.md (if documenting component)
   - stack.md (if documenting tech choice)
6. Claude uses Write tool to create doc
7. Claude updates README.md index
8. Total context: ~500-1500 tokens (minimal)

**Not loaded unless needed**:
- Other docs
- Specs, plans, tasks
- Unrelated context files

---

## Success Criteria

Documentation is complete when:
- [ ] Category correctly identified
- [ ] Filename follows kebab-case convention
- [ ] Document created in `.shipkit-lite/docs/[category]/[filename].md`
- [ ] Appropriate template used
- [ ] Content is clear and actionable
- [ ] README.md index updated with link + description
- [ ] User knows where to find the doc

---

## Common Scenarios

### Scenario 1: Architecture Decision Documentation

```
User: "Document the caching strategy decision we just made"

Claude:
1. Ask: "What's the decision about? Redis vs in-memory?"
2. User confirms
3. Auto-categorize: architecture/
4. Generate filename: caching-strategy.md
5. Read .shipkit-lite/architecture.md for context
6. Fill ADR template with decision details
7. Write .shipkit-lite/docs/architecture/caching-strategy.md
8. Update .shipkit-lite/docs/README.md with link
9. Suggest: "Continue with /lite-implement?"
```

### Scenario 2: API Documentation

```
User: "Create API docs for the new auth endpoints"

Claude:
1. Ask: "Which endpoints? Login, logout, refresh?"
2. Ask: "Who's the audience? Frontend devs, external API consumers?"
3. Auto-categorize: api/
4. Generate filename: user-authentication-api.md
5. Read .shipkit-lite/implementations.md to see endpoint code
6. Fill API Reference template
7. Write .shipkit-lite/docs/api/user-authentication-api.md
8. Update README.md
9. Suggest: "Continue implementing features?"
```

### Scenario 3: Process Runbook

```
User: "Document our deployment process"

Claude:
1. Ask: "What's the process? Production deployment, staging, both?"
2. Ask: "Who runs this? DevOps, any developer?"
3. Auto-categorize: processes/
4. Generate filename: deployment-runbook.md
5. Fill Process Documentation template
6. Write .shipkit-lite/docs/processes/deployment-runbook.md
7. Update README.md
8. Suggest: "Need any related guides?"
```

---

## Tips for Effective Documentation

**Keep it focused**:
- One topic per document
- Don't combine API docs with guides
- Separate processes into distinct runbooks

**Use good titles**:
- Descriptive: "User Authentication API" not "Auth"
- Specific: "Production Deployment Runbook" not "Deploy"
- Clear: "Redis Caching Strategy" not "Cache Decision"

**Update the index**:
- Always add brief description in README.md
- Makes docs discoverable
- Shows what exists at a glance

**When to create new doc vs update existing**:
- New topic/API/decision → New doc
- Revision to existing → Update existing doc + add changelog entry
- Related but separate → New doc + link in "See Also"

**When to upgrade to full /document-artifact**:
- Need versioning and change tracking
- Docs require review workflow
- Generating diagrams automatically
- Exporting to multiple formats
- Large documentation system (100+ docs)

---

**Remember**: Documentation is for future you and your team. Make it findable (good index), readable (clear structure), and actionable (examples + verification steps).

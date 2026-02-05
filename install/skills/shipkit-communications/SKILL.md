---
name: shipkit-communications
description: "Use when user wants to visualize or present shipkit content as HTML. Triggers: 'create presentation', 'visualize this', 'HTML report'."
---

# shipkit-communications - Visual HTML Reports

**Purpose**: Create beautiful, visual HTML reports from any ShipKit Lite content for presentations, sharing, or visual review.

**What it does**: Reads markdown content from `.shipkit/`, generates styled HTML with purple gradient theme, archives old reports, creates `latest.html`.

---

## When to Invoke

**User triggers**:
- "Visualize the architecture decisions"
- "Create HTML report"
- "Make a visual status report"
- "Generate presentation from project status"
- "Show me quality checklist as HTML"
- "Create shareable report"

**Use cases**:
- Share architecture decisions with team
- Present project status to stakeholders
- Visual review of quality checklist
- Export component documentation as HTML
- Create visual specs for review

---

## Prerequisites

**Optional** (depends on what user wants to visualize):
- `.shipkit/architecture.md` - For architecture decisions
- `.shipkit/implementations.md` - For component/route docs
- `.shipkit/stack.md` - For tech stack overview
- `.shipkit/specs/active/*.md` - For specs
- `.shipkit/plans/*.md` - For implementation plans

**No strict prerequisites** - Can create HTML from any content.

---

## Process

### Step 1: Ask What to Visualize

**Before generating anything**, ask user what they want to visualize:

**Present options:**
```
What would you like to visualize as HTML?

1. Architecture Decisions - Visual timeline of decisions
2. Project Status - Complete health dashboard
3. Quality Checklist - Pre-ship verification
4. Component Documentation - All components/routes
5. Feature Specs - Active specifications
6. Implementation Plans - Current plans
7. Tech Stack - Visual stack overview
8. Custom - You specify the files

Choose a number or describe what you need:
```

**Wait for user response.**

---

### Step 2: Determine Source Files

**Based on user choice, identify which .shipkit/ files to read:**

| Choice | Files to Read | Description Word |
|--------|---------------|------------------|
| 1. Architecture Decisions | `.shipkit/architecture.md` | `architecture-decisions` |
| 2. Project Status | Glob `.shipkit/**/*.md` | `project-status` |
| 3. Quality Checklist | `.shipkit/implementations.md`, `.shipkit/specs/active/*.md` | `quality-checklist` |
| 4. Component Documentation | `.shipkit/implementations.md` | `component-docs` |
| 5. Feature Specs | `.shipkit/specs/active/*.md` | `feature-specs` |
| 6. Implementation Plans | `.shipkit/plans/*.md` | `implementation-plans` |
| 7. Tech Stack | `.shipkit/stack.md` | `tech-stack` |
| 8. Custom | User-specified files | User-specified description |

**Description word**: Used for archive filename (2-4 kebab-case words)

---

### Step 3: Read Source Content

**Use Read tool to load source markdown files.**

**Examples:**

For architecture decisions:
```
Read: .shipkit/architecture.md
```

For project status (comprehensive):
```
Glob: .shipkit/**/*.md
Read each file found
```

For quality checklist:
```
Read: .shipkit/implementations.md
Glob: .shipkit/specs/active/*.md
```

**IMPORTANT**: Actually read files - don't generate placeholder content.

---

### Step 4: Check for Existing latest.html

**Check if `.shipkit/communications/latest.html` already exists:**

```
If latest.html exists:
  1. Get current timestamp: YYYYMMDD-HHMM format
  2. Create archive filename: YYYYMMDD-HHMM-{description}.html
     Example: 20251228-1430-architecture-decisions.html
  3. Use Read tool to read latest.html content
  4. Use Write tool to create archive:
     Path: .shipkit/communications/archive/{timestamp}-{description}.html
     Content: [contents of old latest.html]
  5. Proceed to generate new latest.html

If latest.html does NOT exist:
  1. Proceed directly to generate new latest.html
```

**Archive naming examples:**
- `20251228-1430-architecture-decisions.html`
- `20251228-1515-project-status.html`
- `20251228-1620-quality-checklist.html`

---

### Step 5: Generate HTML

**Create beautiful, styled HTML using the template structure.**

**Complete HTML template**: See `references/html-template.md`

**Key template features**:
- Purple gradient theme (`#667eea` → `#764ba2`)
- Responsive design (mobile-friendly)
- Mermaid.js support via CDN
- Inline CSS (no external dependencies)
- Clean typography and spacing

**Template variables to replace**:
- `{Report Title}` - Main title
- `{Report Subtitle}` - Subtitle
- `{Current DateTime}` - Full timestamp
- `{Current Date}` - Date only
- `{CONVERTED MARKDOWN CONTENT HERE}` - HTML-converted content

**Content Conversion Rules:**

1. **Markdown to HTML**: Convert markdown content to semantic HTML
   - `# Header` → `<h2>`
   - `## Header` → `<h3>`
   - `### Header` → `<h4>`
   - `**bold**` → `<strong>`
   - `*italic*` → `<em>`
   - Lists → `<ul>` / `<ol>`
   - Code blocks → `<pre><code>`
   - Inline code → `<code>`
   - Tables → `<table>`

2. **Special Sections**: Wrap important sections in cards
   - Decisions → `.card` div
   - Warnings → `.card` with warning style
   - Key points → `.card`

3. **Mermaid Diagrams**: Detect markdown code blocks with `mermaid` language:
   ````markdown
   ```mermaid
   graph TD
   A --> B
   ```
   ````
   Convert to:
   ```html
   <div class="mermaid">
   graph TD
   A --> B
   </div>
   ```

4. **Timestamps**: Use current datetime in header

**Report Title Examples:**
- "Architecture Decisions"
- "Project Status Dashboard"
- "Quality Confidence Report"
- "Component Documentation"

---

### Step 6: Write latest.html

**Use Write tool to create:**

**Location**: `.shipkit/communications/latest.html`

**Content**: Complete HTML generated in Step 5

**Example Write call:**
```
Write tool:
  File: .shipkit/communications/latest.html
  Content: [Full HTML from Step 5]
```

---

### Step 7: Confirm to User

**After creating HTML, tell user:**

```
✅ Visual HTML report created

📁 Location: .shipkit/communications/latest.html

📊 Report type: {Description}

{IF ARCHIVED}
🗄️  Previous report archived:
   .shipkit/communications/archive/{timestamp}-{description}.html
{END IF}

👉 Open latest.html in your browser to view the report.
```

---

## Workspace Structure

**This skill creates:**

```
.shipkit/
  communications/
    latest.html                                    # Always current report
    archive/
      20251228-1430-architecture-decisions.html   # Previous reports
      20251228-1515-project-status.html
      20251228-1620-quality-checklist.html
```

**Always one `latest.html`** - Easy to find current report

**Archive preserves history** - Never lose previous visualizations

---

## Completion Checklist

Copy and track:
- [ ] Identified source content to visualize
- [ ] Generated HTML with appropriate styling
- [ ] Saved to appropriate location

---

## What Makes This "Lite"

**Included**:
- ✅ Beautiful purple gradient theme
- ✅ Responsive design (mobile-friendly)
- ✅ Mermaid diagram support (via CDN)
- ✅ Inline CSS (no external dependencies)
- ✅ Archive mechanism (timestamp-based)
- ✅ Markdown to HTML conversion
- ✅ Multiple report types
- ✅ One-command generation

**Not included** (vs hypothetical full version):
- ❌ Multiple themes/customization
- ❌ PDF export
- ❌ Email integration
- ❌ Scheduled generation
- ❌ Diff/comparison views
- ❌ Interactive charts

**Philosophy**: Create beautiful, shareable HTML quickly. One command, immediate results.

---

## Content Type Examples

### 1. Architecture Decisions

**Source**: `.shipkit/architecture.md`

**Converts to**: Visual timeline with cards for each decision, showing:
- Decision date
- What was decided
- Rationale
- Alternatives considered

**Good for**: Team alignment, onboarding, documentation

---

### 2. Project Status Dashboard

**Source**: All `.shipkit/**/*.md` files

**Converts to**: Comprehensive dashboard with:
- Tech stack summary
- Active specs (count + list)
- Implementation plans (count + list)
- Recent decisions
- Component inventory

**Good for**: Stakeholder updates, weekly reviews

---

### 3. Quality Checklist

**Source**: `.shipkit/implementations.md` + specs

**Converts to**: Interactive checklist with:
- All components listed
- Acceptance criteria per spec
- Implementation status
- Quality gates

**Good for**: Pre-ship reviews, QA handoff

---

### 4. Component Documentation

**Source**: `.shipkit/implementations.md`

**Converts to**: Component catalog with:
- Each component in a card
- Props/interfaces
- Usage examples
- File locations

**Good for**: Developer reference, onboarding

---

## Integration with Other Skills

**Before shipkit-communications**:
- Any skill that creates `.shipkit/` content
- Examples:
  - `/shipkit-architecture-memory` → Visualize decisions
  - `/shipkit-project-status` → Visualize status
  - `verify manually` → Visualize checklist
  - `document components manually` → Visualize docs

**After shipkit-communications**:
- Share HTML with team
- Present in meetings
- Continue current workflow

**When to use**:
- Need visual format for presentation
- Sharing with non-technical stakeholders
- Want shareable artifact (email, Slack, etc.)
- Prefer visual review over markdown

---

## Context Files This Skill Reads

**Depends on visualization type** (see Step 2):
- `.shipkit/architecture.md` - Architecture decisions
- `.shipkit/implementations.md` - Components/routes
- `.shipkit/stack.md` - Tech stack
- `.shipkit/specs/active/*.md` - Specifications
- `.shipkit/plans/*.md` - Implementation plans
- Any `.shipkit/**/*.md` - Custom/comprehensive

**Lazy loading**: Only reads what's needed for chosen visualization

---

## Context Files This Skill Writes

**Creates/Updates**:
- `.shipkit/communications/latest.html` - OVERWRITE AND REPLACE
  - **Write Strategy**: OVERWRITE AND REPLACE
  - **Behavior**: Always contains most recent visualization
  - **Why**: "latest" means current - old versions go to archive

**Archives**:
- `.shipkit/communications/archive/{timestamp}-{description}.html` - APPEND
  - **Write Strategy**: APPEND (create new file)
  - **Behavior**: Archives old latest.html before overwriting
  - **Why**: Preserve history, never lose previous visualizations

**Never modifies source files**: All `.shipkit/*.md` files are read-only

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Visualization is complete when:
- [ ] User specified what to visualize
- [ ] Source files read successfully
- [ ] Old latest.html archived (if existed)
- [ ] New latest.html created
- [ ] HTML renders correctly in browser
- [ ] Mermaid diagrams render (if present)
- [ ] Styling matches ShipKit Lite purple theme
- [ ] Mobile-responsive
- [ ] User knows where to find latest.html
<!-- /SECTION:success-criteria -->
---

## Common Scenarios

### Scenario 1: Architecture Decisions for Team Review

```
User: "Visualize the architecture decisions"

Claude:
1. Ask confirmation (already clear)
2. Read: .shipkit/architecture.md
3. Check for latest.html (exists)
4. Archive old: archive/20251228-1430-architecture-decisions.html
5. Generate HTML with:
   - Timeline of decisions
   - Each decision as a card
   - Rationale highlighted
   - Alternatives in tables
6. Write: latest.html
7. Confirm: "✅ Architecture decisions visualized. Open .shipkit/communications/latest.html"
```

### Scenario 2: Project Status for Stakeholders

```
User: "Create HTML report for weekly update"

Claude:
1. Ask: "What type of report?"
2. User: "Project status"
3. Glob: .shipkit/**/*.md
4. Read all markdown files
5. No existing latest.html (first time)
6. Generate comprehensive dashboard HTML
7. Write: latest.html
8. Confirm: "✅ Project status dashboard created"
```

### Scenario 3: Quality Checklist Before Launch

```
User: "Show me quality checklist as HTML"

Claude:
1. Ask confirmation
2. Read: implementations.md + specs/active/*.md
3. Check latest.html (exists)
4. Archive: archive/20251228-1620-quality-checklist.html
5. Generate checklist HTML with:
   - All acceptance criteria
   - Component verification
   - Quality gates
6. Write: latest.html
7. Confirm with next steps
```

---

## Tips for Effective Visualizations

**Choose the right type**:
- Architecture decisions → Best for team alignment
- Project status → Best for stakeholder updates
- Quality checklist → Best for pre-ship reviews
- Component docs → Best for developer reference

**When to regenerate**:
- After significant changes to source content
- Before team meetings/presentations
- Weekly for status updates
- Before sharing with stakeholders

**Archive benefits**:
- Compare how project evolved over time
- Reference past visualizations
- Track decision-making history
- Never lose previous reports

**Sharing tips**:
- latest.html is self-contained (inline CSS)
- No external dependencies (except Mermaid CDN)
- Works offline after initial load
- Email-friendly (single file)
- Mobile-responsive for phone viewing

---

## Markdown to HTML Conversion Guide

**Quick reference**:
- Headers: `#` → `<h2>`, `##` → `<h3>`, `###` → `<h4>`
- Emphasis: `**bold**` → `<strong>`, `*italic*` → `<em>`, `` `code` `` → `<code>`
- Lists: `-` → `<ul><li>`, `1.` → `<ol><li>`
- Code blocks with language support
- Tables with header/body structure
- Mermaid diagrams: ` ```mermaid ` → `<div class="mermaid">`

---

**Remember**: This skill is about making ShipKit Lite content beautiful and shareable. Always read actual content, never generate placeholders. Archive old reports to preserve history.
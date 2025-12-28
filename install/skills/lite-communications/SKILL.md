---
name: lite-communications
description: Transform any ShipKit Lite content into visual HTML reports. Creates styled, shareable HTML from architecture decisions, project status, quality checks, or any .shipkit-lite/ content.
---

# lite-communications - Visual HTML Reports

**Purpose**: Create beautiful, visual HTML reports from any ShipKit Lite content for presentations, sharing, or visual review.

**What it does**: Reads markdown content from `.shipkit-lite/`, generates styled HTML with purple gradient theme, archives old reports, creates `latest.html`.

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
- `.shipkit-lite/architecture.md` - For architecture decisions
- `.shipkit-lite/implementations.md` - For component/route docs
- `.shipkit-lite/stack.md` - For tech stack overview
- `.shipkit-lite/specs/active/*.md` - For specs
- `.shipkit-lite/plans/*.md` - For implementation plans

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

**Based on user choice, identify which .shipkit-lite/ files to read:**

| Choice | Files to Read | Description Word |
|--------|---------------|------------------|
| 1. Architecture Decisions | `.shipkit-lite/architecture.md` | `architecture-decisions` |
| 2. Project Status | Glob `.shipkit-lite/**/*.md` | `project-status` |
| 3. Quality Checklist | `.shipkit-lite/implementations.md`, `.shipkit-lite/specs/active/*.md` | `quality-checklist` |
| 4. Component Documentation | `.shipkit-lite/implementations.md` | `component-docs` |
| 5. Feature Specs | `.shipkit-lite/specs/active/*.md` | `feature-specs` |
| 6. Implementation Plans | `.shipkit-lite/plans/*.md` | `implementation-plans` |
| 7. Tech Stack | `.shipkit-lite/stack.md` | `tech-stack` |
| 8. Custom | User-specified files | User-specified description |

**Description word**: Used for archive filename (2-4 kebab-case words)

---

### Step 3: Read Source Content

**Use Read tool to load source markdown files.**

**Examples:**

For architecture decisions:
```
Read: .shipkit-lite/architecture.md
```

For project status (comprehensive):
```
Glob: .shipkit-lite/**/*.md
Read each file found
```

For quality checklist:
```
Read: .shipkit-lite/implementations.md
Glob: .shipkit-lite/specs/active/*.md
```

**IMPORTANT**: Actually read files - don't generate placeholder content.

---

### Step 4: Check for Existing latest.html

**Check if `.shipkit-lite/communications/latest.html` already exists:**

```
If latest.html exists:
  1. Get current timestamp: YYYYMMDD-HHMM format
  2. Create archive filename: YYYYMMDD-HHMM-{description}.html
     Example: 20251228-1430-architecture-decisions.html
  3. Use Read tool to read latest.html content
  4. Use Write tool to create archive:
     Path: .shipkit-lite/communications/archive/{timestamp}-{description}.html
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

**Create beautiful, styled HTML using this structure:**

#### HTML Template Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Report Title} - ShipKit Lite</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1e293b;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            min-height: 100vh;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }

        header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }

        header .subtitle {
            font-size: 1.3em;
            opacity: 0.95;
            margin-bottom: 10px;
        }

        header .timestamp {
            font-size: 1em;
            opacity: 0.8;
        }

        .content {
            padding: 60px 40px;
        }

        h2 {
            font-size: 2.2em;
            color: #667eea;
            margin: 40px 0 20px 0;
            border-bottom: 3px solid #e2e8f0;
            padding-bottom: 10px;
        }

        h3 {
            font-size: 1.6em;
            color: #764ba2;
            margin: 30px 0 15px 0;
        }

        h4 {
            font-size: 1.3em;
            color: #475569;
            margin: 20px 0 10px 0;
        }

        p {
            margin: 15px 0;
            font-size: 1.05em;
            line-height: 1.8;
        }

        ul, ol {
            margin: 15px 0 15px 30px;
            line-height: 1.8;
        }

        li {
            margin: 8px 0;
        }

        code {
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
        }

        pre {
            background: #1e293b;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
        }

        pre code {
            background: none;
            color: inherit;
            padding: 0;
        }

        .card {
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            padding: 25px;
            margin: 25px 0;
            border-radius: 8px;
        }

        .card h3 {
            margin-top: 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }

        th {
            background: #667eea;
            color: white;
            font-weight: bold;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .mermaid {
            background: white;
            padding: 20px;
            margin: 30px 0;
            border-radius: 8px;
        }

        footer {
            background: #1e293b;
            color: white;
            padding: 30px 40px;
            text-align: center;
        }

        footer p {
            opacity: 0.8;
            margin: 5px 0;
        }

        @media (max-width: 768px) {
            header h1 {
                font-size: 2em;
            }
            .content {
                padding: 30px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{Report Title}</h1>
            <p class="subtitle">{Report Subtitle}</p>
            <p class="timestamp">Generated: {Current DateTime}</p>
        </header>

        <div class="content">
            {CONVERTED MARKDOWN CONTENT HERE}
        </div>

        <footer>
            <p>Generated by ShipKit Lite</p>
            <p>{Current Date}</p>
        </footer>
    </div>

    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default'
        });
    </script>
</body>
</html>
```

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

**Location**: `.shipkit-lite/communications/latest.html`

**Content**: Complete HTML generated in Step 5

**Example Write call:**
```
Write tool:
  File: .shipkit-lite/communications/latest.html
  Content: [Full HTML from Step 5]
```

---

### Step 7: Confirm to User

**After creating HTML, tell user:**

```
✅ Visual HTML report created

📁 Location: .shipkit-lite/communications/latest.html

📊 Report type: {Description}

{IF ARCHIVED}
🗄️  Previous report archived:
   .shipkit-lite/communications/archive/{timestamp}-{description}.html
{END IF}

👉 Open latest.html in your browser to view the report.
```

---

## Workspace Structure

**This skill creates:**

```
.shipkit-lite/
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

**Source**: `.shipkit-lite/architecture.md`

**Converts to**: Visual timeline with cards for each decision, showing:
- Decision date
- What was decided
- Rationale
- Alternatives considered

**Good for**: Team alignment, onboarding, documentation

---

### 2. Project Status Dashboard

**Source**: All `.shipkit-lite/**/*.md` files

**Converts to**: Comprehensive dashboard with:
- Tech stack summary
- Active specs (count + list)
- Implementation plans (count + list)
- Recent decisions
- Component inventory

**Good for**: Stakeholder updates, weekly reviews

---

### 3. Quality Checklist

**Source**: `.shipkit-lite/implementations.md` + specs

**Converts to**: Interactive checklist with:
- All components listed
- Acceptance criteria per spec
- Implementation status
- Quality gates

**Good for**: Pre-ship reviews, QA handoff

---

### 4. Component Documentation

**Source**: `.shipkit-lite/implementations.md`

**Converts to**: Component catalog with:
- Each component in a card
- Props/interfaces
- Usage examples
- File locations

**Good for**: Developer reference, onboarding

---

## Integration with Other Skills

**Before lite-communications**:
- Any skill that creates `.shipkit-lite/` content
- Examples:
  - `/lite-architecture-memory` → Visualize decisions
  - `/lite-project-status` → Visualize status
  - `/lite-quality-confidence` → Visualize checklist
  - `/lite-component-knowledge` → Visualize docs

**After lite-communications**:
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
- `.shipkit-lite/architecture.md` - Architecture decisions
- `.shipkit-lite/implementations.md` - Components/routes
- `.shipkit-lite/stack.md` - Tech stack
- `.shipkit-lite/specs/active/*.md` - Specifications
- `.shipkit-lite/plans/*.md` - Implementation plans
- Any `.shipkit-lite/**/*.md` - Custom/comprehensive

**Lazy loading**: Only reads what's needed for chosen visualization

---

## Context Files This Skill Writes

**Creates/Updates**:
- `.shipkit-lite/communications/latest.html` - OVERWRITE AND REPLACE
  - **Write Strategy**: OVERWRITE AND REPLACE
  - **Behavior**: Always contains most recent visualization
  - **Why**: "latest" means current - old versions go to archive

**Archives**:
- `.shipkit-lite/communications/archive/{timestamp}-{description}.html` - APPEND
  - **Write Strategy**: APPEND (create new file)
  - **Behavior**: Archives old latest.html before overwriting
  - **Why**: Preserve history, never lose previous visualizations

**Never modifies source files**: All `.shipkit-lite/*.md` files are read-only

---

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

---

## Common Scenarios

### Scenario 1: Architecture Decisions for Team Review

```
User: "Visualize the architecture decisions"

Claude:
1. Ask confirmation (already clear)
2. Read: .shipkit-lite/architecture.md
3. Check for latest.html (exists)
4. Archive old: archive/20251228-1430-architecture-decisions.html
5. Generate HTML with:
   - Timeline of decisions
   - Each decision as a card
   - Rationale highlighted
   - Alternatives in tables
6. Write: latest.html
7. Confirm: "✅ Architecture decisions visualized. Open .shipkit-lite/communications/latest.html"
```

### Scenario 2: Project Status for Stakeholders

```
User: "Create HTML report for weekly update"

Claude:
1. Ask: "What type of report?"
2. User: "Project status"
3. Glob: .shipkit-lite/**/*.md
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

**Headers**:
```markdown
# Title         → <h2>Title</h2>
## Section      → <h3>Section</h3>
### Subsection  → <h4>Subsection</h4>
```

**Emphasis**:
```markdown
**bold**   → <strong>bold</strong>
*italic*   → <em>italic</em>
`code`     → <code>code</code>
```

**Lists**:
```markdown
- Item 1      → <ul><li>Item 1</li>...
1. Item 1     → <ol><li>Item 1</li>...
```

**Code blocks**:
````markdown
```javascript
code
```
````
Becomes:
```html
<pre><code class="language-javascript">code</code></pre>
```

**Tables**:
```markdown
| A | B |
|---|---|
| 1 | 2 |
```
Becomes:
```html
<table>
  <thead><tr><th>A</th><th>B</th></tr></thead>
  <tbody><tr><td>1</td><td>2</td></tr></tbody>
</table>
```

**Links**:
```markdown
[text](url)  → <a href="url">text</a>
```

**Blockquotes**:
```markdown
> Quote  → <blockquote>Quote</blockquote>
```

---

**Remember**: This skill is about making ShipKit Lite content beautiful and shareable. Always read actual content, never generate placeholders. Archive old reports to preserve history.

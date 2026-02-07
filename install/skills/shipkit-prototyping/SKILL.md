---
name: shipkit-prototyping
description: "Use when user wants to quickly mockup UI before implementing. Triggers: 'prototype', 'mockup', 'quick UI', 'sketch this'."
argument-hint: "<component or feature>"
---

# shipkit-prototyping - Rapid UI Prototyping

**Purpose**: Create interactive UI prototypes for immediate user feedback and rapid iteration before committing to full implementation.

**What it does**: Scaffolds single-file React + Tailwind prototypes via CDN (no build step), enables live iteration with user viewing changes in real-time, supports importing existing mockups.

---

## When to Invoke

**User triggers**:
- "Create a prototype"
- "Build a mockup"
- "Rapid prototype for [feature]"
- "Mock up the UI"
- "Test the interface idea"

**Suggested after**:
- `/shipkit-spec` - Spec exists, ready to visualize UI
- User describes a UI idea they want to validate quickly

**Use cases**:
- Validate UI/UX concepts before full implementation
- Get user feedback on interactions and layout
- Explore multiple design approaches quickly
- Test usability assumptions with real users
- Create throwaway prototypes for stakeholder demos

---

## Prerequisites

**Recommended (spec-first workflow):**
- `.shipkit/specs/active/[feature].json` - Feature spec provides context
  - **Workflow:** Create spec first with `/shipkit-spec`, then prototype from it
  - **Why:** Spec clarifies requirements before exploring UI solutions
  - **Warning if missing:** Skill will prompt to create spec first

**Optional (enhances prototyping):**
- `.shipkit/why.json` - Vision informs design choices (brand, audience)

**Not required:**
- No implementation needed
- No design system required (Tailwind provides utility classes)
- Can prototype without prior work (if user insists, skip spec check)

---

## The Iron Laws

**IRON LAW #1: PROTOTYPE IS DISPOSABLE**
```
THE PROTOTYPE IS NOT PRODUCTION CODE.
IT EXISTS TO LEARN, NOT TO SHIP.
DELETE IT AFTER EXTRACTING INSIGHTS.
```

**Why:** Prototypes use shortcuts (inline styles, hardcoded data). Shipping them creates technical debt. Value is learning, not code.

**Red flags:** "Clean up and ship it", "80% done", "Refactor into production"

**Instead:** Extract to spec, rebuild properly, keep as reference only

---

**IRON LAW #2: ITERATE WITH USER WATCHING**
```
NEVER BUILD IN ISOLATION.
USER WATCHES LIVE UPDATES.
FEEDBACK DRIVES EVERY CHANGE.
```

**Why:** UX assumptions are usually wrong. Real users reveal issues immediately. Live iteration is 10x faster than build-review-rebuild.

**Red flags:** "Finish then show", "Polish first", "I know what users want"

**Instead:** Share screen, change→save→user sees in 2s, ask "How does this feel?", iterate until "yes, that's it"

---

**IRON LAW #3: NO BACKEND, NO BUILD STEP**
```
SINGLE HTML FILE WITH CDN IMPORTS.
NO NPM, NO BUNDLER, NO API CALLS.
WORKS BY DOUBLE-CLICKING THE FILE.
```

**Why:** Setup time kills iteration. User sees prototype in seconds, not minutes. Focus on UI/UX, not infrastructure.

**Red flags:** "Set up Vite", "npm install", "Connect to API"

**Instead:** One `.html` with React + Tailwind CDN, mock data in state, Babel transpiles in browser

---

## Process

### Step 1: Understand What to Prototype

**FIRST: Check for spec (spec-first workflow enforcement)**

**Check if spec exists:**
```bash
ls .shipkit/specs/active/*.json 2>/dev/null
```

**If NO spec found:**
```
⚠️  No spec found in .shipkit/specs/active/

Recommended: Create a spec first with /shipkit-spec
- Spec clarifies requirements before exploring UI
- Prototyping without spec risks building wrong solution

Options:
1. Create spec first (recommended): Run /shipkit-spec now
2. Proceed without spec: I'll ask questions to understand requirements

Which option? (1/2)
```

**If user chooses "1":** Invoke `/shipkit-spec` now, then return to prototyping after spec created
**If user chooses "2":** Proceed with questions below (user takes responsibility for no spec)

---

**If spec EXISTS or user chose to proceed without:**

**Ask user 2-3 questions:**

**1. What feature/interaction are we prototyping?**
```
Example responses:
- "Recipe sharing flow - user clicks share, gets link"
- "Dark mode toggle in settings"
- "Onboarding wizard with 3 steps"

If spec exists: Reference spec name, ask which part to prototype
```

**2. What's the core interaction to validate?**
```
Focus on the ONE thing that's risky or uncertain:
- "Does the share button placement feel natural?"
- "Is the toggle obvious enough?"
- "Do users understand the wizard flow?"
```

**3. Do you have an existing mockup to start from?**
```
Options:
a) Start from scratch (Claude generates React + Tailwind HTML)
b) Import existing HTML (user provides file/zip)
c) Reference a spec (Claude reads spec and generates from it)
```

**Read context if available:**
- `.shipkit/specs/active/[feature].json` - Read spec for requirements
- `.shipkit/why.json` - Understand brand/audience for design choices

**Token budget:** Keep context reading under 1000 tokens

---

### Step 2: Create Prototype Structure

**Determine prototype name:**
```
Ask: "What should we call this prototype?"
Default: Use feature name from spec or user description
Example: "recipe-share-v1"

Store as: prototype_name
```

**Create folder structure:**
```
.shipkit-mockups/
  [prototype_name]/
    index.html          # Main prototype file
    README.md           # What this prototype explores
    iterations.md       # Log of changes made during session
```

**If importing existing mockup:**
```
User provides .zip file → extract to .shipkit-mockups/[name]/
Preserve existing structure
Note: Skip Step 3, go directly to Step 4 (iterate)
```

---

### Step 3: Generate Initial HTML Prototype

**Create single-file HTML with React + Tailwind via CDN:**

**Basic template structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Feature Name] Prototype</title>

    <!-- Tailwind CSS via CDN -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- React + ReactDOM + Babel via CDN -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState } = React;

        function App() {
            // State and mock data here
            return (
                <div className="min-h-screen bg-gray-50 p-4">
                    {/* Component UI with Tailwind classes */}
                </div>
            );
        }

        ReactDOM.render(<App />, document.getElementById('root'));
    </script>
</body>
</html>
```

**Why React + Tailwind via CDN:**
- **React:** Component structure, state management (`useState`, etc.)
- **Tailwind:** Rapid styling with utility classes (no custom CSS)
- **CDN:** No build step, no npm install, works by double-clicking file
- **Babel:** Enables JSX syntax in browser

**Design principles:**
1. **Mobile-first** - Tailwind responsive classes (`sm:`, `md:`, `lg:`)
2. **Accessible** - Semantic HTML, ARIA labels, keyboard nav
3. **Interactive** - All buttons/clicks update state
4. **Mock data** - Hardcode realistic examples (no API calls)

**See `references/examples.md` for complete working example with share button, toast notifications, and state management.**

**Write to:** `.shipkit-mockups/[name]/index.html`

**Also create README:**
```markdown
# [Prototype Name]

## What This Explores
[One sentence: what UI/UX question this prototype answers]

## How to View
Double-click `index.html` or serve via `python -m http.server 8000`

## Core Interactions
- [Key interactions to test]

## Limitations
Mock data only, single-page, disposable code (not production-ready)
```

**Write to:** `.shipkit-mockups/[name]/README.md`

---

### Step 4: Iterate with User (The Core Loop)

**CRITICAL: User must have prototype open in browser during this step.**

**Tell user:**
```
Open the prototype now:
1. Navigate to: .shipkit-mockups/[name]/
2. Double-click index.html (or serve via http.server)
3. Keep browser window visible

Ready? I'll make changes and you'll see them live.
```

**Iteration loop:**

```
1. Ask: "What should we change?"

2. User responds with feedback:
   - "The button is too small"
   - "Move the share button to the top right"
   - "Add a confirmation message after clicking"
   - "The colors feel wrong"

3. Make the change:
   - Edit index.html inline
   - Show user the specific change made
   - Tell user: "Saved. Refresh browser to see update."

4. User refreshes browser, sees change

5. Ask: "How does that feel? What's next?"

6. Repeat until user says "this is good" or session ends
```

**Keep iteration log:**

Append each change to `.shipkit-mockups/[name]/iterations.md`:
```markdown
## [Timestamp] - [Change]
**Feedback**: "Button is too small"
**Change**: Increased padding 8px → 16px, font 14px → 16px
**Response**: "Better, but still feels cramped"
```

**Iteration speed is critical:**
- Keep changes small (one thing at a time)
- Make change → save → user sees result in <10 seconds
- Don't overthink - prototype is disposable
- Follow user's instinct over design theory

---

### Step 5: Extract Key Learnings

**After iteration loop complete (user says "done" or "good enough"):**

**Ask user:**
```
What did we learn from this prototype?

Specifically:
1. What worked well? (keep for implementation)
2. What didn't work? (avoid in implementation)
3. Any surprises? (unexpected user reactions)
```

**Append to iterations.md:**
```markdown
---
## Key Learnings
**Worked**: [User-validated decisions, successful interactions]
**Didn't Work**: [Failed approaches, confusing elements]
**Surprises**: [Unexpected behavior, wrong assumptions]
**Next**: Extract to spec via `/shipkit-prototype-to-spec` or continue iterating
```

---

### Step 6: Archive or Continue

**Ask user what's next:**
1. **New variant** → Copy to `[name]-v2/`, iterate on different approach
2. **Extract to spec** → Run `/shipkit-prototype-to-spec` to capture UI/UX decisions
3. **Move to implementation** → Prototype stays as reference, proceed to `/shipkit-plan`

**Note:** Delete prototype after implementation ships (served its learning purpose)

---

## When This Skill Integrates with Others

### Before This Skill

**shipkit-spec** - Creates feature specification
- **When**: Spec exists and describes functionality, ready to explore UI
- **Why**: Spec provides context for what to prototype
- **Trigger**: User asks "can we prototype this?" after writing spec

**shipkit-why-project** - Defines project vision
- **When**: Vision defines target audience and brand direction
- **Why**: Informs design choices (professional vs playful, mobile-first vs desktop)
- **Trigger**: Brand guidelines affect prototype aesthetics

### After This Skill

**shipkit-prototype-to-spec** - Extracts prototype learnings into spec
- **When**: Prototype iteration complete, ready to document UI/UX decisions
- **Why**: Preserve validated UI patterns for implementation
- **Trigger**: User says "extract this to the spec" or "done prototyping"

**shipkit-plan** - Creates implementation plan
- **When**: Prototype validated, ready to plan real implementation
- **Why**: Prototype serves as reference for what to build
- **Trigger**: User says "let's build this for real" after prototyping

**shipkit-architecture-memory** - Documents UX design decisions
- **When**: Prototype validated and UX patterns established
- **Why**: Capture UX rationale from prototyping for future reference
- **Trigger**: Prototype complete, design decisions need documentation

### Special Relationships

**Can run standalone** - No prerequisites required
- **When**: User has UI idea they want to validate quickly
- **Why**: Prototyping is fastest way to explore uncertain UI decisions
- **Trigger**: User describes UI concept verbally

**Complements shipkit-spec** - Not a replacement
- **When**: Spec describes functionality, prototype explores UI
- **Why**: Spec = what it does, Prototype = how it feels
- **Trigger**: Both exist for same feature

---

## Context Files This Skill Reads

**Optional (enhances prototyping):**
- `.shipkit/specs/active/[feature].json` - Feature context
- `.shipkit/why.json` - Vision and brand direction
- `.shipkit/implementations.json` - Existing component patterns to reuse

**User-provided:**
- Existing mockup files (.html, .zip) if importing

---

## Context Files This Skill Writes

**Creates in `.shipkit-mockups/[name]/`:**
- `index.html` - Main prototype (CREATE then ITERATE during session)
- `README.md` - What this prototype explores (CREATE once)
- `iterations.md` - Change log (APPEND each iteration)

**Never modifies specs or implementation** - Prototypes are separate throwaway artifacts

---

---

## Red Flags

### Red Flag 1: Building Without User Present
**Symptom:** "Finish then show", creating elaborate UI alone
**Why wrong:** Defeats rapid iteration, wastes effort
**Fix:** Stop, get user on screen, show incomplete work, iterate together

### Red Flag 2: Over-Engineering
**Symptom:** "Add Router", "Set up TypeScript", "Connect API", separate files
**Why wrong:** Setup kills speed, disposable code, obscures core interaction
**Fix:** Single HTML, CDN imports, conditional rendering, mock data, one file

### Red Flag 3: Shipping the Prototype
**Symptom:** "80% done, ship it", clean up and deploy, reluctance to delete
**Why wrong:** Shortcuts create tech debt, needs proper architecture
**Fix:** Extract to spec via `/shipkit-prototype-to-spec`, rebuild with `/shipkit-plan`, delete after shipping

---

## Tips, Scenarios, and Examples

**See `references/examples.md` for:**
- Tips for effective prototyping (mobile-first, real content, focus on one interaction)
- Common scenarios (validating flows, comparing approaches, importing mockups)
- Complete React + Tailwind example template
- Template variations (multi-step flows, forms, lists)

---

**Remember:** Prototype is disposable. Value is in learning, not code. Iterate fast, extract insights, delete after shipping.

---

<!-- SECTION:success-criteria -->
## Success Criteria

Prototyping is complete when:
- [ ] User's UI/UX question clearly defined
- [ ] Single-file HTML prototype created in `.shipkit-mockups/[name]/`
- [ ] User has viewed prototype in browser
- [ ] At least one iteration cycle completed with user feedback
- [ ] Key learnings documented in `iterations.md`
- [ ] Next step decided: new variant, extract to spec, or move to implementation
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
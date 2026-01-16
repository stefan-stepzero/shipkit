# Interaction Design Reference

Extended guidance for creating user journeys and interaction patterns.

## Table of Contents

- User Journey Mapping Fundamentals
- Interaction Design Principles
- Common UX Patterns
- Mobile vs Desktop Considerations
- Accessibility Guidelines
- Testing & Validation

---

## User Journey Mapping Fundamentals

### What is a User Journey?

A user journey maps the complete experience a user has with your product, from initial awareness through to advocacy. It's not just a feature list or screen flow—it's a narrative of the user's thoughts, feelings, and actions at each stage.

**Key Components:**
1. **Stages** - Phases in the user's relationship with your product
2. **Touchpoints** - Specific interactions between user and product
3. **User Actions** - What the user does
4. **User Thoughts** - What they're thinking/wondering
5. **User Emotions** - How they feel (frustration, delight, confusion)
6. **Opportunities** - Where we can improve the experience

### Journey Mapping Process

**Step 1: Define Scope**
- Which persona? (Focus on one at a time)
- Which job to be done? (One journey per JTBD)
- What time period? (First hour? First week? First year?)
- What success looks like? (Clear outcome)

**Step 2: Research Current State**
- Shadow real users (if product exists)
- Interview users about their current workflows
- Analyze support tickets and error logs
- Review session recordings
- Map what actually happens (not what you wish happened)

**Step 3: Identify Pain Points**
- Where do users get stuck?
- Where do they abandon?
- Where do they use workarounds?
- Where is there unnecessary friction?
- Where are the emotion valleys (frustration, confusion)?

**Step 4: Design Future State**
- How do we remove friction?
- How do we create emotion peaks (delight, accomplishment)?
- How do we guide users to success?
- What can we automate or simplify?
- What defaults can we provide?

**Step 5: Validate**
- Create prototypes
- Test with real users
- Measure success metrics
- Iterate based on findings

### Stages in a Complete User Journey

**1. Awareness / Discovery**
- User realizes they have a problem
- Searches for solutions
- Discovers your product exists
- Forms first impression

**Key Questions:**
- How do users find us?
- What are they looking for when they arrive?
- What's their emotional state?
- What makes them stay vs. leave immediately?

**2. Consideration / Evaluation**
- User explores what you offer
- Compares to alternatives
- Evaluates if this solves their problem
- Assesses effort/cost vs. benefit

**Key Questions:**
- What information do they need to decide?
- What concerns or objections arise?
- How do they evaluate alternatives?
- What tips them toward "yes"?

**3. First Use / Onboarding**
- User commits (sign up, purchase, download)
- Gets started for first time
- Tries to accomplish first goal
- Experiences initial value (or doesn't)

**Key Questions:**
- How quickly can they reach value?
- What obstacles prevent them from starting?
- What causes early abandonment?
- What creates the "aha!" moment?

**Critical Concept: Time to Value (TTV)**
- How long from sign up to first value?
- Target: Under 5 minutes for POC/MVP, under 2 minutes for established
- Measure: Track "time to aha!" moment

**4. Regular Use / Habit Formation**
- User incorporates product into workflow
- Builds habits and patterns
- Discovers additional features
- Becomes proficient

**Key Questions:**
- How often do they use it?
- What's the core loop (trigger → action → reward)?
- How do they discover features?
- What keeps them coming back?

**Habit Formation Loop:**
1. Trigger (internal or external)
2. Action (easy to do)
3. Variable reward (satisfying outcome)
4. Investment (builds commitment)

**5. Power Use / Mastery**
- User becomes expert
- Uses advanced features
- Optimizes workflows
- Seeks efficiency

**Key Questions:**
- How do we reveal power without overwhelming beginners?
- What shortcuts and bulk actions matter?
- How do users customize to their needs?
- What prevents complexity from overwhelming?

**6. Retention / Continued Engagement**
- User continues using over time
- Finds ongoing value
- Resists switching to alternatives
- Expands usage

**Key Questions:**
- Why would they stop using it?
- How do we stay relevant as needs evolve?
- What new value can we provide?
- How do we re-engage if they lapse?

**7. Advocacy / Referral**
- User recommends to others
- Shares successes publicly
- Provides testimonials
- Brings in team/colleagues

**Key Questions:**
- What makes them excited to share?
- Who would they tell about this?
- What would they say?
- How do we make sharing easy?

---

## Interaction Design Principles

### Principle 1: Minimize Cognitive Load

**What it means:**
Don't make users think harder than necessary. Every decision, every piece of information, every option increases mental effort.

**How to apply:**
- **Progressive disclosure:** Show only what's needed right now
- **Sensible defaults:** 80% should never change settings
- **Clear labels:** "Save changes" not "Submit"
- **Reduce choices:** 3-5 options max for most decisions
- **Chunking:** Group related items (7±2 rule)

**Examples:**
- ✅ Google search: One field, one button
- ❌ Advanced search with 15 filters shown by default

### Principle 2: Provide Clear Feedback

**What it means:**
Users should always know: Where am I? What just happened? What can I do next? Was that successful?

**How to apply:**
- **Immediate acknowledgment:** Button press shows response <100ms
- **Progress indicators:** For anything >2 seconds
- **Success confirmation:** "Saved" toast, checkmark animation
- **Error explanation:** "Email is required" not "Invalid input"
- **State visibility:** Current page highlighted in nav

**Examples:**
- ✅ Stripe checkout: Each step shows progress, current step, what's next
- ❌ Silent failures: Form submits but nothing happens

### Principle 3: Design for Errors

**What it means:**
Users will make mistakes. Design to prevent errors, and when they happen, make recovery easy.

**How to apply:**
- **Constraints:** Disable unavailable actions
- **Validation:** Real-time feedback on form fields
- **Confirmation:** "Delete 50 items?" before destructive action
- **Undo:** Allow mistakes to be reversed
- **Helpful errors:** "Try 'project:alpha' instead of 'project alpha'"

**Error Prevention Hierarchy:**
1. Make error impossible (constraints, design)
2. Make error unlikely (defaults, guidance)
3. Make error obvious (validation, warnings)
4. Make error recoverable (undo, confirmation)

### Principle 4: Maintain Consistency

**What it means:**
Similar things should look and behave similarly. Users learn patterns and expect them to apply everywhere.

**How to apply:**
- **Visual consistency:** Same button style for all primary actions
- **Behavioral consistency:** Swipe left always does the same thing
- **Terminology consistency:** Don't alternate "Delete" and "Remove"
- **Location consistency:** Save button always bottom-right
- **Interaction consistency:** Click vs. hover vs. right-click patterns

**Platform Consistency:**
- Follow platform conventions (iOS != Android != Web)
- Don't reinvent standard controls
- Match user expectations from other apps

### Principle 5: Prioritize Ruthlessly

**What it means:**
Not everything can be prominent. The more you emphasize, the less anything stands out.

**How to apply:**
- **One primary action** per screen (big, colorful button)
- **2-3 secondary actions** (smaller, less prominent)
- **Everything else** hidden in menus/buried
- **Information hierarchy:** Big → Medium → Small
- **Visual weight:** Use size, color, position to guide attention

**Examples:**
- ✅ Mobile keyboards: Common letters bigger, rare punctuation smaller
- ❌ Enterprise software: 20 equal-sized buttons in toolbar

### Principle 6: Respect User Context

**What it means:**
Users come with different devices, abilities, time, and attention. Design for their reality, not ideal conditions.

**How to apply:**
- **Device context:** Thumb-friendly on mobile, keyboard shortcuts on desktop
- **Attention context:** Can they give full attention or are they multitasking?
- **Time context:** How much time do they have right now?
- **Accessibility context:** Works for visual, motor, cognitive differences
- **Network context:** Works on slow connections

**Contexts to Consider:**
- **Commuter on subway:** Intermittent connection, one hand, distracted
- **Office worker:** Keyboard-driven, multiple monitors, interruptions
- **Non-technical user:** Unfamiliar jargon, needs guidance
- **Power user:** Efficiency-focused, knows shortcuts, impatient

---

## Common UX Patterns

### Navigation Patterns

**1. Hub and Spoke**
- Central dashboard with links to features
- User always returns to hub
- **Good for:** Few main features, infrequent use
- **Example:** Banking app (dashboard → accounts → back to dashboard)

**2. Nested Hierarchy**
- Drill down into categories
- Breadcrumbs show path
- **Good for:** Content organization, discovery
- **Example:** E-commerce (Home → Category → Subcategory → Product)

**3. Filtered List**
- Start with everything, filter to find item
- **Good for:** Large datasets, search-heavy
- **Example:** Airbnb (all listings → filter by location, price, dates)

**4. Tab-Based**
- Switch between views of same object
- Context stays constant
- **Good for:** Different aspects of one thing
- **Example:** LinkedIn profile (Activity, Experience, Education tabs)

**5. Linear Flow (Wizard)**
- Step-by-step progression
- Can't skip ahead
- **Good for:** Onboarding, checkout, complex forms
- **Example:** TurboTax (answer questions in sequence)

### Input Patterns

**1. Smart Defaults**
- Pre-fill with most likely value
- User can change if needed
- **Example:** Country defaults to detected location

**2. Inline Editing**
- Click to edit in place
- No modal or separate edit screen
- **Good for:** Quick changes, transparency
- **Example:** Notion (click any text to edit)

**3. Autosave**
- Save in background, no manual save
- Show "Saved" indicator for confidence
- **Good for:** Content creation, long forms
- **Example:** Google Docs

**4. Typeahead / Autocomplete**
- Suggest as user types
- Reduce typing, prevent errors
- **Example:** Google search suggestions

**5. Drag and Drop**
- Move/reorder by dragging
- Visual, intuitive
- **Good for:** Reordering, file uploads, categorizing
- **Example:** Trello (drag cards between lists)

### Feedback Patterns

**1. Optimistic UI**
- Assume action succeeds, update UI immediately
- Roll back if fails
- **Good for:** Fast-feeling apps, high success rate
- **Example:** Twitter like (heart fills immediately)

**2. Loading Skeletons**
- Show layout before content loads
- Less jarring than spinner
- **Good for:** Content-heavy pages
- **Example:** LinkedIn feed loading

**3. Toast Notifications**
- Temporary message, auto-dismiss
- Doesn't block interaction
- **Good for:** Non-critical confirmations
- **Example:** "Item added to cart"

**4. Empty States**
- Explain why it's empty
- Provide action to populate
- **Good for:** First use, zero results
- **Example:** Mailbox zero illustration with encouragement

### Onboarding Patterns

**1. Gradual Engagement**
- Let them use product before signup
- Ask for commitment when value is clear
- **Example:** Figma (edit file → prompted to save → sign up)

**2. Contextual Onboarding**
- Show tips when user reaches relevant feature
- Just-in-time learning
- **Example:** Slack (channel tips appear when you create first channel)

**3. Product Tour**
- Guide through key features
- Can be skipped
- **Warning:** Often ignored, use sparingly

**4. Preloaded Content**
- Show examples/templates instead of blank slate
- User deletes/modifies rather than starting from scratch
- **Example:** Notion (template gallery)

---

## Mobile vs Desktop Considerations

### Mobile-Specific Patterns

**Touch Targets:**
- Minimum 44x44pt (iOS) or 48x48dp (Android)
- More spacing between tappable elements
- Thumbs are imprecise compared to mouse

**Thumb Zones:**
- **Easy to reach:** Bottom third, sides
- **Harder to reach:** Top corners, top center
- Place primary actions in thumb zone

**Gestures:**
- **Swipe:** Navigate, dismiss, reveal actions
- **Pull to refresh:** Update content
- **Long press:** Contextual menus
- **Pinch to zoom:** Images, maps
- Don't rely solely on gestures (include visible alternatives)

**Reduced Screen Real Estate:**
- One thing at a time
- Prioritize ruthlessly
- Expand/collapse sections
- Bottom sheets for auxiliary content

**Interruptions:**
- Users are distracted, interrupted
- Save state automatically
- Quick resume from where they left off

### Desktop-Specific Patterns

**Hover States:**
- Reveal additional info on hover
- Tooltips for icons
- Preview on hover
- Not available on mobile!

**Keyboard Shortcuts:**
- Power users expect them
- Cmd/Ctrl + S to save
- Cmd/Ctrl + F to search
- Arrow keys to navigate
- Tab to move between fields

**Multi-Tasking:**
- Expect windows side-by-side
- Copy/paste between apps
- Drag and drop from other apps

**Cursor Precision:**
- Smaller targets acceptable
- More dense layouts possible
- Multi-select with shift/cmd

---

## Accessibility Guidelines

### WCAG Principles (Web Content Accessibility Guidelines)

**1. Perceivable**
- Text alternatives for images
- Captions for videos
- Color is not the only indicator
- Sufficient color contrast (4.5:1 for text)

**2. Operable**
- All functionality via keyboard
- No keyboard traps
- Enough time to read/interact
- No flashing content (seizure risk)

**3. Understandable**
- Readable text (clear language)
- Predictable behavior
- Input assistance (errors identified)
- Labels for form fields

**4. Robust**
- Works with assistive technologies
- Semantic HTML
- ARIA labels where needed

### Practical Accessibility Checklist

**Visual:**
- ✅ Color contrast ratios meet WCAG AA
- ✅ Don't rely on color alone ("red means error" also has icon)
- ✅ Text can be resized to 200% without breaking layout
- ✅ Images have alt text

**Motor:**
- ✅ All actions keyboard-accessible
- ✅ Touch targets minimum 44x44pt
- ✅ No fine motor control required
- ✅ Undo available for destructive actions

**Auditory:**
- ✅ Captions for video
- ✅ Transcripts for audio
- ✅ Visual alerts in addition to sound

**Cognitive:**
- ✅ Clear, simple language
- ✅ Consistent navigation
- ✅ Progress indicators for multi-step
- ✅ Avoid time limits (or make generous)

### Screen Readers

**How They Work:**
- Read content linearly (top to bottom)
- Rely on semantic HTML structure
- Use heading levels to navigate
- Announce role/state of elements

**Design Implications:**
- Logical reading order (even if visual layout differs)
- Meaningful heading structure (H1 → H2 → H3)
- Form labels associated with inputs
- Button text describes action ("Delete item" not just "Delete")
- Skip links to jump past navigation

---

## Testing & Validation

### Usability Testing Methods

**1. Moderated In-Person Testing**
- **Setup:** User performs tasks while thinking aloud, you observe
- **Participants:** 5-8 per persona
- **Duration:** 60 minutes per session
- **Good for:** Deep insights, follow-up questions, early-stage design

**Process:**
1. Welcome and explain (5 min)
2. Background questions (5 min)
3. Task scenarios (40 min)
4. Post-task questions (10 min)

**What to Ask:**
- "What do you think this page is for?"
- "What would you do next?"
- "What are you looking for?"
- Don't lead: "Does that make sense?" → "What do you think will happen?"

**2. Unmoderated Remote Testing**
- **Setup:** User completes tasks on their own, recorded
- **Participants:** 10-20
- **Duration:** 15-20 minutes
- **Good for:** Specific task testing, quick validation, larger sample size

**Tools:** UserTesting.com, Maze, Lookback

**3. First Click Testing**
- **Question:** "Where would you click to [do task]?"
- **Good for:** Navigation, information architecture
- **Fast:** Can test with dozens of people quickly

**4. 5-Second Test**
- **Setup:** Show screen for 5 seconds, then ask what they remember
- **Good for:** First impressions, visual hierarchy
- **Questions:** "What is this page for?" "What caught your attention?"

**5. A/B Testing**
- **Setup:** Show version A to 50%, version B to 50%
- **Measure:** Which performs better on key metric
- **Good for:** Optimizing existing flows, data-driven decisions
- **Warning:** Needs significant traffic, tests "what" not "why"

### What to Test

**Critical Flows:**
1. First time user experience (sign up → first value)
2. Core use case (most common task)
3. Error scenarios (what happens when things go wrong)

**Test Scenarios (Not Features):**
- ❌ "Sign up for account"
- ✅ "You heard about this from a friend. Explore and decide if it's worth signing up."

**Good Scenarios:**
- Provide context and motivation
- Don't give step-by-step instructions
- Match realistic situations
- Have clear success criteria

**Metrics to Track:**
- **Task success rate:** Did they complete it?
- **Time on task:** How long did it take?
- **Error rate:** How many mistakes?
- **Satisfaction:** How did they feel about it? (SUS score)

### Analyzing Results

**Patterns to Look For:**
- Where do multiple users get stuck?
- What do they look for but can't find?
- What do they click that doesn't work as expected?
- What language do they use (vs. what you call things)?
- What delights them?
- What frustrates them?

**Prioritizing Fixes:**
- **High impact, easy fix:** Do immediately
- **High impact, hard fix:** Plan for next sprint
- **Low impact, easy fix:** Consider (batch with other small changes)
- **Low impact, hard fix:** Probably skip

---

## Journey Mapping Anti-Patterns

### What NOT to Do

**1. Feature Lists Disguised as Journeys**
- ❌ "User clicks button → modal opens → user fills form"
- ✅ "User realizes they need to export data → looks for export → confused by format options → selects CSV based on familiarity"

**2. Happy Path Only**
- ❌ Mapping only when everything goes right
- ✅ Include errors, edge cases, confusion, abandonment

**3. Starting with Solutions**
- ❌ "We'll add a wizard to guide them"
- ✅ First understand the problem, then design solutions

**4. Ignoring Emotions**
- ❌ Just actions and screens
- ✅ Map feelings: frustration, confusion, delight, accomplishment

**5. Too Abstract or Too Specific**
- ❌ "User wants to be productive" (too vague)
- ❌ "User clicks Settings > Profile > Edit > Save" (too granular)
- ✅ "User needs to update their email address after changing jobs"

**6. Designing for Yourself**
- ❌ Assuming your technical knowledge/context
- ✅ Design for personas with different backgrounds/skills

**7. Skipping Research**
- ❌ Making up what users do
- ✅ Base on real user interviews, observations, data

---

## Additional Resources

### Books
- *Don't Make Me Think* by Steve Krug (usability fundamentals)
- *The Design of Everyday Things* by Don Norman (design principles)
- *Hooked* by Nir Eyal (habit formation)
- *100 Things Every Designer Needs to Know About People* by Susan Weinschenk

### Tools
- Journey mapping: Miro, Figma, Mural
- Prototyping: Figma, Framer, Principle
- Usability testing: UserTesting.com, Maze, Lookback
- Analytics: Mixpanel, Amplitude, Heap

### Patterns Libraries
- Nielsen Norman Group (research-backed patterns)
- UI Patterns (catalog of common solutions)
- Mobbin (mobile app patterns)
- Page Flows (user flow examples)

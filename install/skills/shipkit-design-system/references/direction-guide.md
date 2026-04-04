# Design Direction Guide

Framework for deriving aesthetic direction FROM project context rather than applying generic defaults. Inspired by Anthropic's frontend-design plugin approach — opinionated creative guidance — but grounded in the specific project.

---

## Step 0: Benchmark Research

**Before committing to any aesthetic choices, ground the direction in real-world evidence.**

1. Read `product-definition.json` for the key UX patterns the product uses (e.g., dashboard, onboarding wizard, search/filter, data table, checkout flow)
2. For each pattern, identify 2-3 products known for excellent implementations:
   - Use web search: "[pattern] best UX examples" or "[pattern] design inspiration"
   - Prefer products in the same domain or serving similar personas
   - Note what makes their design work — not just how it looks, but why the choices serve the user
3. Synthesize benchmark findings into the direction:
   - "For your dashboard pattern, Stripe uses dense but scannable cards with clear hierarchy — this works because their users are data-oriented"
   - "For your onboarding, Linear uses progressive disclosure with minimal screens — this works because their users are technical and impatient"
4. Let benchmarks inform each of the 6 dimensions below — typography, color, spacing decisions should reference what works in production, not abstract theory

**The goal is NOT to copy.** The goal is to make design choices informed by evidence of what works for similar patterns and audiences, then adapt to the specific project's vision and principles.

---

## The 6 Dimensions

Every design direction covers these 6 dimensions. Each is derived from upstream context, not chosen in isolation.

### 1. Aesthetic Tone

**Derived from:** why.json (vision, approach) + product-discovery.json (personas)

| Vision Keywords | Suggests |
|----------------|----------|
| Professional, enterprise, trust | Refined, structured, restrained palette |
| Creative, playful, young | Bold, asymmetric, saturated colors |
| Technical, developer, tools | Dense, monospace-friendly, dark-mode-first |
| Warm, personal, community | Organic, rounded, warm neutrals |
| Luxury, premium, exclusive | Minimal, high-contrast, serif typography |
| Educational, accessible, inclusive | Clear, high-contrast, generous spacing |

**Don't:** Pick "clean and modern" — that's the default Claude gives without guidance. Be specific.

### 2. Typography Direction

**Derived from:** aesthetic tone + persona accessibility needs + brand personality

| Tone | Heading Font Style | Body Font Style |
|------|-------------------|-----------------|
| Refined/luxury | Serif (editorial) | Clean sans-serif |
| Playful/creative | Display/decorative | Rounded sans-serif |
| Technical/developer | Monospace or geometric sans | System or clean sans |
| Warm/personal | Humanist sans-serif | Humanist sans-serif |
| Bold/startup | Heavy geometric sans | Light geometric sans |

**Rules:**
- Always pair a distinctive heading font with a readable body font
- Never default to Inter, Roboto, Arial, or system fonts for headings
- Body font can be more conservative — readability wins
- Check Google Fonts or Fontsource for free options that match the direction
- Minimum body text: 16px (1rem). Never smaller for primary content.

### 3. Color Philosophy

**Derived from:** brand identity + emotional targets from personas + accessibility

| Emotional Target | Color Strategy |
|-----------------|---------------|
| Trust & stability | Blue-anchored, conservative palette |
| Energy & action | Warm accents (orange, red), high saturation |
| Calm & wellness | Green/teal anchored, muted tones |
| Creativity & expression | Purple/magenta, diverse accent palette |
| Neutrality & professionalism | Monochrome + single strong accent |

**Rules:**
- One dominant brand color + one sharp accent outperforms evenly distributed palettes
- Semantic colors (error, success, warning, info) are functional — don't let brand override them
- Ensure WCAG AA contrast (4.5:1 for text, 3:1 for large text/UI) at minimum
- Define both light and dark mode tokens from the start, even if only shipping one initially

### 4. Spacing & Density

**Derived from:** product type + primary persona + platform

| Product Type | Density |
|-------------|---------|
| Consumer app (mobile-first) | Generous — large touch targets, breathing room |
| Data dashboard | Dense — information-rich, compact controls |
| Content/editorial | Balanced — wide reading column, generous margins |
| Developer tool | Dense — maximize code/data visibility |
| E-commerce | Mixed — generous hero, dense product grids |

**Base unit:** 4px (0.25rem) for most projects. Data-heavy UIs may use 2px or 8px.

### 5. Motion Principles

**Derived from:** UX patterns + interaction style + persona expectations

| UX Pattern | Motion Approach |
|-----------|----------------|
| Dashboard with real-time data | Subtle transitions, no blocking animations |
| Onboarding/wizard flow | Directional slides, progress reveals |
| Content browsing | Scroll-triggered reveals, parallax hints |
| Form-heavy workflow | Micro-feedback only (success checks, error shakes) |
| Marketing/landing | Orchestrated load sequence, scroll storytelling |

**Rules:**
- CSS-only animations for HTML projects; Motion/Framer Motion for React
- One well-orchestrated page load > scattered micro-interactions
- Respect `prefers-reduced-motion` — always provide a reduced/off fallback
- Animation duration: 150-300ms for micro, 300-500ms for transitions, 500-1000ms for reveals

### 6. Accessibility Stance

**Derived from:** personas + legal requirements + ethical position

| Persona Need | Minimum Standard |
|-------------|-----------------|
| General consumer | WCAG AA (4.5:1 contrast, keyboard nav) |
| Education/government | WCAG AA, ideally AAA for text |
| Users with disabilities identified in personas | WCAG AAA + specific accommodations |
| Developer/power user | Keyboard-first, screen reader support |

**Always include:**
- Focus indicators on all interactive elements
- Sufficient color contrast (don't rely on color alone)
- Semantic HTML structure
- alt text strategy (not just "add alt text" — define when to use decorative vs. descriptive)
- Touch target minimum: 44x44px on mobile

---

## Anti-Patterns (from Anthropic's frontend-design guidance)

**Never default to:**
- Inter, Roboto, Arial, or system fonts for display/heading use
- Purple gradients on white backgrounds (cliched AI aesthetic)
- Predictable centered-content layouts with no spatial tension
- Cookie-cutter component patterns with no context-specific character
- Space Grotesk (overused in AI/tech products)

**Instead:**
- Commit to a specific aesthetic and execute it with precision
- Bold maximalism and refined minimalism both work — the key is intentionality
- Every project should look different from the last
- Match implementation complexity to the vision — maximalist needs elaborate code, minimalist needs restraint

---

## DIRECTION.md Template

Every field below is **required**. No freeform prose — use the constrained values. Each dimension must cite its source field (the specific key from a `.shipkit/` artifact that drove the decision).

```markdown
# Design Direction — {Project Name}

**Generated by:** /shipkit-design-system
**Date:** YYYY-MM-DD
**Sources consulted:** [list every .shipkit/ file read, with the specific fields used]

## Aesthetic Tone
- **Classification:** [ONE of: refined, bold, technical, warm, minimal, editorial, playful, dense-professional]
- **Key adjectives (exactly 3):** [word], [word], [word]
- **This is NOT:** [what it explicitly avoids — at least 2 anti-descriptors]
- **Benchmark:** [named real product with similar tone + what makes it work]
- **Source:** [cite specific why.json field and persona that drove this choice]

## Typography
- **Heading font:** [exact font name from Google Fonts / Fontsource]
- **Heading weight:** [number: 400-900]
- **Why this heading font:** [one sentence connecting font traits to aesthetic tone]
- **Body font:** [exact font name]
- **Body weight:** [number: 400-900]
- **Minimum body size:** [px value, must be ≥16px]
- **Scale ratio:** [number, e.g. 1.25 (Major Third), 1.333 (Perfect Fourth)]
- **Source:** [cite persona accessibility needs + brand personality fields]

## Color Philosophy
- **Brand primary:** [exact hex value]
- **Brand accent:** [exact hex value]
- **Strategy:** [ONE of: monochrome+accent, analogous, complementary, triadic, split-complementary]
- **Emotional target:** [ONE of: trust, energy, calm, creativity, neutrality, authority, warmth]
- **Contrast standard:** [WCAG AA (4.5:1) or WCAG AAA (7:1)]
- **Dark mode:** [yes-from-start / planned / not-needed] — [rationale]
- **Source:** [cite brand identity fields + emotional targets from personas]

## Spacing & Density
- **Classification:** [ONE of: generous, balanced, dense, mixed]
- **Base unit:** [exact px value: 2, 4, or 8]
- **Comfortable touch target:** [exact px value, must be ≥44px on mobile]
- **Content width max:** [exact px or rem value]
- **Source:** [cite product type + primary persona]

## Motion
- **Classification:** [ONE of: orchestrated, subtle, micro-only, minimal, none]
- **Duration range:** [min]ms–[max]ms
- **Easing:** [exact CSS easing function, e.g. cubic-bezier(0.4, 0, 0.2, 1)]
- **Key moments (max 3):** [specific interaction → animation type]
- **Reduced motion fallback:** [instant / fade-only / off]
- **Library:** [CSS-only / Framer Motion / Motion One / none]
- **Source:** [cite UX patterns from product-definition]

## Accessibility
- **Standard:** [WCAG AA or WCAG AAA]
- **Focus indicator:** [exact style, e.g. "2px solid brand-primary, 2px offset"]
- **Color independence:** [how info is conveyed without color — icons, text, patterns]
- **Specific accommodations:** [from personas, or "none identified"]
- **Source:** [cite persona accessibility needs + legal/ethical requirements]
```

**Validation rule:** If any field contains vague language ("clean", "modern", "intuitive", "user-friendly", "seamless", "elegant") without a concrete specification alongside it, the output fails review. Every adjective must be backed by a measurable choice or a named reference.

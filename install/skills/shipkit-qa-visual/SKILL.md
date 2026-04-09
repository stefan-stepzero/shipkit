---
name: shipkit-qa-visual
description: "Visual QA using Playwright as a browser automation library. Two modes: --setup installs Playwright and creates ui-goals.json; default mode writes inline scripts to navigate, interact, screenshot, and report against goals."
argument-hint: "<what to test> or --setup"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
effort: medium
---

# shipkit-qa-visual

Visual QA for SaaS apps using Playwright as a lightweight browser automation library — not a test framework. Write an inline script, run it, screenshot meaningful states, read the screenshots, report against UI goals.

---

## Modes

Parse `$ARGUMENTS` to determine mode:

- **`--setup`** → Run the Setup flow (one-time per project)
- **Anything else** (or empty) → Run the Visual QA flow

---

## Setup Mode (`--setup`)

One-time project setup. Walk through each step, skip any that are already done.

### 1. Install Playwright

Check if playwright is in `package.json` devDependencies. If not:

```bash
npm install -D @playwright/test playwright
```

Then install Chromium (warn user about ~200MB download):

```bash
npx playwright install chromium
```

### 2. Create playwright.config.ts

Only if it doesn't exist at the project root. Detect the app's base URL first:

1. Check `$ARGUMENTS` for a URL
2. Probe common ports: `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000` (try 3000, 5173, 4321, 8080, 6847)
3. Check `package.json` scripts for port hints
4. Ask the user if none found

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  retries: 0,
  timeout: 120_000,
  expect: { timeout: 30_000 },
  use: {
    baseURL: '<detected-url>',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
```

### 3. Create directories

```bash
mkdir -p screenshots e2e
```

Add `screenshots/` to `.gitignore` if not already there.

### 4. Create UI Goals

This is the interactive step. The goals document grounds all future visual feedback.

**Scan the codebase for routes/pages:**
- Next.js: glob `app/**/page.{tsx,ts,jsx,js}` and `pages/**/*.{tsx,ts,jsx,js}` (exclude `_app`, `_document`, `api/`)
- React Router: grep for `<Route` or `createBrowserRouter`
- Other: grep for route definitions

**Propose goals to the user:**

For each detected page, propose what that page should accomplish and what to look for. Present a summary:

```
Proposed UI Goals

Base URL: http://localhost:3000
Pages detected: 3

/ (Landing)
  Goals: Clear value proposition above the fold, CTA visible and prominent
  Look for: No layout shift after hydration

/app (Main App)
  Goals: Input form clearly labeled, submit shows loading state, results render after completion
  Look for: Loading spinner on submit, error states show actionable messages

/settings (Settings)
  Goals: Current settings visible on load, changes save with confirmation
  Look for: Form preserves values on page refresh

Reply 'confirm' to write, or describe changes.
```

**Wait for user confirmation.** Do not write until confirmed.

Write to `.shipkit/ui-goals.json`:

```json
{
  "baseUrl": "http://localhost:3000",
  "pages": [
    {
      "path": "/",
      "name": "Landing",
      "goals": [
        "Clear value proposition above the fold",
        "CTA button visible and prominent"
      ],
      "lookFor": [
        "No layout shift after hydration"
      ]
    }
  ],
  "lastConfirmed": "2026-04-09T00:00:00Z",
  "lastTested": null
}
```

**Schema notes:**
- `pages[].goals` — What this page should accomplish. Plain language. These ground visual feedback.
- `pages[].lookFor` — Optional. Specific visual things to check — layout, contrast, loading states, error states. More tactical than goals.
- `lastConfirmed` — When user last reviewed and approved.
- `lastTested` — When screenshots were last taken and reviewed. Set to `null` until first run.

---

## Visual QA Flow (default)

This is the everyday mode. User describes what to test, Claude writes a script, runs it, reads the screenshots, reports.

### Step 1: Load context

1. Read `.shipkit/ui-goals.json` — these goals ground your visual feedback
2. Read `playwright.config.ts` for `baseURL`
3. If neither exists, tell the user to run `/shipkit-qa-visual --setup` first

If goals exist, show a one-line summary:
```
Goals loaded: 3 pages, last confirmed 2026-04-09
```

### Step 2: Write the script

Based on what the user asked for (or if no description given, pick goals that haven't been visually verified recently), write an inline Node script.

**Script template — every script must follow this pattern:**

```javascript
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1280, height: 900 });

  // Console capture — always include this
  const logs = [];
  page.on('console', msg => logs.push(`[${msg.type()}] ${msg.text()}`));
  page.on('pageerror', err => logs.push(`[ERROR] ${err.message}`));

  // --- Navigation and interaction go here ---

  await page.goto('http://localhost:3000/app');
  await page.waitForTimeout(3000);
  await page.screenshot({ path: 'screenshots/app-initial.png', fullPage: true });

  // Interact
  await page.locator('[data-testid="problem-input"]').fill('Some input');
  await page.locator('[data-testid="submit-btn"]').click();
  await page.waitForTimeout(1000);
  await page.screenshot({ path: 'screenshots/app-loading.png', fullPage: true });

  // Wait for async result
  await page.locator('[data-testid="results-panel"]').waitFor({ timeout: 60000 });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'screenshots/app-results.png', fullPage: true });

  // --- End of interaction ---

  // Write console log — always include this
  fs.writeFileSync('screenshots/console.log', logs.join('\n'));

  await browser.close();
})();
```

Write the script to `screenshots/qa-script.mjs` (overwritten each run).

**Conventions — follow these exactly:**

| Rule | Detail |
|------|--------|
| Selectors | `data-testid` ONLY: `page.locator('[data-testid="..."]')`. Never CSS selectors, never text matching, never ARIA roles. If an element lacks a data-testid, tell the user to add one. |
| Viewport | `page.setViewportSize({ width: 1280, height: 900 })` — every script |
| Screenshots | `fullPage: true` always. Descriptive filenames: `screenshots/{page}-{state}.png`. Overwrite previous. |
| Timeouts | `page.waitForTimeout(1000-5000)` for animations/hydration. `element.waitFor({ timeout: 60000 })` for real API calls. Never rely on default timeouts. |
| Console | Always capture with `page.on('console')` and `page.on('pageerror')`. Write to `screenshots/console.log`. |
| No test framework | Never use `test()`, `expect()`, `describe()`. This is Playwright as a library, not a test runner. |

### Step 3: Run the script

```bash
node screenshots/qa-script.mjs
```

If it fails, read the error. Common issues:
- **Element not found** → the `data-testid` doesn't exist. Tell the user which testid is missing.
- **Navigation error** → wrong URL or app not running. Check the base URL.
- **Timeout** → the element never appeared. May be a real bug — screenshot what's visible and report.

Attempt one fix if the error is a simple selector/timing issue. If it fails again, report with whatever screenshots were captured.

### Step 4: Read and report

1. **Read each screenshot** captured during the run (use the Read tool on the image files)
2. **Read `screenshots/console.log`** for errors, warnings, failed fetches
3. **Compare against `ui-goals.json`** — for each relevant page's goals and lookFor items, assess whether the screenshot shows the goal being met

**Report format:**

```
## Visual QA Report

Base URL: http://localhost:3000
Pages checked: /app

### /app — Main App

Screenshots: app-initial.png, app-loading.png, app-results.png

**Goals:**
- Input form clearly labeled — YES, form labels visible in initial screenshot
- Submit shows loading state — YES, spinner visible in loading screenshot
- Results render after completion — YES, results panel populated in results screenshot

**Look for:**
- Loading spinner on submit — visible, good
- Error states show actionable messages — not tested this run (happy path only)

**Console:** 2 warnings (React hydration), 0 errors. No failed fetches.

**Issues:** None found.
```

4. **Update `lastTested`** in `ui-goals.json` to current ISO timestamp

### Step 5: Iterate

After reporting, the user may ask for changes:
- "The button looks wrong" → adjust script or flag for the developer
- "Also check the error state" → write a new script variant, run again
- "Add testids to the settings page" → tell the user which testids to add

This is a conversation, not a one-shot report. Stay in the loop until the user is satisfied.

---

## Context Files

| Reads | Purpose |
|-------|---------|
| `.shipkit/ui-goals.json` | Goals that ground visual feedback |
| `playwright.config.ts` | Base URL and config |
| `package.json` | Dependency check during setup |

| Writes | When |
|--------|------|
| `.shipkit/ui-goals.json` | Created on setup; `lastTested` updated each run |
| `screenshots/*.png` | Captured during runs (gitignored, overwritten) |
| `screenshots/console.log` | Console output from each run (overwritten) |
| `screenshots/qa-script.mjs` | The inline script (overwritten each run) |
| `playwright.config.ts` | Created on setup if missing |

---

## Integration

| Skill | How |
|-------|-----|
| `shipkit-review-shipping` | Can reference visual QA as an optional verification step |

---

<!-- SECTION:after-completion -->
## After Completion

Visual QA screenshots and console output are in `screenshots/`. The report maps findings back to the goals in `ui-goals.json`.

- **Everything looks good** → continue development or run `/shipkit-preflight`
- **Issues found** → fix the UI, then re-run `/shipkit-qa-visual` to verify
- **Goals stale** → edit `.shipkit/ui-goals.json` directly to update what matters
- **Missing testids** → add `data-testid` attributes to interactive elements, then re-run
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Playwright installed and Chromium available (setup mode)
- [ ] `playwright.config.ts` exists at project root
- [ ] `.shipkit/ui-goals.json` exists with user-confirmed goals
- [ ] Screenshots captured to `screenshots/` using fullPage and consistent viewport
- [ ] All selectors use `data-testid` — no CSS selectors, text matching, or ARIA roles
- [ ] Console errors captured to `screenshots/console.log`
- [ ] Report maps visual findings back to goals in `ui-goals.json`
- [ ] `lastTested` updated in `ui-goals.json` after each run
- [ ] User can iterate — adjust, re-run, re-check — within the same conversation
<!-- /SECTION:success-criteria -->

# Mission Control Dashboard — User Stories & Implementation Status

## Information Architecture

The dashboard serves two distinct contexts with different information needs:

```
Portfolio View (landing)          Project Detail (drill-in)
┌────────────────────────┐       ┌─────────────────────────────────┐
│                        │       │ ← Back to Portfolio             │
│  [Proj A] [Proj B] ... │ click │                                 │
│                        │ ───── │  Overview │ Artifacts │ Activity │
│  scan → decide → click │   →   │                                 │
│                        │       │  [selected tab content]         │
└────────────────────────┘       └─────────────────────────────────┘
```

**Routing:** Hash-based (`#/` = portfolio, `#/project/{encodedPath}` = detail). Bookmarkable.

**Rule:** If only one project exists, skip portfolio and auto-redirect to project detail.

---

## Context A: Portfolio View

The portfolio view answers one question: **"Where should I focus?"**

The developer glances at project cards for 5 seconds and clicks into one. This view is a router, not a destination.

### PA-1: See project health at a glance [DONE]

> As a developer managing multiple projects, I want to see each project as a card showing: active session count, artifact count, and a freshness indicator — so I can spot which projects need attention without clicking into each one.

**Acceptance criteria:**
- [x] Each project is a card with: name, path, session count (active/standby/stopped), artifact count, last activity timestamp
- [x] Freshness indicator: green (activity < 1h), amber (< 24h), red (> 24h), grey (no sessions)
- [x] Cards sorted by most recent activity

**Implementation:** `PortfolioView.tsx` → `ProjectCard` with `getFreshness()` helper

### PA-2: See what's missing across projects [DONE]

> As a developer, I want to see which projects are missing foundational artifacts (goals, spec, plan, preflight, architecture) — so I can identify under-specified projects before they drift.

**Acceptance criteria:**
- [x] Each project card shows artifact coverage as small dots for the 5 foundational types
- [x] Missing foundational artifacts shown with dim/empty styling
- [x] Exists vs missing distinguished visually (`.coverage-item.exists` / `.coverage-item.missing`)

**Implementation:** `PortfolioView.tsx` → artifact coverage row using `FOUNDATIONAL_ARTIFACTS` from `types.ts`

### PA-3: See stale artifacts across portfolio [DONE]

> As a developer, I want to see which projects have artifacts that haven't been refreshed recently — so I can spot drift before it becomes a problem.

**Acceptance criteria:**
- [x] Freshness indicator on each project card (green/amber/red based on `lastActivity` timestamp)
- [x] Visual distinction between "no artifacts" and "stale artifacts"

**Implementation:** `PortfolioView.tsx` → `getFreshness()` computes color + label from `lastActivity`

### PA-4: Quick-launch into a project [DONE]

> As a developer, I want to click a project card and immediately see its full detail view — so context-switching is instant.

**Acceptance criteria:**
- [x] Single click navigates to project detail
- [x] Back button returns to portfolio without losing state
- [x] URL updates for bookmarking (`#/project/{encodedPath}`)
- [x] Keyboard accessible (Enter/Space on cards)

**Implementation:** `App.tsx` → `navigate()` + hash routing; `PortfolioView.tsx` → `role="button"` + `tabIndex={0}` + keyboard handlers

---

## Context B: Project Detail View

Once inside a project, the developer wants depth. This view has 3 tabs: Overview, Artifacts, Activity. Commands accessible from header button.

### Overview Tab

#### PB-1: See current project state [DONE]

> As a developer focused on one project, I want to see a summary of: active sessions, artifact coverage, recent skill activity, and top recommendations — so I have a complete picture on one screen.

**Acceptance criteria:**
- [x] Stats row: active sessions, artifact count, skills used, total events
- [x] Artifact coverage grid: all 17 artifact types with icon + exists/missing status
- [x] Foundational artifacts visually highlighted
- [x] Top 3 recommendations from recommendation engine
- [x] Recent activity feed (last 8 events)

**Implementation:** `ProjectOverview.tsx` — stats row + coverage grid + recommendations + activity feed

#### PB-2: See what's been done and what's missing [DONE]

> As a developer, I want to see which skills have been run, when they were last run, and which recommended skills haven't been run yet — so I know workflow gaps.

**Acceptance criteria:**
- [x] Skill usage list sorted by most-used
- [x] Each skill shows: name, run count badge, last used timestamp
- [x] Visual distinction between used and unused skills

**Implementation:** `ProjectOverview.tsx` → skill usage section from `codebase.skills`

#### PB-3: Get context-aware next-step recommendations [DONE]

> As a developer, I want the dashboard to suggest what to run next based on what's done, what's stale, and what's missing — so the dashboard guides my workflow instead of me having to remember it.

**Acceptance criteria:**
- [x] Recommendations ranked by priority (high/medium/low) with color-coded dots
- [x] Each recommendation has: message explaining why, one-click "Send" button
- [x] Recommendations sourced from: SKILL_KNOWLEDGE staleness, missing foundational skills, follow-up suggestions
- [x] Send button calls `sendCommand()` to active session

**Implementation:** `ProjectOverview.tsx` → recommendation cards with `sendCommand()` integration; server generates recommendations in `generateRecommendations()`

### Artifacts Tab

#### PB-4: Browse all project artifacts [DONE]

> As a developer, I want to see all .shipkit/*.json artifacts for this project as cards — so I can quickly find and inspect any artifact.

**Acceptance criteria:**
- [x] Artifact cards showing: type icon, filename, version, last updated, summary preview
- [x] Cards indicate rendering capability: "graph" badge, "view" badge, or JSON-only
- [x] Sorted by last updated (most recent first)
- [x] Stale indicator on artifacts older than 7 days

**Implementation:** `ArtifactsView.tsx` → `getSortedArtifacts()` + `isStale()` + badge system; icons from `ARTIFACT_TYPE_ICONS`

#### PB-5: View artifact with type-appropriate rendering [DONE]

> As a developer, I want each artifact rendered meaningfully — goals as a prioritized list, preflight as a readiness checklist, architecture as a node graph — so I get value without reading raw JSON.

**Acceptance criteria:**
- [x] 3 artifact types render as interactive graphs (architecture, data-contracts, product-discovery) via React Flow
- [x] 14 artifact types have structured renderers (goals, preflight, project-status, plan, spec, test-coverage, work-memory, scale-readiness, bug-spec, prompt-audit, ux-decisions, user-tasks, project-why, codebase-index)
- [x] All types have JSON fallback view
- [x] Toggle between structured/graph view and raw JSON

**Implementation:** `ArtifactRenderers.tsx` (14 renderers + `ArtifactStructuredView` router) + `ArtifactGraph.tsx` (React Flow) + `ArtifactsView.tsx` detail view with toggle

#### PB-6: Know if artifacts are fresh or stale [DONE]

> As a developer, I want to see when each artifact was last updated and its version — so I know if I'm looking at current data or something outdated.

**Acceptance criteria:**
- [x] Last updated timestamp on each artifact card
- [x] Version number displayed
- [x] Stale badge on artifacts older than 7 days
- [x] "Source" field shows which skill produced the artifact

**Implementation:** `ArtifactsView.tsx` → `isStale()` + `.badge-stale` + meta row (version, date, source)

### Activity Tab

#### PB-7: See what Claude has been doing [DONE]

> As a developer, I want to see a timeline of recent tool uses and skill invocations for this project — so I can track progress without reading terminal scroll.

**Acceptance criteria:**
- [x] Chronological event list (most recent first)
- [x] Each event shows: tool icon, tool name, skill name (if applicable), relative timestamp
- [x] Filter by event type ("All Events" / "Skills Only" toggle)
- [x] Session grouping (events grouped by session ID with session status badge)

**Implementation:** `ProjectActivity.tsx` → events grouped by sessionId, filter toggle, `TOOL_ICONS` map

#### PB-8: Know if the session is alive [DONE]

> As a developer, I want to see the session's last heartbeat and current status — so I know if it's active, idle in standby, or dead.

**Acceptance criteria:**
- [x] Session status badge: active (green), standby (amber), stopped (grey), stale (red)
- [x] Last seen timestamp with relative time
- [x] Standby mode clearly indicated

**Implementation:** `ProjectDetail.tsx` header badge + `ProjectActivity.tsx` session group headers with status dots

### Commands

#### PB-9: Send a skill command [DONE]

> As a developer, I want to pick a skill from a categorized list and send it to the active session — so I can trigger work without switching terminals.

**Acceptance criteria:**
- [x] All 37 skills available, organized in 7 categories (Discovery, Planning, Knowledge, Execution, Quality, Communication, System)
- [x] Single click selects skill, double-click sends immediately
- [x] Optional free-text context/arguments field
- [x] Ctrl+Enter keyboard shortcut to send
- [x] Disabled state when no active session

**Implementation:** `CommandPanel.tsx` → `SKILL_CATEGORIES` (37 skills), chip selection, double-click quick-send, textarea, Ctrl+Enter

#### PB-10: See command queue status [DONE]

> As a developer, I want to see pending, in-flight, and processed commands — so I know what's queued and what's been picked up.

**Acceptance criteria:**
- [x] Queue status visible: pending count, in-flight count, processed count
- [x] Each queued command shows: prompt text, timestamp, status
- [x] Visual confirmation when command is queued
- [x] Auto-dismiss confirmation after 3 seconds

**Implementation:** `CommandPanel.tsx` → `fetchQueue()` polling, queue stat badges, sent confirmation with auto-dismiss

---

## Technical Architecture

### File Inventory (8 active components + 4 foundation)

| File | Purpose | Lines |
|------|---------|-------|
| `App.tsx` | Layout shell, hash router, data fetching | ~120 |
| `App.css` | Complete design system (mobile-first, 31 sections) | ~1000 |
| `types.ts` | All TypeScript types + artifact constants | ~150 |
| `api.ts` | Server API calls (8 endpoints) | ~55 |
| `hooks/useApi.ts` | Auto-refreshing data hook (3s interval) | ~50 |
| `PortfolioView.tsx` | Landing page with project cards | ~120 |
| `ProjectDetail.tsx` | Drill-in shell with tabs + command trigger | ~80 |
| `ProjectOverview.tsx` | Overview tab (stats, coverage, recommendations, activity, skills) | ~200 |
| `ProjectActivity.tsx` | Activity tab (timeline, filters, session groups) | ~150 |
| `ArtifactsView.tsx` | Artifacts tab (cards, detail, stale indicators) | ~250 |
| `CommandPanel.tsx` | Command modal (37 skills, 7 categories, queue) | ~270 |
| `ArtifactRenderers.tsx` | 14 structured artifact renderers | ~650 |
| `ArtifactGraph.tsx` | React Flow graph renderers (3 types) | ~200 |
| `main.tsx` | Vite entry point | ~10 |

### Design System

- **Theme:** Dark, professional (Linear/Vercel inspired). Zinc palette.
- **Typography:** Inter (primary), JetBrains Mono (code/timestamps)
- **Mobile-first:** Base styles are mobile; `@media (min-width)` for sm/md/lg/xl
- **Breakpoints:** 640px (sm), 768px (md), 1024px (lg), 1280px (xl)
- **Touch:** 44px minimum touch targets on `pointer: coarse` devices
- **Colors:** `--bg-base` #09090b, `--bg-surface` #18181b, `--accent-blue` #3b82f6, `--accent-green` #22c55e, `--accent-amber` #f59e0b, `--accent-red` #ef4444

### Server (Node.js, no dependencies)

- **Port:** 7777
- **Version:** 1.1.0
- **SKILL_KNOWLEDGE:** 23 skill entries with relationship data
- **Artifact validation:** Warns on missing type/version/summary
- **Command queue:** File-based inbox per session
- **Persistence:** Codebases to disk, events to append-only log
- **Tests:** 47/47 integration tests passing

### Reporter Hook (Python)

- **Artifact collection:** `rglob("*.json")` — recursive, includes subdirectories
- **Artifact keys:** Relative paths from `.shipkit/` (e.g., `specs/active/login-spec.json`)
- **Convention:** Only ships files with `$schema: "shipkit-artifact"`
- **Sync cache:** Tracks last sync time to avoid redundant sends

---

## Remaining Polish (Future)

These are refinements, not blockers. The dashboard is functional for all 10 user stories.

### UX Refinements
- [ ] Loading skeletons instead of empty states during initial data fetch
- [ ] Animated transitions between portfolio and project views
- [ ] Keyboard navigation between project cards (arrow keys)
- [ ] Search/filter in portfolio view (when > 5 projects)
- [ ] Artifact diff view (compare versions)

### Server Enhancements
- [ ] Server-side event filtering by project (avoid client-side filter for large event sets)
- [ ] WebSocket for real-time updates (replace polling)
- [ ] Artifact history (track previous versions)
- [ ] Dashboard authentication (currently open on localhost)

### Mobile Polish
- [ ] Test on actual mobile devices (currently CSS-only responsive)
- [ ] Pull-to-refresh gesture
- [ ] Bottom sheet for command panel on mobile (currently full-screen modal)
- [ ] Swipe between project detail tabs

### Observability
- [ ] Error boundary components (prevent white screen on render errors)
- [ ] Dashboard health endpoint (frontend build hash, bundle size)
- [ ] Analytics: track which skills are sent most from dashboard

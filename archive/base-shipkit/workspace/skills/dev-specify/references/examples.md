# Feature Specification Examples

Two complete specification examples showing good specs at different complexity levels.

---

## Example 1: Simple Feature - Dark Mode Toggle

```markdown
# Feature Specification: Dark Mode Toggle

**Created:** 2025-01-15
**Last Updated:** 2025-01-15
**Status:** Draft

---

## Overview

**Problem:**
80% of users access app at night (per analytics). User story #12: "As a night-time user,
I want dark mode, so my eyes don't hurt." Currently app is light-only, causing eye strain
and battery drain on OLED devices.

**Solution:**
Add dark mode toggle in settings. Persist preference. Apply dark theme throughout app.

**Value:**
- User: Reduced eye strain, better battery life
- Business: Higher engagement at night (improve 35% night bounce rate)

---

## User Stories

**Primary User Story:**
```
As a night-time user
I want to enable dark mode
So that the app doesn't hurt my eyes in low light

Acceptance Criteria:
- Toggle exists in settings
- Dark theme applies immediately
- Preference persists across sessions
- All screens support dark mode
```

**Related User Stories:**
- User story #4: Accessibility (high contrast modes)

---

## Scope

**In Scope:**
- Dark mode toggle in settings
- Dark theme for all screens
- Preference persistence
- Smooth theme switching

**Out of Scope:**
- Auto dark mode (sunset/sunrise detection) - future
- Custom theme colors - future
- Per-screen theme override - not needed

---

## User Experience

### User Journey
(Extracted from prod-interaction-design: Settings Journey)

1. User opens Settings
2. User sees "Appearance" section
3. User taps Dark Mode toggle
4. Theme switches immediately (no reload)
5. User navigates app - all screens are dark

### Key Interactions
1. User taps toggle → Theme switches with 200ms fade transition
2. User closes app → Preference saved
3. User reopens app → Dark mode still active

### UI Requirements
- Toggle component: Material Design switch (per brand guidelines)
- Dark theme colors: Use brand dark palette (charcoal #1E1E1E, accent blue #4A90E2)
- Icons: Invert for dark mode (per brand: "Icons must be visible on both themes")
- Responsive: All device sizes (mobile, tablet)

---

## Functional Requirements

### Core Functionality

1. **Dark Mode Toggle**
   - Description: Switch in Settings > Appearance
   - Acceptance:
     - Given: User is in Settings
     - When: User taps Dark Mode toggle
     - Then: Theme switches within 200ms, toggle reflects state

2. **Theme Application**
   - Description: Apply dark theme to all app screens
   - Acceptance:
     - Given: Dark mode is enabled
     - When: User navigates to any screen
     - Then: Screen uses dark theme colors

3. **Preference Persistence**
   - Description: Remember user's theme choice
   - Acceptance:
     - Given: User enabled dark mode
     - When: User closes and reopens app
     - Then: Dark mode is still active

### Business Rules
- Default: Light mode (don't assume dark preference)
- Theme applies globally (not per-screen)
- Transition is animated (not jarring instant switch)

### Validation Rules
- Toggle state must match theme (no mismatches)
- Theme must load before first screen render (no flash)

---

## Non-Functional Requirements

### Performance
- Theme switch: <200ms (per constitution UX targets)
- App launch: No delay due to theme loading (<100ms overhead)

### Security
- None specific (preference is not sensitive data)

### Reliability
- Theme must apply on 100% of screens (no forgotten screens)
- Preference must persist reliably (local storage)

### Accessibility
- High contrast in both modes (WCAG AA minimum, per brand guidelines)
- Screen reader announces theme change
- Toggle is keyboard accessible

---

## Technical Constraints

(From dev-constitution)
- React Native: Use React Context for theme
- State management: Redux for user preferences
- Testing: Jest + React Testing Library, 80% coverage
- Performance: <60ms component re-render

---

## Dependencies

### External Dependencies
- None

### Internal Dependencies
- Brand design system (dark color palette must be defined)
- Settings screen (already exists)

---

## Data Requirements

### Data Models (High-Level)
- UserPreferences: { theme: 'light' | 'dark' }

### Data Flow
User toggles → Redux action → AsyncStorage → Context update → Components re-render

---

## Edge Cases & Error Handling

### Edge Cases
1. First launch (no preference set): Default to light mode
2. Invalid preference value in storage: Default to light mode, log error
3. Mid-theme-switch navigation: Complete animation before allowing navigation

### Error States
- Storage write fails: Show toast "Couldn't save preference", retry on next toggle
- Theme colors missing: Fall back to default colors, log error

---

## Success Criteria

**Done When:**
- [ ] Dark mode toggle exists in Settings
- [ ] All screens support dark theme
- [ ] Preference persists across app restarts
- [ ] Theme switches in <200ms
- [ ] Tests pass (80% coverage)
- [ ] Accessibility audit passes (WCAG AA)

**Metrics:**
- Night bounce rate: Reduce from 35% to <25%
- Dark mode adoption: Track % of users enabling it (target >40%)

---

## Open Questions

None - spec is complete.

---

## Notes

- Design team confirmed dark color palette in brand guidelines
- QA will test on OLED devices (battery impact)
- Future: Auto dark mode based on time (not this iteration)
```

---

## Example 2: Complex Feature - Collaborative Document Editing

```markdown
# Feature Specification: Real-Time Collaborative Editing

**Created:** 2025-01-15
**Last Updated:** 2025-01-15
**Status:** Draft

---

## Overview

**Problem:**
Teams currently email documents back and forth (from user interviews), losing track of versions
and creating merge conflicts. User story #3: "As a team member, I want to edit documents with
my team in real-time, so we don't create conflicting versions."

40% of support tickets are about merge conflicts and lost changes.

**Solution:**
Real-time collaborative editing with presence indicators, conflict-free sync (CRDT), and
version history.

**Value:**
- User: No more merge conflicts, see teammates' changes instantly
- Business: Reduce support tickets 40%, increase team plan conversions (collaboration is #1 requested feature)

---

## User Stories

**Primary User Story:**
```
As a team member
I want to edit documents with my team in real-time
So that we don't create conflicting versions

Acceptance Criteria:
- See who else is editing
- See their changes as they type
- Changes never conflict
- Can see document history
- Works offline (syncs when reconnected)
```

**Related User Stories:**
- User story #7: Offline editing
- User story #12: Version history and rollback

---

## Scope

**In Scope:**
- Real-time text editing (multiple cursors)
- Presence indicators (who's online, where they're editing)
- Conflict-free sync (operational transformation or CRDT)
- Connection status indicator
- Basic version history (auto-save snapshots)

**Out of Scope:**
- Rich media collaboration (images, embeds) - future
- Video/voice chat - not needed (users use Zoom)
- Commenting/suggestions (Google Docs style) - future
- Fine-grained version diff - future (just snapshots for now)

---

## User Experience

### User Journey
(Extracted from prod-interaction-design: Document Editing Journey)

1. User opens document
2. System shows who else is viewing/editing (presence)
3. User starts typing
4. Other users see changes in real-time (<500ms)
5. User's cursor position visible to others
6. Connection drops → indicator shows "Offline", edits queue
7. Connection restores → queued edits sync automatically
8. No conflicts, ever

### Key Interactions
1. User types → Text appears for all users <500ms
2. User moves cursor → Other users see cursor position
3. Network drops → Yellow "Offline" indicator, editing continues
4. Network restores → Green "Online", auto-sync, no user action needed
5. User clicks version history → Sidebar shows snapshots (every 5min)

### UI Requirements
- Presence indicators: Avatar circles (top-right), colored cursors (per brand: use team colors)
- Connection status: Subtle dot (green/yellow/red), per brand's status component
- Cursors: Colored by user, with name label (Figma style, per interaction design)
- Version history: Sidebar panel (Material Design, per brand)
- Responsive: Desktop primary (mobile is read-only for MVP)

---

## Functional Requirements

### Core Functionality

1. **Real-Time Text Sync**
   - Description: Synchronize text edits across users in real-time
   - Acceptance:
     - Given: 2+ users editing same document
     - When: User types text
     - Then: Other users see text within 500ms

2. **Conflict-Free Editing**
   - Description: Concurrent edits never conflict
   - Acceptance:
     - Given: 2 users editing same paragraph
     - When: Both type simultaneously
     - Then: Both edits merge correctly (no conflicts, no data loss)

3. **Presence Indicators**
   - Description: Show who's viewing/editing
   - Acceptance:
     - Given: User opens document
     - When: Document loads
     - Then: User sees list of others (name, avatar, online status)

4. **Cursor Positions**
   - Description: Show where others are editing
   - Acceptance:
     - Given: User is editing
     - When: Another user moves cursor
     - Then: First user sees colored cursor with name label

5. **Offline Editing**
   - Description: Edit while offline, sync when online
   - Acceptance:
     - Given: User is editing and loses connection
     - When: User continues editing
     - Then: Edits queue locally, sync on reconnection (no data loss)

6. **Auto-Save Snapshots**
   - Description: Automatically save version history
   - Acceptance:
     - Given: Document is being edited
     - When: 5 minutes pass
     - Then: Snapshot is saved to version history

### Business Rules
- Text sync uses CRDT (from architecture decision: Yjs library)
- Max 10 simultaneous editors per document (per performance targets)
- Snapshots kept for 30 days (per data retention policy)
- Offline edits queue max 100 operations (then warn user)

### Validation Rules
- Document ID must be valid (authorized access)
- User must be authenticated (JWT)
- Edits must pass CRDT validation (no invalid operations)

---

## Non-Functional Requirements

### Performance
- Text sync latency: <500ms p95 (per success metrics)
- Cursor update: <200ms (per constitution UX targets)
- Max concurrent users: 10 per document
- Snapshot creation: <1s (background, non-blocking)

### Security
- Document access: Check permissions on every operation (not just on load)
- WebSocket auth: Validate JWT on connect and every 15min
- Prevent unauthorized edits: Server validates all operations

### Reliability
- 99.5% uptime (per success metrics SLA)
- Offline queue: Survives app close/reopen
- Sync retries: Exponential backoff (2s, 4s, 8s, max 3 attempts)
- Conflict resolution: Guaranteed convergence (CRDT property)

### Accessibility
- Screen reader: Announce when others join/leave
- Keyboard shortcuts: Navigate version history
- High contrast: Cursors visible in both light/dark mode

---

## Technical Constraints

(From dev-constitution)
- WebSockets for real-time (not polling)
- Yjs for CRDT (proven library, team expertise)
- React for UI (cursor overlays)
- PostgreSQL for snapshots (existing DB)
- Redis for presence (fast ephemeral data)

---

## Dependencies

### External Dependencies
- Yjs library: CRDT implementation
- WebSocket server: Real-time infrastructure
- Redis: Presence and cursor positions (ephemeral)

### Internal Dependencies
- Auth system: Must provide JWT for WebSocket auth
- Document model: Must support version snapshots
- Offline storage: LocalStorage or IndexedDB for queued edits

---

## Data Requirements

### Data Models (High-Level)
- Document: { id, content (Yjs state), snapshots[] }
- Snapshot: { id, documentId, content, timestamp, authorId }
- Presence: { userId, documentId, cursorPosition, online, lastSeen }

### Data Flow
User edits → Yjs CRDT → WebSocket → Server → Broadcast to others → Yjs merge → UI update
Offline: User edits → Yjs CRDT → Local queue → (reconnect) → WebSocket → Server → Sync

---

## Edge Cases & Error Handling

### Edge Cases
1. **User joins mid-edit:** Sync full document state, then start receiving deltas
2. **10th user tries to join:** Show "Document full (max 10 editors). Retry?" with read-only mode
3. **Massive paste (100K chars):** Chunk operations, show progress, warn if exceeds limit
4. **Rapid connect/disconnect:** Debounce presence updates (1s) to avoid flicker
5. **Snapshot during heavy editing:** Snapshot background thread, don't block typing

### Error States
- WebSocket disconnect: Yellow "Reconnecting..." indicator, auto-retry
- Sync failure after 3 retries: Red "Offline - changes saved locally", manual retry button
- Invalid operation from server: Log error, discard operation, don't crash
- Snapshot save fails: Retry in 1min, log error, don't block editing

---

## Success Criteria

**Done When:**
- [ ] 2+ users can edit same document simultaneously
- [ ] Concurrent edits merge without conflicts (tested with 10 users)
- [ ] Changes appear <500ms (verified with network throttling)
- [ ] Offline editing works (tested in airplane mode)
- [ ] Presence and cursors update in real-time
- [ ] Version snapshots saved every 5min
- [ ] Tests pass (80% coverage, including conflict scenarios)
- [ ] Load test: 10 concurrent editors, no performance degradation

**Metrics:**
- Merge conflict support tickets: Reduce from 40% to <5%
- Team plan conversions: Increase 20% (collaboration is conversion driver)
- Sync success rate: >99.5%
- Latency p95: <500ms

---

## Open Questions

[NEEDS_CLARIFICATION: Should read-only viewers count toward 10-user limit?]
[NEEDS_CLARIFICATION: How to handle user who's been offline for 2 days? Force conflict resolution or auto-merge?]

---

## Notes

- Yjs chosen over Operational Transform (simpler, better offline support)
- Max 10 users based on load testing (WebSocket broadcast overhead)
- Version history UX to be finalized with design team (just technical capability in scope)
- Mobile collaborative editing deferred (read-only for now)
```

---

## Key Differences by Complexity

| Aspect | Simple (Dark Mode) | Complex (Collab Edit) |
|--------|-------------------|----------------------|
| **Length** | ~600 words | ~1200 words |
| **User Stories** | 1 primary | 1 primary + 2 related |
| **Dependencies** | None external | 3 external libs |
| **Edge Cases** | 3 | 5 |
| **Performance Reqs** | 2 simple | 4 detailed |
| **Data Models** | 1 simple | 3 complex |
| **Scope Risk** | Low (well-defined) | Medium (real-time is complex) |
| **Clarifications** | 0 | 2 |

---

## Anti-Example: Bad Spec

```markdown
# Feature Specification: User Authentication

## Overview
We need authentication.

## Requirements
- Users can log in
- Passwords should be secure
- Remember me checkbox
- Forgot password

## Success
It works.
```

**Why terrible:**
- ❌ No problem statement (why do users need auth?)
- ❌ Not grounded in user stories
- ❌ Vague requirements ("secure" how? "works" how?)
- ❌ No acceptance criteria (not testable)
- ❌ Missing: UI details, error handling, edge cases, performance, security specifics
- ❌ No technical constraints
- ❌ No success metrics
- ❌ Unmeasurable "success" criteria

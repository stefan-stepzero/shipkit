# Common Scenarios

## Scenario 1: Feature Just Completed

```
User: "Log what we did today"

Claude:
1. Ask: "What did we accomplish?"
   User: "Built the recipe sharing feature"
2. Ask: "Any blockers?"
   User: "None, it's shipped"
3. Ask: "What's next?"
   User: "Add analytics tracking"
4. Read .shipkit-lite/progress.md
5. Append session:
   ## [2025-01-15] | Recipe Sharing Feature
   **Completed**: Recipe sharing feature
   **Files**: ShareButton.tsx, share/[token]/page.tsx, api/share/route.ts
   **Status**: ✓ Shipped
   **Next Steps**: Add analytics tracking
```

---

## Scenario 2: Work In Progress

```
User: "Save progress, I need to stop"

Claude:
1. Ask: "What did we get done?"
   User: "Started the sharing feature, got the UI done but API not finished"
2. Ask: "What's blocking?"
   User: "Need to figure out auth for the share token"
3. Ask: "Next session plan?"
   User: "Finish the API, add tests"
4. Append session:
   ## [2025-01-15] | Sharing Feature (Partial)
   **Completed**: Share button UI component
   **Files**: ShareButton.tsx
   **Status**: 🚧 In Progress
   **Blockers**: Need to design auth for share tokens
   **Next Steps**: Implement share API, add token auth, write tests
```

---

## Scenario 3: Infer from Conversation

```
User: "Just infer what we did"

Claude:
1. Review conversation history
2. Note:
   - Created 3 files (ShareButton.tsx, route.ts, types.ts)
   - Discussed token-based auth approach
   - Ran tests, all passing
   - Suggested analytics as next step
3. Read progress.md
4. Append session:
   ## [2025-01-15] | Recipe Sharing Implementation
   **Completed**:
   - Share button component with copy-to-clipboard
   - Share API endpoint with token generation
   - Type definitions for sharing
   **Files**:
   - `components/ShareButton.tsx` - Share UI
   - `app/api/share/route.ts` - Token generation
   - `types/sharing.ts` - Type definitions
   **Key Decisions**:
   - Token-based sharing (UUID v4, 24hr expiry)
   - Copy-to-clipboard using navigator.clipboard
   **Status**: ✓ Shipped
   **Next Steps**: Add analytics tracking for share events
```

---

## Scenario 4: Debugging Session

```
User: "Log this debugging session"

Claude:
1. Ask: "What bug did we fix?"
   User: "Share button wasn't working in Safari"
2. Ask: "What was the issue?"
   User: "Clipboard API needs https, was failing in dev"
3. Ask: "How did we fix it?"
   User: "Added fallback to document.execCommand"
4. Append session:
   ## [2025-01-15] | Safari Clipboard Bug Fix
   **Completed**: Fixed share button Safari compatibility
   **Files**: `components/ShareButton.tsx` - Added clipboard fallback
   **Key Decisions**:
   - Use navigator.clipboard with fallback to execCommand for Safari/http
   - Show error toast if both methods fail
   **Status**: ✓ Shipped
   **Next Steps**: Test on mobile Safari, consider adding share sheet API
```

---

## Scenario 5: Multiple Features in One Session

```
User: "We did a lot today, log it all"

Claude:
1. Ask: "What did we complete?"
   User: "Share feature, analytics, and dark mode toggle"
2. Ask: "Any issues?"
   User: "Analytics is shipping errors to console, need to debug"
3. Ask: "Next session?"
   User: "Fix analytics errors, add user settings page"
4. Append session:
   ## [2025-01-15] | Multi-Feature Session
   **Completed**:
   - Recipe sharing with token-based auth (✓ shipped)
   - Dark mode toggle in settings (✓ shipped)
   - Analytics tracking (🚧 partial - has bugs)
   **Files**:
   - `components/ShareButton.tsx` - Share UI
   - `app/api/share/route.ts` - Share API
   - `components/DarkModeToggle.tsx` - Theme toggle
   - `lib/analytics.ts` - Event tracking (buggy)
   **Status**: 🚧 In Progress
   **Blockers**: Analytics throwing console errors on page load
   **Next Steps**:
   - Debug analytics initialization
   - Add user settings page
   - Test dark mode persistence
   **Session Duration**: ~3 hours
```

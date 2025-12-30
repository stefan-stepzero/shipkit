# Example Scenarios

Different ways route documentation is used and updated.

---

## Scenario 1: First Time Documentation

**Context**: User just built first few routes, no implementations.md exists yet

**User**: "Document my routes"

**Process**:
1. Ask: "Which routes?" → User: "All of them"
2. Scan all route files in project (no timestamp comparison yet)
3. Detect: 3 routes found
4. Extract data fetching, auth, dependencies for each
5. Generate documentation entries for all 3 routes
6. **Create** `.shipkit-lite/implementations.md` with:
   - Header with "Last route documentation scan: [now]"
   - All 3 route entries
   - Empty components section

**Result**: New file created with complete current state

---

## Scenario 2: Incremental Update

**Context**: implementations.md exists, user added 2 new routes since last scan

**User**: "Update route docs"

**Process**:
1. Read `.shipkit-lite/implementations.md`
2. Find "Last route documentation scan: 2025-01-10 15:00:00"
3. Compare route file mtimes vs scan timestamp
4. Find: 2 routes modified after scan time
5. Extract info for those 2 routes only (skip unchanged routes)
6. **Archive** current implementations.md → `archives/implementations-2025-01-15-14-32-00.md`
7. **Write new** implementations.md with:
   - Updated timestamp: "Last route documentation scan: 2025-01-15 14:32:00"
   - All route entries (3 old + 2 new = 5 total)
   - Preserve existing component entries

**Result**: Clean snapshot with all current routes, old version archived

---

## Scenario 3: Force Full Re-scan

**Context**: User refactored routes, wants to re-document everything

**User**: "Re-document all routes from scratch"

**Process**:
1. User explicitly requests full scan (ignore timestamp)
2. Scan ALL route files regardless of modification time
3. Extract info for all routes
4. **Archive** current implementations.md
5. **Write new** implementations.md with:
   - Current timestamp
   - All routes (complete fresh scan)

**Result**: Full refresh, captures any refactoring changes

---

## Scenario 4: No Changes

**Context**: implementations.md exists, no routes modified since last scan

**User**: "Update route docs"

**Process**:
1. Read implementations.md
2. Find "Last route documentation scan: [yesterday]"
3. Compare route file mtimes
4. Find: NO routes modified after scan time
5. Report: "No route changes detected since last scan"
6. Don't update timestamp (nothing changed)

**Result**: No changes made, saved user time

---

## Scenario 5: Specific Route Documentation

**Context**: User just built one new route, wants to document just that

**User**: "Document the /dashboard/analytics route I just added"

**Process**:
1. User specifies exact route path
2. Find file: `app/dashboard/analytics/page.tsx`
3. Extract info for ONLY that route
4. **Archive** current implementations.md (if exists)
5. **Write new** implementations.md with:
   - Updated timestamp
   - All existing routes + new route entry
   - Preserve components section

**Result**: Targeted documentation update

---

## Scenario 6: Multi-Framework Project

**Context**: Project uses Next.js + separate SvelteKit admin panel

**User**: "Document all routes"

**Process**:
1. Read stack.md → Detects: Next.js + SvelteKit
2. Scan routes using both framework patterns:
   - Next.js: `app/**/page.tsx`
   - SvelteKit: `src/routes/**/+page.svelte`
3. Classify routes by framework
4. Document each with framework-specific patterns
5. Generate entries with framework indicator

**Example entry**:
```markdown
### `/admin/users` - SvelteKit Page

**File**: `src/routes/admin/users/+page.svelte`
**Framework**: SvelteKit

**Data Strategy**:
- Fetching: Server load function
- Method: `+page.server.ts` load
- Sources: Supabase admin queries
```

---

## Scenario 7: Discovering Undocumented Components

**Context**: While documenting routes, skill finds components not yet documented

**Process**:
1. Document routes as normal
2. Detect component dependencies: `<DashboardLayout>`, `<StatsCard>`
3. Check implementations.md components section
4. Find: Components not documented yet
5. Suggest next step after route documentation

**Output**:
```
✅ Route documentation updated

📋 Documented routes:
  • /dashboard - Uses DashboardLayout, StatsCard
  • /profile - Uses ProfileForm, AvatarUpload

⚠ Found 4 undocumented components:
  • DashboardLayout
  • StatsCard
  • ProfileForm
  • AvatarUpload

👉 Next: Run /lite-component-knowledge to document these components
```

---

## Scenario 8: Auth Pattern Evolution

**Context**: User migrated from component guards to middleware

**User**: "Re-document routes to capture new auth patterns"

**Process**:
1. Force full re-scan (ignore timestamps)
2. Re-extract auth patterns for all routes
3. Detect new pattern: middleware.ts with matchers
4. Update all route entries with new auth method
5. **Archive** old version (preserves history of migration)
6. **Write new** version with updated auth patterns

**Before** (old archive):
```markdown
### `/dashboard` - Protected Route

**Auth**:
- Protected: Yes
- Method: Component-level guard (`useUser` hook)
```

**After** (new implementations.md):
```markdown
### `/dashboard` - Protected Route

**Auth**:
- Protected: Yes
- Method: Middleware matcher `/dashboard/:path*`
```

---

## Scenario 9: Hybrid Data Fetching Detection

**Context**: Route uses Server Component for initial load + Client Component for interactions

**Process**:
1. Analyze route file structure
2. Detect:
   - Page component is async (Server Component)
   - Contains `'use client'` children components
   - Server Component fetches initial data
   - Client Components use hooks for dynamic data
3. Classify as "Hybrid"
4. Document both patterns

**Example entry**:
```markdown
### `/dashboard/stats` - Hybrid

**Data Strategy**:
- Fetching: Hybrid (Server initial + Client dynamic)
- Method:
  - Server: Direct Supabase query for initial stats
  - Client: SWR for real-time updates (child component)
- Sources: Supabase `stats` table

**Key Patterns**:
- Server Component pre-fetches last 24h for instant display
- Client `<LiveStats>` component polls every 30s for updates
- Progressive enhancement: works without JS (shows static data)
```

---

## Scenario 10: API Route Documentation

**Context**: User wants to document both page routes AND API routes

**Process**:
1. Scan both page routes AND `/api` directory
2. Detect API routes: `app/api/**/route.ts`
3. Extract different patterns for API routes:
   - HTTP methods (GET, POST, etc.)
   - Request validation
   - Response format
4. Document API routes separately from pages

**Example**:
```markdown
## Routes

### `/dashboard` - Page

[Regular page entry...]

---

### `POST /api/items` - API Endpoint

**File**: `app/api/items/route.ts`
**Last documented**: 2025-01-15 14:32:00

**Auth**: Bearer token validation
**Validation**: Zod schema `CreateItemSchema`
**Database**: INSERT into `items` table
**Response**: 201 Created with item object

---
```

---

## Tips for Different Scenarios

**First time**:
- Document all routes to establish baseline
- Don't worry about timestamps yet

**Incremental**:
- Trust timestamp-based freshness
- Only document what changed
- Saves time on large codebases

**After refactoring**:
- Force full re-scan
- Capture architectural changes

**Targeted**:
- Document specific route user specifies
- Faster for single-route updates

**Multi-framework**:
- Leverage stack.md to detect all frameworks
- Use framework-specific patterns for each

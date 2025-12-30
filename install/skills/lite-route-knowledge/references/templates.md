# Documentation Templates

Templates for documenting route implementations.

---

## Route Documentation Entry Template

**Use this template for each documented route**:

```markdown
### `/route-path` - [Page Type]

**File**: `path/to/file.tsx`
**Last documented**: [timestamp]

**Data Strategy**:
- Fetching: [Server Component | Client Component | Hybrid]
- Method: [Direct async | useEffect | SWR | React Query | Server Actions]
- Sources: [Supabase | API route | External API]

**Auth**:
- Protected: [Yes/No]
- Method: [Middleware | Component guard | Server-side check]
- Requires: [Authenticated user | Specific role | RLS policy]

**RLS Policies** (if using Supabase):
- `policy_name` - Policy description
- `another_policy` - Another policy description

**Dependencies**:
- Hooks: `hookName1`, `hookName2`
- Components: `ComponentName1`, `ComponentName2`
- Actions: `actionName` (Server Action)
- Utils: `utilName1`, `utilName2`

**Key Patterns**:
- [Notable implementation detail 1]
- [Notable implementation detail 2]

---
```

---

## Complete File Structure Template

**implementations.md** structure with routes section:

```markdown
# Implementations

**Last route documentation scan**: [current timestamp]
**Last component documentation scan**: [timestamp or "Not yet scanned"]

---

## Routes

### `/dashboard` - Server Component

**File**: `app/dashboard/page.tsx`
**Last documented**: 2025-01-15 14:32:00

**Data Strategy**:
- Fetching: Server Component
- Method: Direct async with Supabase
- Sources: Supabase `dashboard_data` table

**Auth**:
- Protected: Yes
- Method: Middleware protection
- Requires: Authenticated user (RLS enforced)

**RLS Policies**:
- `dashboard_access` - User can only see own dashboard data

**Dependencies**:
- Components: `DashboardLayout`, `StatsCard`
- Utils: `formatCurrency`, `calculateStats`

**Key Patterns**:
- Uses parallel queries with Promise.all()
- Caches dashboard stats for 5 minutes

---

### `/profile` - Client Component

**File**: `app/profile/page.tsx`
**Last documented**: 2025-01-15 14:32:00

**Data Strategy**:
- Fetching: Client Component
- Method: SWR with revalidation
- Sources: Supabase via client-side query

**Auth**:
- Protected: Yes
- Method: Component-level guard
- Requires: Authenticated user

**Dependencies**:
- Hooks: `useUser`, `useProfile`
- Components: `ProfileForm`, `AvatarUpload`
- Actions: `updateProfile` (Server Action for mutations)

**Key Patterns**:
- Real-time profile updates via SWR
- Optimistic UI updates on form submission

---

## Components

[Component entries from component-knowledge-lite]

---
```

---

## Example Complete Route Entry

**Real-world example with all sections filled**:

```markdown
### `/dashboard/analytics` - Hybrid (Server Layout + Client Charts)

**File**: `app/dashboard/analytics/page.tsx`
**Last documented**: 2025-01-15 16:45:23

**Data Strategy**:
- Fetching: Hybrid
- Method: Server Component fetches initial data, Client Component for interactive charts
- Sources: Supabase `analytics_events` table + aggregation queries

**Auth**:
- Protected: Yes
- Method: Middleware matcher `/dashboard/:path*`
- Requires: Authenticated user with `analytics_access` role

**RLS Policies**:
- `team_analytics` - User can only see analytics for their team
- `time_range_limit` - Data limited to last 90 days for non-admin users

**Dependencies**:
- Hooks: `useUser`, `useAnalytics`, `useChartData`
- Components: `AnalyticsLayout`, `LineChart`, `BarChart`, `DateRangePicker`
- Actions: `exportAnalytics` (Server Action for CSV export)
- Utils: `formatNumber`, `calculateGrowth`, `aggregateByDay`

**Key Patterns**:
- Server Component pre-fetches last 30 days for instant display
- Client Component allows date range selection with dynamic refetching
- Charts use React Query for caching and background updates
- Export feature uses Server Action to generate CSV server-side
- Implements progressive enhancement (works without JS for basic view)

---
```

---

## Minimal Route Entry (Simple Route)

**For basic routes with minimal complexity**:

```markdown
### `/about` - Static Page

**File**: `app/about/page.tsx`
**Last documented**: 2025-01-15 14:32:00

**Data Strategy**:
- Fetching: Server Component (static)
- Method: No data fetching
- Sources: N/A

**Auth**:
- Protected: No
- Method: Public route

**Dependencies**: None

---
```

---

## API Route Template

**For documenting API endpoints**:

```markdown
### `POST /api/items` - Create Item

**File**: `app/api/items/route.ts`
**Last documented**: 2025-01-15 14:32:00

**Auth**:
- Protected: Yes
- Method: Bearer token validation
- Requires: Authenticated user

**Validation**:
- Input: Zod schema `CreateItemSchema`
- Fields: `name` (string), `description` (string), `category` (enum)

**Database**:
- Operation: INSERT into `items` table
- RLS: `items_insert` policy (user must own parent resource)

**Response**:
- Success: 201 Created with item object
- Error: 400 Bad Request (validation), 401 Unauthorized, 500 Server Error

**Dependencies**:
- Utils: `validateRequest`, `handleAPIError`
- Schemas: `CreateItemSchema`

---
```

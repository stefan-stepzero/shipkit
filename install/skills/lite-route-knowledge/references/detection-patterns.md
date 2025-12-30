# Route Detection Patterns

Framework-specific patterns for detecting routes, data fetching strategies, and auth requirements.

---

## Framework Route Detection

### Next.js App Router (Server Components)

**Route detection**:
```bash
app/**/page.tsx
app/**/layout.tsx
app/**/loading.tsx
app/**/error.tsx
```

**Data strategy indicators**:
```tsx
// Server Component (no 'use client')
export default async function Page() {
  const data = await db.query(...) // Direct DB
  const res = await fetch(..., { cache: 'no-store' }) // Server fetch
}

// Client Component
'use client'
export default function Page() {
  const { data } = useSWR(...) // Client fetch
}
```

**Auth patterns**:
```tsx
// Middleware protection
// Check middleware.ts matcher: ['/dashboard/:path*']

// Server-side check
import { auth } from '@/auth'
const session = await auth()
if (!session) redirect('/login')
```

---

### Next.js Pages Router

**Route detection**:
```bash
pages/**/*.tsx
pages/api/**/*.ts (API routes)
```

**Data strategy indicators**:
```tsx
// SSR
export async function getServerSideProps() { ... }

// SSG
export async function getStaticProps() { ... }

// Client
export default function Page() {
  useEffect(() => fetch(...))
}
```

---

### SvelteKit

**Route detection**:
```bash
src/routes/**/+page.svelte
src/routes/**/+page.server.ts
src/routes/**/+layout.svelte
```

**Data strategy indicators**:
```ts
// Server load
export async function load({ fetch }) {
  const data = await fetch(...) // Server-side
}
```

---

### React Router / Vite

**Route detection**:
```bash
src/routes/**/*.tsx
src/pages/**/*.tsx
```

**Data strategy indicators**:
```tsx
// Client-only (typical for SPA)
useEffect(() => fetch(...))
const { data } = useQuery(...)
```

---

### Nuxt

**Route detection**:
```bash
pages/**/*.vue
```

---

## Data Fetching Strategy Classification

### Server Component (Next.js App Router)

**Characteristics**:
- No `'use client'` directive
- `async function` component
- Direct `await fetch()` or `await db.query()`

**Pros**: SEO-friendly, secure, fast initial load
**Cons**: Can't use React hooks

**Example**:
```tsx
async function Page() {
  const data = await fetch(...) // Direct async
  const dbData = await supabase.from(...) // Direct DB query
}
```

---

### Client Component

**Characteristics**:
- Has `'use client'` directive
- Uses `useEffect`, `useSWR`, `useQuery`, etc.

**Pros**: Interactive, real-time updates
**Cons**: Client-side bundle, slower initial render

**Example**:
```tsx
'use client'
function Page() {
  const { data } = useSWR('/api/data')
  useEffect(() => { ... })
}
```

---

### Hybrid

**Characteristics**:
- Layout is Server Component
- Child components are Client Components
- Combines benefits

**Example**:
```tsx
// Layout (Server Component)
export default function Layout({ children }) {
  const data = await fetchData()
  return <div>{children}</div>
}

// Page (Client Component)
'use client'
export default function Page() {
  const [state, setState] = useState()
}
```

---

### Server Actions (Next.js)

**Characteristics**:
- `'use server'` directive
- Form mutations without API routes

**Pattern**: Server Component + Server Action for mutations

**Example**:
```tsx
'use server'
async function createItem(formData: FormData) {
  const data = await db.insert(...)
}
```

---

### API Routes

**Characteristics**:
- Separate `/api/*` endpoints
- Called from client via `fetch()`

**Pattern**: Traditional REST API

**Example**:
```tsx
// API route
export async function GET(req: Request) {
  const data = await db.query()
  return Response.json(data)
}

// Client usage
const res = await fetch('/api/data')
```

---

## Auth Pattern Detection

### Middleware-Based Protection

**File**: `middleware.ts` or `middleware.js`

**Pattern**:
```ts
export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*']
}

export function middleware(req: NextRequest) {
  const token = req.cookies.get('session')
  if (!token) return NextResponse.redirect('/login')
}
```

**Detection**: Check if route path matches middleware matcher

---

### Component-Level Guards

**Pattern**:
```tsx
export default function ProtectedPage() {
  const { user, isLoading } = useUser()

  if (isLoading) return <Spinner />
  if (!user) redirect('/login')

  return <Dashboard />
}
```

**Detection**: Look for early returns checking `user` or `session`

---

### Server-Side Checks

**Pattern**:
```tsx
export default async function Page() {
  const session = await getServerSession()
  if (!session) redirect('/login')
}
```

**Detection**: `getServerSession`, `auth()`, or similar in Server Component

---

### RLS (Row Level Security) - Supabase

**Pattern**:
```tsx
// Automatically enforced by Supabase
const { data } = await supabase
  .from('dashboard_data')
  .select('*')
// RLS policy 'dashboard_access' filters results by user_id
```

**Detection**:
- Look for comments mentioning policy names
- Check table name (e.g., `user_profiles` likely has user RLS)
- Infer from context (authenticated queries assume RLS)

---

## Dependency Detection

### Hooks
**Patterns**: `useUser`, `useDashboard`, `useAuth`, custom hooks starting with `use`

### Components
**Patterns**: `<Layout>`, `<DataTable>`, `<AuthGuard>`, capitalized JSX tags

### Utilities
**Patterns**: `formatDate`, `validateInput`, imported helper functions

### Server Actions
**Patterns**: `'use server'` directive, async functions passed to forms

---

## Tips for Pattern Matching

**Be specific about data sources**:
- ❌ "Uses Supabase" (vague)
- ✅ "Server Component with direct supabase.from('users').select()" (specific)

**Document auth method clearly**:
- ❌ "Protected route" (how?)
- ✅ "Protected via middleware matcher in middleware.ts" (clear)

**Note RLS policies**:
- If you see RLS policy names in comments, document them
- If table is user-scoped, mention "Likely RLS-protected" + table name

**Track dependencies**:
- List all imported hooks, components, utilities
- This helps understand what else needs to be documented

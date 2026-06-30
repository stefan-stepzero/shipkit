# Ecosystem Defaults — Next.js Full-Stack (App Router)

> **LLM-generated reference.** Authored 2026-06-27 with then-current best practice.
> **Refresh:** regenerate when stale or after a major Next.js / library release — ask Claude to "regenerate references/ecosystem-defaults/nextjs-fullstack.md with current best practice."

## When to use

Full-stack Next.js applications on the App Router — UI plus server-side logic (Server Actions, Route Handlers) in one codebase, typically deployed to a serverless/edge platform. If the project pairs a Next.js frontend with a separate backend (e.g. a Python API), consult that backend's reference too.

## Non-negotiable defaults

- **One validation library across the whole stack** — forms, API/action inputs, and env vars all validated by the same schema library, with types inferred from the schema (never hand-maintained in parallel).
- **A typed ORM / query builder, not raw SQL**, with managed migrations.
- **A real auth library/provider — never custom auth.** Sessions/tokens, password handling, and OAuth flows are solved problems.
- **Validate at the trust boundary**: every Server Action and Route Handler validates its input before doing work; never trust client-shaped data.
- **Type-safe data fetching/mutation** rather than untyped `fetch` glue.

## Recommended libraries by concern

| Concern | Default | Notes |
|---|---|---|
| Validation (everything) | **Zod** | Forms, action/route input, env-var parsing; infer types from schemas |
| Server mutations | **Server Actions** for most mutations; **Route Handlers** for complex/public API surface | |
| Type-safe actions | **next-safe-action** (or a typed action wrapper) | Validated input + typed result for Server Actions |
| ORM | **Prisma** or **Drizzle** | Typed models; managed migrations |
| Auth | **Auth.js (NextAuth)**, **Clerk**, or **Supabase Auth** | Pick one; do not hand-roll |
| Forms | **React Hook Form** + Zod resolver | Schema-driven validation, minimal re-renders |
| Client data fetching | **TanStack Query** | Caching, invalidation, background refetch |
| Styling | **Tailwind CSS** | Utility-first; consistent design tokens |
| Component primitives | **shadcn/ui** or **Radix** | Accessible primitives; don't rebuild dialogs/menus |
| Env-var safety | Zod-validated env module (e.g. `@t3-oss/env-nextjs`) | Fail the build on missing/invalid env |

## Anti-patterns to avoid

- Two sources of truth for a shape — a TypeScript `interface` *and* hand-written runtime checks — instead of inferring the type from one Zod schema.
- Custom authentication (bespoke session cookies, hand-rolled JWT signing, DIY password hashing).
- Unvalidated Server Action / Route Handler inputs ("the client already validated it").
- Raw SQL strings for normal CRUD instead of the ORM.
- Reaching for a heavy client-state library (Redux) when Server Components + TanStack Query cover server state.
- Reading `process.env.X` directly in many files instead of one validated env module.
- Re-implementing accessible UI primitives (modals, dropdowns, comboboxes) by hand.

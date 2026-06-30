# Ecosystem Defaults — React SPA (Vite)

> **LLM-generated reference.** Authored 2026-06-27 with then-current best practice.
> **Refresh:** regenerate when stale or after a major React / tooling release — ask Claude to "regenerate references/ecosystem-defaults/react-spa.md with current best practice."

## When to use

Client-rendered React single-page applications, typically Vite-based, talking to a separate API. If the backend is also in scope, read its ecosystem-defaults file (e.g. `python-api.md`).

## Non-negotiable defaults

- **Separate server state from client state.** Server data (fetched, cached, invalidated) and local UI state are different problems — use a server-state library for the former, a light store for the latter.
- **Schema-first form and input validation**, with types inferred from the schema.
- **A real router**, not hand-rolled `window.location` switching.
- **A component test setup that renders real components and mocks the network at the boundary**, not deep-mocked internals.

## Recommended libraries by concern

| Concern | Default | Notes |
|---|---|---|
| Server state | **TanStack Query** | Caching, refetch, invalidation for API data |
| Client/UI state | **Zustand** or **Jotai** | Lightweight; reach for Redux only if it already exists |
| Validation | **Zod** | Forms and API-response parsing; infer types from schemas |
| Forms | **React Hook Form** + Zod resolver | Schema-driven, minimal re-renders |
| Routing | **TanStack Router** or **React Router** | Type-safe routing preferred |
| Styling | **Tailwind CSS** + **shadcn/ui** | Utility-first + accessible primitives |
| API mocking (tests) | **MSW** | Mock at the network boundary, not the fetch wrapper |
| Tests | **Vitest** + **Testing Library** | Vite-native; not Jest for a Vite app |
| Data fetching transport | **fetch** wrapped once, or a typed client | Centralize base URL / auth headers / error handling |

## Anti-patterns to avoid

- Storing fetched server data in a global client store and hand-writing cache/invalidation logic (that's what TanStack Query is for).
- Reaching for Redux + middleware on a small app when Zustand/Jotai suffice.
- Hand-rolled form validation and error state instead of React Hook Form + Zod.
- A homegrown router built on `window.location` / `history` listeners.
- Jest in a Vite project (config friction; Vitest is the native fit).
- Deep-mocking modules in tests instead of mocking the network with MSW.
- Duplicating a response shape as a TS `interface` *and* manual runtime checks instead of one Zod schema.

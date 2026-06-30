# Ecosystem Defaults — Python Backend APIs

> **LLM-generated reference.** Authored 2026-06-27 with then-current best practice.
> **Refresh:** regenerate when stale or after a major framework/library release — ask Claude to "regenerate references/ecosystem-defaults/python-api.md with current best practice."

## When to use

Python backend services exposing an HTTP API (REST or GraphQL) — request/response handling, persistence, auth, background work. If the service is primarily an LLM pipeline, read `python-llm.md` as well.

## Non-negotiable defaults

- **Schema-first validation at every boundary.** Request bodies, query params, responses, env config — all validated by typed models, never hand-written `if`-checks.
- **An ORM / query builder, not raw SQL strings.** Typed models that line up with your validation schemas; migrations managed by tooling, not ad-hoc `ALTER TABLE`.
- **Async-capable HTTP framework and async DB drivers** so I/O-bound endpoints scale.
- **Tests with fixtures and a real test database/transaction**, not mocks-everywhere.
- **Reproducible local dependencies** (DB, cache, queue) via containerization, so "works on my machine" isn't the contract.

## Recommended libraries by concern

| Concern | Default | Notes |
|---|---|---|
| Web framework | **FastAPI** | Pydantic request/response models, async-native, OpenAPI for free |
| Data modeling / validation | **Pydantic v2** | Shared between API schemas and domain models |
| App config / secrets | **pydantic-settings** | Validated settings object; fail fast on missing env |
| ORM | **SQLAlchemy 2.x** (or SQLModel for Pydantic-native models) | Typed models; avoid raw SQL except for tuned hot paths |
| Migrations | **Alembic** | Versioned, reviewable migrations |
| Outbound HTTP | **httpx** (async) | Not `requests` |
| Background jobs | **Celery**, **Dramatiq**, or a hosted queue | See `mechanism-standards.md` → Background Jobs |
| Auth | A library / provider, not custom crypto | OAuth2/OIDC via the framework's security utilities or an auth provider |
| Tests | **pytest** + fixtures, `httpx`/`ASGITransport` test client | Transactional DB fixtures; not `unittest` |
| Local dev deps | **Docker Compose** (or equivalent) | DB + cache + queue reproducible |
| Logging | **structlog** | Structured, request-scoped context |

## Anti-patterns to avoid

- Manual `if not body.get("email"): ...` validation instead of a request model.
- Raw, string-interpolated SQL (injection risk + no typing) for normal CRUD.
- Schema changes applied by hand instead of through migrations.
- `requests` (sync) inside async endpoints.
- `unittest`-style mock-heavy tests that never touch a real DB.
- Rolling your own password hashing / token signing / session crypto.
- One giant `main.py` with no separation between routing, domain logic, and persistence.
- Secrets read via scattered `os.getenv` instead of one validated settings object.

# Mechanism Standards — What to Reach For

> **Stable, stack-agnostic reference.** Maps common mechanism types to the standard solution Claude should default to, plus the anti-patterns to avoid. This file tells you *what* category of solution to reach for; the `ecosystem-defaults/<stack>.md` files name the *specific* library for your stack.

Use during **Step 2b: Ecosystem Audit**. For each mechanism, find its category below, default to the standard, and only deviate (recording `whyNotStandard`) when the standard genuinely doesn't fit.

The tone is **"default to this," not "you must."** A conscious, recorded deviation is fine; an un-considered reinvention is the failure mode this file exists to prevent.

---

| Mechanism | Default to (positive recommendation) | Don't do this (anti-patterns) |
|---|---|---|
| **LLM Chain / AI Pipeline** | Typed models for every step's I/O (Pydantic/Zod). Schema-enforced **structured outputs** over string parsing. Stream long generations. Retry with exponential backoff. Track token budget/cost. Official provider SDK, not hand-rolled HTTP. | Regex/`json.loads` over free-text completions; the legacy completions API; a heavyweight orchestration framework wrapped around a trivial linear chain; no retry on rate limits. |
| **Authentication** | Use an auth library/provider (Auth.js, Clerk, Supabase Auth, Auth0, framework security utils). OAuth2/OIDC for third-party. Pick **one** session model — JWT *or* server sessions, not both. | Rolling custom auth — hand-rolled JWT signing, DIY password hashing, bespoke session cookies. Storing passwords reversibly. Mixing JWT and session auth incoherently. |
| **Data Validation** | Schema-first validation at **all** boundaries (API input, form input, env vars, config). Stack-native: Pydantic (Python), Zod (TypeScript). Infer types from the schema (one source of truth). | Manual `if`-check validation; a TS `interface` *and* a parallel runtime check (two sources of truth); trusting client-supplied data; validating only some boundaries. |
| **Database Access** | An ORM or query builder, not raw SQL. Migrations managed by tooling. Connection pooling. Typed models that match your validation schemas. | String-interpolated SQL for normal CRUD (injection + no typing); schema changes by hand instead of migrations; a new DB connection per request. |
| **File Processing / Upload** | Presigned URLs for direct upload (S3/R2/Supabase Storage). Stream large files. **Validate file type/size server-side.** Established libraries for format-specific parsing (pdf parsers, image processors, ffmpeg). | Proxying large uploads through your app server; trusting the client-declared content type; hand-parsing binary formats; loading huge files fully into memory. |
| **Background Jobs / Queues** | A real queue service (BullMQ, Celery, Dramatiq, Inngest, Trigger.dev). Idempotent jobs. Dead-letter queue for failures. | `setTimeout`/`setInterval` or ad-hoc cron scripts as a job system; non-idempotent jobs that double-charge on retry; silently dropping failed jobs. |
| **Payments / Billing** | A payments provider (Stripe, Lemon Squeezy). **Webhook-driven** state, not polling. Idempotent webhook handlers (verify signature, dedupe by event ID). | Building payment processing yourself; storing raw card data; polling for payment status; non-idempotent webhook handlers that double-apply. |
| **Email / Notifications** | A transactional email/notification service (Resend, Postmark, SendGrid). Template-based content. Queue sends for reliability. | String-concatenated email bodies; sending synchronously in the request path; no retry/queue; sending bulk from your own SMTP without deliverability tooling. |
| **Search** | A full-text/search service (Algolia, Meilisearch, Typesense, or PostgreSQL FTS). Faceted search for filtering. Debounced typeahead. | `LIKE '%term%'` queries as a search engine; unindexed full-table scans; firing a query on every keystroke without debounce. |
| **Real-time / WebSockets** | A managed realtime service (Pusher, Ably, Supabase Realtime, PartyKit) or Socket.io. Let the library handle presence and reconnection. | Hand-rolling the raw WebSocket protocol; no reconnection/backoff; building presence tracking from scratch. |
| **PDF / Document Generation** | Server-side rendering (Puppeteer/Playwright, or a PDF library like react-pdf / a document skill). Template-based layout. | Client-side generation for critical/official documents; string-built layout; rendering inconsistently across browsers. |
| **Caching** | Redis/Upstash for shared cache. HTTP cache headers for CDN. TanStack Query/SWR for client-side cache. **Define the invalidation strategy up front.** | In-process dicts as a shared cache across instances; caching with no invalidation plan; caching user-specific data in a shared key. |

---

## How to apply this

1. Map each mechanism to a row above.
2. Adopt the positive recommendation, then open the matching `ecosystem-defaults/<stack>.md` for the concrete library in your stack.
3. Record the libraries on the mechanism (`uses: [...]`).
4. If you deviate from the standard, record **why** (`whyNotStandard: "..."`). A deviation without a reason is the thing to catch in review.

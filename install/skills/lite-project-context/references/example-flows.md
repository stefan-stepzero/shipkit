# Example Flows

Common scenarios for project context scanning.

---

## Flow 1: First Run

```
User: "Scan the project"

Claude:
1. Check .shipkit-lite/stack.md → doesn't exist
2. Ask: "First run detected. Scan now?"
3. User: "Yes"
4. Scan package.json → Next.js 14, React 18, Tailwind 3
5. Scan .env.example → 4 required vars
6. Scan supabase/migrations → 3 tables
7. Generate stack.md, env-requirements.md, schema.md
8. Output: "✅ Context generated. 33 deps, 3 tables, 4 env vars."
9. Suggest: "Run `/lite-project-status` to see project health"
```

---

## Flow 2: Cached Read (Fresh Context)

```
User: "What's my stack?"

Claude:
1. Check .shipkit-lite/stack.md → exists
2. Compare times: stack.md (Jan 15 14:32) > package.json (Jan 14 10:00)
3. Context is fresh, skip scan
4. Read stack.md (~50 tokens)
5. Output summary from cached file
6. "Context last updated: Jan 15. Still fresh."
```

---

## Flow 3: Stale Context

```
User: "Update context"

Claude:
1. Check .shipkit-lite/stack.md → exists
2. Compare times: package.json (Jan 16 09:00) > stack.md (Jan 15 14:32)
3. Ask: "⚠️ Context appears stale. Rescan?"
4. User: "Yes"
5. Rescan all files
6. Detect new dependency: zod added
7. Regenerate stack.md with updated info
8. Output: "✅ Context refreshed. 34 deps (was 33), added zod."
```

---

## Flow 4: Triggered by shipkit-master-lite

```
Session start → shipkit-master-lite loads

shipkit-master-lite:
1. Try to read .shipkit-lite/stack.md → doesn't exist
2. Output: "⚠️ No project context found."
3. Suggest: "Run `/lite-project-context` to scan your project first."

User: "/lite-project-context"

[Follow first run flow]
```

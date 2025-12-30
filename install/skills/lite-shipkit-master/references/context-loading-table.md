# Context Loading Table

Which context files to load for each skill invocation.

---

## Context Loading by Skill

| Skill | Always Load | Conditionally Load |
|-------|-------------|-------------------|
| `/lite-project-status` | Glob .shipkit-lite/** | N/A |
| `/lite-project-context` | package.json | .env.example, migrations/, prisma/schema.prisma |
| `/lite-architecture-memory` | .shipkit-lite/architecture.md | N/A |
| `/lite-spec` | .shipkit-lite/specs/active/ | stack.md (tech choices), architecture.md (patterns) |
| `/lite-plan` | specs/active/[feature].md, stack.md | architecture.md, types.md, schema.md |
| `/lite-implement` | plans/[feature].md, stack.md | specs/, types.md, implementations.md |
| `/lite-component-knowledge` | .shipkit-lite/implementations.md | stack.md (to reference tech) |
| `/lite-route-knowledge` | .shipkit-lite/implementations.md | stack.md (to reference framework) |
| `/lite-quality-confidence` | implementations.md | specs/active/ (acceptance criteria) |
| `/lite-user-instructions` | .shipkit-lite/user-tasks/active.md | N/A |
| `/lite-work-memory` | .shipkit-lite/progress.md | N/A |

**Token budget per skill invocation: ~1500-2500 tokens**

---

## Loading Strategy

**Incremental loading pattern:**

```
Session start (500 tokens):
  - master SKILL.md
  - stack.md (if fresh)
  - architecture.md (if exists)

Skill invocation (~1500-2500 tokens):
  - Skill SKILL.md (~200 tokens)
  - Always Load files (~500-1000 tokens)
  - Conditionally Load files (~500-1000 tokens)

Total per interaction: ~2000-3000 tokens
```

**vs. Loading everything upfront:**
```
Session start: ~7000 tokens
  - All skills
  - All context files
```

**Efficiency gain: 85-90% token reduction through lazy loading**

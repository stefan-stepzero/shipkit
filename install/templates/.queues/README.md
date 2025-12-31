# Queue File Templates

**Purpose:** These templates define the format for queue files created by detection skills.

**Location in user projects:** `.shipkit-lite/.queues/`

**What are queue files?**
- Ephemeral markdown files that signal work needs to be done
- Created automatically by milestone detection skills
- Consumed by preventative skills (lite-integration-docs, lite-data-contracts, etc.)
- Deleted or archived after work is complete

**Queue file lifecycle:**
1. Detection skill scans project state (e.g., after spec created)
2. If work needed, creates queue file from template
3. lite-whats-next reads queues and suggests next skill
4. User runs suggested skill
5. Skill reads queue, performs work, marks items complete
6. Queue file archived or deleted when all items complete

**Why queues?**
- Automatic detection: Users don't need to remember to run preventative skills
- Timely suggestions: Skills triggered at the RIGHT workflow milestone
- Clear priorities: Queue shows exactly what needs attention
- Audit trail: Track what was detected and when

**Gitignore:** `.queues/` directory is git-ignored (ephemeral, not committed)

---

## Queue Templates

Each template below shows the format for a specific queue type:

1. **fetch-integration-docs.md.template** - Services needing current documentation
2. **define-data-contracts.md.template** - Data types/interfaces to define
3. **components-to-document.md.template** - Components needing documentation
4. **routes-to-document.md.template** - Routes/APIs needing documentation
5. **ux-audit-needed.md.template** - Components needing UX audit
6. **integrations-used.md.template** - Service integrations detected in code

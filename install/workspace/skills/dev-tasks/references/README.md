# Dev-Tasks - Extended References

This folder contains extended documentation for the dev-tasks skill.

## Files in This Folder

- **reference.md** - Comprehensive guide to dependency-ordered task breakdown (2000+ words)
  - Core principles of user story organization
  - Task format requirements and validation
  - Phase structure (Setup, Foundational, User Stories, Polish)
  - Dependency analysis and parallel execution
  - TDD integration patterns
  - Constitution compliance checking
  - Common patterns and anti-patterns

- **examples.md** - Concrete task breakdown examples for different feature types
  - User Authentication (Full TDD)
  - REST API CRUD (No TDD)
  - Frontend + Backend Integration
  - Minimal Single-Story Feature
  - Shows proper format, dependencies, and organization

## Adding Your Own References

Feel free to add:
- PDFs with task breakdown methodologies
- Links to articles about dependency management
- Notes from team discussions about task sizing
- Custom task templates for your domain
- Examples from past projects that worked well

Claude will read all files in this folder when running the skill.

## Quick Reference: Task Format

Every task must follow this format:
```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Example:**
```
- [ ] T012 [P] [US1] Create User model in src/models/user.py
```

Where:
- `- [ ]` = Checkbox (always present)
- `T012` = Task ID (sequential, in execution order)
- `[P]` = Parallel marker (optional, only if truly parallel)
- `[US1]` = Story label (required for user story phases)
- Rest = Clear description with exact file path

## Quick Reference: Phase Structure

```
Phase 1: Setup
  → Project initialization, dependencies, basic config

Phase 2: Foundational (CRITICAL - blocks all stories)
  → Shared infrastructure ALL stories depend on
  → Database, auth framework, API structure, base models

Phase 3+: User Stories (one phase per story, by priority)
  → Each story = vertical slice (models + services + endpoints)
  → Stories can run in parallel
  → Each story independently testable

Final Phase: Polish
  → Cross-cutting concerns, docs, optimization
```

## Constitution Integration

Before generating tasks, ALWAYS read:
```
.shipkit/skills/dev-constitution/outputs/constitution.md
```

The constitution defines:
- Project structure (file paths)
- Testing requirements (TDD? Coverage?)
- Architectural patterns (Repository? Service layer?)
- Naming conventions (PascalCase? camelCase?)

Tasks must align with constitution standards.

## When to Use This Skill

Run `/dev-tasks` after:
1. `/dev-specify` (spec.md exists)
2. `/dev-plan` (plan.md exists)

The skill generates `tasks.md` with:
- Dependency-ordered implementation tasks
- User story organization
- Parallel execution markers
- TDD integration (if requested)
- Constitution compliance

## Next Steps After Tasks Generated

After tasks.md is created:
1. Review task breakdown with team
2. Validate dependencies are correct
3. Confirm MVP scope (usually User Story 1 only)
4. Run `/dev-implement` to start execution

## Support

For questions about:
- **Task format:** See reference.md "Task Format Requirements"
- **Dependencies:** See reference.md "Dependency Analysis"
- **TDD integration:** See reference.md "TDD Integration"
- **Examples:** See examples.md for complete breakdowns

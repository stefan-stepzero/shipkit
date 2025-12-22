# Tasks: [FEATURE NAME]

**Created:** [DATE]
**Feature:** [FEATURE-NUMBER-AND-NAME]
**Input Documents:** spec.md, plan.md, constitution.md

**Organization:** Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Task Format

```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components:**
- **Checkbox**: `- [ ]` (markdown checkbox)
- **Task ID**: Sequential number (T001, T002, T003...) in execution order
- **[P] marker**: Include ONLY if task can run in parallel (different files, no dependencies)
- **[Story] label**: REQUIRED for user story phase tasks (e.g., [US1], [US2], [US3])
- **Description**: Clear action with exact file path

**Examples:**
- `- [ ] T001 Create project structure per implementation plan`
- `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`

---

## Path Conventions

Paths should match the project structure defined in plan.md:
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose:** Project initialization and basic structure

[SETUP TASKS - Project initialization, dependencies, basic configuration]

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose:** Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL:** No user story work can begin until this phase is complete

[FOUNDATIONAL TASKS - Database setup, authentication framework, API structure, base models, error handling, environment configuration]

**Checkpoint:** Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal:** [Brief description of what this story delivers from spec.md]

**Acceptance Criteria:** [From spec.md user story]

**Independent Test:** [How to verify this story works on its own]

### Tests for User Story 1 (if TDD requested)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation (RED phase of TDD)**

[TEST TASKS - Contract tests, integration tests, unit tests specific to US1]

### Implementation for User Story 1

[IMPLEMENTATION TASKS - Models, services, endpoints, validation, logging for US1]

**Checkpoint:** At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal:** [Brief description of what this story delivers from spec.md]

**Acceptance Criteria:** [From spec.md user story]

**Independent Test:** [How to verify this story works on its own]

### Tests for User Story 2 (if TDD requested)

[TEST TASKS for US2]

### Implementation for User Story 2

[IMPLEMENTATION TASKS for US2]

**Checkpoint:** At this point, User Stories 1 AND 2 should both work independently

---

[REPEAT FOR EACH USER STORY FROM spec.md]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose:** Improvements that affect multiple user stories

[POLISH TASKS - Documentation, code cleanup, performance optimization, security hardening, cross-cutting concerns]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1):** No dependencies - can start immediately
- **Foundational (Phase 2):** Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+):** All depend on Foundational phase completion
  - User stories can then proceed in parallel (if team capacity allows)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase):** Depends on all desired user stories being complete

### User Story Dependencies

[LIST DEPENDENCIES BETWEEN USER STORIES - Most should be independent]

### Within Each User Story

- Tests (if TDD) MUST be written and FAIL before implementation (RED-GREEN-REFACTOR)
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

[LIST PARALLEL EXECUTION OPPORTUNITIES - Tasks marked with [P]]

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if TDD):
Task: "[Test task 1]"
Task: "[Test task 2]"

# Launch all models for User Story 1 together:
Task: "[Model task 1]"
Task: "[Model task 2]"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE:** Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Task Summary

**Total Tasks:** [COUNT]
**Setup Tasks:** [COUNT]
**Foundational Tasks:** [COUNT]
**User Story Tasks:** [COUNT per story]
**Polish Tasks:** [COUNT]
**Parallel Opportunities:** [COUNT of tasks marked [P]]

---

## Constitution Compliance

All tasks follow patterns established in:
- **File:** `.shipkit/skills/dev-constitution/outputs/constitution.md`
- **Coding Standards:** [Reference relevant sections]
- **Testing Requirements:** [Reference relevant sections]
- **Architectural Patterns:** [Reference relevant sections]

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- If TDD: Verify tests fail (RED) before implementing (GREEN), then refactor (REFACTOR)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

# Dev-Tasks Reference: Dependency-Ordered Task Breakdown

**Purpose:** This reference provides comprehensive guidance for generating dependency-ordered, user-story-based task breakdowns that enable independent implementation and testing.

**Last Updated:** 2025-12-22

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [Task Organization Philosophy](#task-organization-philosophy)
3. [Dependency Analysis](#dependency-analysis)
4. [Task Format Requirements](#task-format-requirements)
5. [Phase Structure](#phase-structure)
6. [Parallel Execution Markers](#parallel-execution-markers)
7. [TDD Integration](#tdd-integration)
8. [Constitution Integration](#constitution-integration)
9. [Common Patterns](#common-patterns)
10. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

---

## Core Principles

### 1. User Story Organization

**Tasks MUST be organized by user story**, not by technical layer.

**Why:**
- Each user story represents a vertical slice of functionality
- Stories can be implemented independently
- Stories can be tested independently
- Stories can be delivered incrementally (MVP approach)
- Teams can work on different stories in parallel

**Traditional (WRONG) organization:**
```
Phase 1: All Models
Phase 2: All Services
Phase 3: All Endpoints
```

**User Story-Based (CORRECT) organization:**
```
Phase 1: Setup
Phase 2: Foundational (blocking prerequisites)
Phase 3: User Story 1 (models + services + endpoints for US1)
Phase 4: User Story 2 (models + services + endpoints for US2)
Phase 5: User Story 3 (models + services + endpoints for US3)
```

### 2. Independence First

Each user story phase should be:
- **Independently implementable:** Can be built without other stories being complete
- **Independently testable:** Can be verified without other stories working
- **Independently deliverable:** Can be deployed and provide value on its own

### 3. Constitution-Driven Task Patterns

All tasks must align with the technical standards and architectural decisions documented in `constitution.md`. The constitution defines:
- Coding standards and conventions
- Testing requirements and patterns
- Architectural patterns to follow
- Technology stack constraints
- File organization patterns

**Before generating tasks, read the constitution to ensure:**
- Task descriptions use correct naming conventions
- File paths follow established project structure
- Testing strategy matches constitution requirements
- Implementation patterns align with architectural decisions

### 4. Dependency Visibility

Dependencies between tasks must be explicit and clear:
- **Sequential dependencies:** Task B depends on Task A completing
- **Phase dependencies:** All tasks in Phase N depend on Phase N-1 completing
- **Story dependencies:** Story 2 may depend on Story 1 (but minimize these)
- **Parallel opportunities:** Tasks with no dependencies should be marked [P]

---

## Task Organization Philosophy

### The Three-Layer Model

Every feature implementation has three distinct layers:

#### Layer 1: Setup (Phase 1)
**Purpose:** Project initialization and shared infrastructure

**Contains:**
- Project structure creation
- Dependency installation
- Build configuration
- Linting/formatting setup
- Basic tooling configuration

**Characteristics:**
- Runs once per project
- No dependencies
- Many tasks can run in parallel
- Quick to complete

#### Layer 2: Foundational (Phase 2)
**Purpose:** Core infrastructure that ALL user stories depend on

**Contains:**
- Database schema and migrations framework
- Authentication/authorization framework
- API routing and middleware structure
- Base models/entities used by multiple stories
- Error handling infrastructure
- Logging infrastructure
- Environment configuration

**Characteristics:**
- **BLOCKS all user story work**
- Must be complete before ANY story begins
- Many tasks can run in parallel within this phase
- Critical path for the entire project

**Important:** Be disciplined about what goes here. Only include truly foundational items that multiple stories depend on. Story-specific infrastructure goes in that story's phase.

#### Layer 3: User Stories (Phase 3+)
**Purpose:** Deliver vertical slices of user-facing functionality

**Contains (per story):**
- Tests specific to this story (if TDD)
- Models specific to this story
- Services specific to this story
- Endpoints/UI specific to this story
- Validation specific to this story
- Integration specific to this story

**Characteristics:**
- One phase per user story
- Ordered by priority (P1, P2, P3...)
- Can run in parallel (if team capacity allows)
- Each story is independently testable
- Each story delivers value on its own

---

## Dependency Analysis

### Identifying Dependencies

When analyzing spec.md and plan.md, identify these dependency types:

#### 1. Data Dependencies
```
Example: UserService depends on User model existing
Task Order:
  T012 [P] [US1] Create User model in src/models/user.py
  T014 [US1] Implement UserService in src/services/user_service.py (depends on T012)
```

#### 2. Infrastructure Dependencies
```
Example: All user stories depend on authentication framework
Task Order:
  Phase 2: Foundational
    T005 Implement authentication framework
  Phase 3: User Story 1 (can only start after Phase 2 complete)
    T012 [US1] Create protected endpoint (uses auth from T005)
```

#### 3. Integration Dependencies
```
Example: Story 2 integrates with Story 1's functionality
Task Order:
  Phase 3: User Story 1
    T012-T017 [US1] Complete US1 functionality
  Phase 4: User Story 2
    T020-T022 [US2] Core US2 functionality
    T023 [US2] Integrate with User Story 1 components (depends on US1 complete)
```

#### 4. Testing Dependencies (if TDD)
```
Example: Tests must be written and fail BEFORE implementation
Task Order (RED-GREEN-REFACTOR):
  T010 [P] [US1] Write contract test for /users endpoint
  T011 [P] [US1] Write integration test for user creation
  [Verify tests FAIL - RED phase]
  T012 [P] [US1] Create User model
  T014 [US1] Implement UserService
  T015 [US1] Implement /users endpoint
  [Verify tests PASS - GREEN phase]
  T016 [US1] Refactor and optimize
  [Verify tests STILL PASS - REFACTOR phase]
```

### Minimizing Cross-Story Dependencies

**Goal:** User stories should be as independent as possible.

**Strategies:**

1. **Shared entities in Foundational phase:**
   ```
   If User model is needed by US1, US2, and US3:
   → Put User model in Phase 2: Foundational
   → All stories can then use it independently
   ```

2. **Feature flags for integration:**
   ```
   If US2 enhances US1 functionality:
   → US2 should work independently
   → Integration with US1 is optional enhancement
   → Use feature flags to enable/disable integration
   ```

3. **API contracts as boundaries:**
   ```
   If US2 calls US1's API:
   → Define API contract in Phase 2 or US1
   → US2 depends on contract, not implementation
   → Can mock US1 API for US2 testing
   ```

---

## Task Format Requirements

### Strict Format Enforcement

Every task MUST follow this exact format:

```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

### Component Breakdown

#### 1. Checkbox: `- [ ]`
- ALWAYS present
- Enables task tracking in markdown
- Can be checked off when complete

#### 2. Task ID: `[T###]`
- Sequential numbering: T001, T002, T003...
- Numbered in execution order
- Unique across entire tasks.md
- Makes dependencies explicit (e.g., "depends on T012")

#### 3. [P] Parallel Marker (OPTIONAL)
- Include ONLY if task can run in parallel
- Criteria for [P]:
  - Modifies different files than other [P] tasks in same phase
  - No dependencies on incomplete tasks
  - Can be started immediately (within its phase)
- Examples:
  - ✅ `T012 [P] [US1] Create User model in src/models/user.py`
  - ✅ `T013 [P] [US1] Create Post model in src/models/post.py`
  - ❌ `T014 [US1] Implement UserService (depends on T012, T013)` - NO [P], has dependencies

#### 4. [Story] Label (REQUIRED for user story phases)
- Format: [US1], [US2], [US3]... maps to user stories from spec.md
- **Setup phase:** NO story label
- **Foundational phase:** NO story label
- **User Story phases:** MUST have story label
- **Polish phase:** NO story label
- Purpose: Enables traceability from task → user story → requirements

#### 5. Description with File Path
- **Action verb:** Create, Implement, Configure, Add, Update...
- **What:** Specific component/feature
- **Where:** Exact file path
- **Examples:**
  - ✅ "Create User model in src/models/user.py"
  - ✅ "Implement authentication middleware in src/middleware/auth.py"
  - ✅ "Configure database connection in src/config/database.ts"
  - ❌ "Create models" (too vague, no file path)
  - ❌ "Implement user stuff" (too vague)

### Format Validation Checklist

When generating tasks, verify:
- [ ] Every task has checkbox `- [ ]`
- [ ] Every task has sequential Task ID (T001, T002...)
- [ ] [P] marker only on truly parallel tasks
- [ ] [Story] label on all user story phase tasks
- [ ] [Story] label NOT on Setup/Foundational/Polish phases
- [ ] Every task has clear action verb
- [ ] Every task has exact file path
- [ ] No duplicate Task IDs
- [ ] Task IDs are in execution order

---

## Phase Structure

### Phase 1: Setup (Shared Infrastructure)

**Duration:** Usually 3-10 tasks
**Parallelization:** High - most tasks can run in parallel

**Typical Tasks:**
```
- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools
- [ ] T004 [P] Setup build configuration
- [ ] T005 [P] Configure git hooks for code quality
```

**Completion Criteria:**
- Project structure exists
- Dependencies installed
- Basic tooling configured
- Ready for foundational work

### Phase 2: Foundational (Blocking Prerequisites)

**Duration:** Usually 5-15 tasks
**Parallelization:** Medium - some tasks parallelizable
**Criticality:** HIGH - blocks all user story work

**Typical Tasks:**
```
- [ ] T006 Setup database schema and migrations framework
- [ ] T007 [P] Implement authentication/authorization framework
- [ ] T008 [P] Setup API routing and middleware structure
- [ ] T009 Create base models/entities that all stories depend on
- [ ] T010 [P] Configure error handling and logging infrastructure
- [ ] T011 [P] Setup environment configuration management
```

**Discipline Required:**
- Only truly foundational items belong here
- If only one story needs it → put it in that story's phase
- If multiple stories need it → foundational
- Be conservative - when in doubt, put it in the story phase

**Completion Criteria:**
- All blocking infrastructure complete
- User story work can begin
- Multiple stories can start in parallel

**Checkpoint:**
```
**Checkpoint:** Foundation ready - user story implementation can now begin in parallel
```

### Phase 3+: User Story Phases

**One phase per user story, ordered by priority**

Each user story phase should follow this structure:

```markdown
## Phase N: User Story X - [Title] (Priority: PX)

**Goal:** [Brief description of what this story delivers]

**Acceptance Criteria:** [From spec.md]

**Independent Test:** [How to verify this story works on its own]

### Tests for User Story X (if TDD requested)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T0XX [P] [USX] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T0XX [P] [USX] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story X

- [ ] T0XX [P] [USX] Create [Entity1] model in src/models/[entity1].py
- [ ] T0XX [P] [USX] Create [Entity2] model in src/models/[entity2].py
- [ ] T0XX [USX] Implement [Service] in src/services/[service].py (depends on models)
- [ ] T0XX [USX] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T0XX [USX] Add validation and error handling
- [ ] T0XX [USX] Add logging for user story operations

**Checkpoint:** At this point, User Story X should be fully functional and testable independently
```

**Within-Story Task Order:**
1. **Tests first** (if TDD) - Write and verify they FAIL
2. **Models** - Data layer
3. **Services** - Business logic layer
4. **Endpoints/UI** - Presentation layer
5. **Integration** - Connect components
6. **Validation** - Error handling
7. **Logging** - Observability

### Final Phase: Polish & Cross-Cutting Concerns

**Duration:** Usually 5-10 tasks
**Parallelization:** High - most tasks can run in parallel
**Timing:** After all desired user stories complete

**Typical Tasks:**
```
- [ ] T0XX [P] Documentation updates in docs/
- [ ] T0XX Code cleanup and refactoring
- [ ] T0XX Performance optimization across all stories
- [ ] T0XX [P] Additional unit tests (if requested) in tests/unit/
- [ ] T0XX Security hardening
- [ ] T0XX Run quickstart.md validation
```

---

## Parallel Execution Markers

### When to Use [P]

Mark a task with [P] if ALL of these are true:
1. **Different files:** Task modifies different files than other [P] tasks in same phase
2. **No dependencies:** Task doesn't depend on other incomplete tasks in same phase
3. **Can start immediately:** Task can begin as soon as its phase starts

### Parallel Opportunities by Phase

#### Setup Phase
**High parallelization:** Most setup tasks are independent
```
- [ ] T001 Create project structure
- [ ] T002 [P] Install dependencies
- [ ] T003 [P] Configure linting
- [ ] T004 [P] Setup build tools
```

#### Foundational Phase
**Medium parallelization:** Some infrastructure tasks are independent
```
- [ ] T006 Setup database schema (must be first)
- [ ] T007 [P] Implement authentication (independent of T006)
- [ ] T008 [P] Setup API routing (independent of T006, T007)
- [ ] T009 Create base models (depends on T006)
```

#### User Story Phases
**High parallelization within story:** Different models/services/endpoints
```
### Tests (if TDD)
- [ ] T010 [P] [US1] Contract test A
- [ ] T011 [P] [US1] Contract test B

### Models
- [ ] T012 [P] [US1] Create User model
- [ ] T013 [P] [US1] Create Profile model

### Services (depend on models)
- [ ] T014 [US1] Implement UserService (depends on T012, T013)

### Endpoints (depend on services)
- [ ] T015 [US1] Implement /users endpoint (depends on T014)
```

**High parallelization across stories:** Different stories can run in parallel
```
Once Foundational phase completes:
- Story 1: Developer A
- Story 2: Developer B
- Story 3: Developer C
All can work in parallel!
```

### Parallel Execution Examples Section

Include a practical example in every tasks.md:

```markdown
## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if TDD):
Task: "Contract test for /users endpoint in tests/contract/test_users.py"
Task: "Integration test for user creation in tests/integration/test_user_creation.py"

# Launch all models for User Story 1 together:
Task: "Create User model in src/models/user.py"
Task: "Create Profile model in src/models/profile.py"
```

This helps implementers understand parallelization opportunities.

---

## TDD Integration

### When TDD is Requested

If spec.md or plan.md request TDD (Test-Driven Development), integrate it into task structure:

#### RED-GREEN-REFACTOR Cycle

For each user story:

**🔴 RED Phase: Write Failing Tests**
```
- [ ] T010 [P] [US1] Write contract test for /users endpoint
  → Run test → Verify it FAILS (proves test works)
- [ ] T011 [P] [US1] Write integration test for user creation
  → Run test → Verify it FAILS
```

**🟢 GREEN Phase: Implement Minimal Code**
```
- [ ] T012 [P] [US1] Create User model in src/models/user.py
- [ ] T013 [US1] Implement UserService in src/services/user_service.py
- [ ] T014 [US1] Implement /users endpoint in src/api/users.py
  → Run tests → Verify they PASS
```

**🔵 REFACTOR Phase: Clean Up**
```
- [ ] T015 [US1] Refactor UserService for clarity
- [ ] T016 [US1] Optimize User model queries
  → Run tests → Verify they STILL PASS
```

### Test Task Format

Test tasks should specify:
- **Test type:** Contract, integration, unit, E2E
- **What's being tested:** Endpoint, user journey, function
- **File path:** Exact test file location

**Examples:**
```
- [ ] T010 [P] [US1] Contract test for POST /users endpoint in tests/contract/test_users_create.py
- [ ] T011 [P] [US1] Integration test for user registration flow in tests/integration/test_registration.py
- [ ] T012 [P] [US1] Unit test for password hashing in tests/unit/test_password_utils.py
```

### Test Independence

Tests should be parallelizable:
- Different test files can run simultaneously
- Tests don't depend on each other
- Tests use isolated test data
- Tests clean up after themselves

---

## Constitution Integration

### Reading Constitution Before Task Generation

**ALWAYS read constitution.md before generating tasks:**
```
File: .shipkit/skills/dev-constitution/outputs/constitution.md
```

### Constitution Influences on Tasks

#### 1. File Structure
Constitution defines project structure → tasks use correct paths
```
Constitution says: "Backend: src/, Frontend: client/"
Tasks use:
  - [ ] T012 [US1] Create User model in src/models/user.py
  - [ ] T013 [US1] Create LoginForm in client/components/LoginForm.tsx
```

#### 2. Testing Requirements
Constitution defines test coverage → tasks include appropriate tests
```
Constitution says: "Minimum 80% coverage, TDD required"
Tasks include:
  - Tests BEFORE implementation
  - Contract tests for all endpoints
  - Integration tests for critical flows
```

#### 3. Architectural Patterns
Constitution defines patterns → tasks follow those patterns
```
Constitution says: "Repository pattern for data access"
Tasks include:
  - [ ] T012 [US1] Create UserRepository in src/repositories/user_repository.py
  - [ ] T013 [US1] Implement UserService using UserRepository
```

#### 4. Naming Conventions
Constitution defines conventions → task descriptions use them
```
Constitution says: "PascalCase for classes, camelCase for functions"
Tasks specify:
  - [ ] T012 [US1] Create UserModel class in src/models/UserModel.py
  - [ ] T013 [US1] Implement getUserById() in src/services/userService.py
```

### Constitution Compliance Section

Every tasks.md should include:

```markdown
## Constitution Compliance

All tasks follow patterns established in:
- **File:** `.shipkit/skills/dev-constitution/outputs/constitution.md`
- **Coding Standards:** [Reference specific sections, e.g., "Section 4.1: Naming Conventions"]
- **Testing Requirements:** [Reference specific sections, e.g., "Section 5.2: Test Coverage"]
- **Architectural Patterns:** [Reference specific sections, e.g., "Section 2.3: Repository Pattern"]
```

---

## Common Patterns

### Pattern 1: CRUD Resource

When implementing a CRUD resource for a user story:

```
Phase N: User Story X - [CRUD Resource Name]

Tests (if TDD):
- [ ] T0XX [P] [USX] Contract test for POST /resource
- [ ] T0XX [P] [USX] Contract test for GET /resource/:id
- [ ] T0XX [P] [USX] Contract test for PUT /resource/:id
- [ ] T0XX [P] [USX] Contract test for DELETE /resource/:id

Models:
- [ ] T0XX [USX] Create Resource model in src/models/resource.py

Services:
- [ ] T0XX [USX] Implement ResourceService CRUD methods in src/services/resource_service.py

Endpoints:
- [ ] T0XX [P] [USX] Implement POST /resource endpoint
- [ ] T0XX [P] [USX] Implement GET /resource/:id endpoint
- [ ] T0XX [P] [USX] Implement PUT /resource/:id endpoint
- [ ] T0XX [P] [USX] Implement DELETE /resource/:id endpoint

Validation:
- [ ] T0XX [USX] Add input validation for Resource
- [ ] T0XX [USX] Add authorization checks for Resource endpoints
```

### Pattern 2: Integration Feature

When implementing integration with external service:

```
Phase N: User Story X - [External Service Integration]

Setup:
- [ ] T0XX [P] [USX] Install [service] SDK/client library
- [ ] T0XX [P] [USX] Configure [service] credentials in environment

Wrapper:
- [ ] T0XX [USX] Create [Service]Client wrapper in src/clients/[service]_client.py
- [ ] T0XX [USX] Implement error handling for [service] API

Tests (if TDD):
- [ ] T0XX [P] [USX] Mock test for [service] client in tests/unit/test_[service]_client.py
- [ ] T0XX [P] [USX] Integration test for [service] workflow

Integration:
- [ ] T0XX [USX] Integrate [service] client with existing service layer
- [ ] T0XX [USX] Add [service] logging and monitoring
```

### Pattern 3: Database Migration

When database schema changes are needed:

```
Phase N: User Story X - [Feature Name]

Database:
- [ ] T0XX [USX] Create migration for [entity] table in migrations/YYYYMMDD_create_[entity].sql
- [ ] T0XX [USX] Add indexes for [entity] queries

Models (depend on migration):
- [ ] T0XX [P] [USX] Create [Entity] model in src/models/[entity].py
```

### Pattern 4: Frontend Component

When implementing UI component:

```
Phase N: User Story X - [UI Feature]

Components:
- [ ] T0XX [P] [USX] Create [Component] in client/components/[Component].tsx
- [ ] T0XX [P] [USX] Create [Component]Styles in client/styles/[Component].module.css

State Management:
- [ ] T0XX [USX] Create [feature] slice in client/store/[feature]Slice.ts
- [ ] T0XX [USX] Implement [feature] API calls in client/api/[feature]Api.ts

Tests (if TDD):
- [ ] T0XX [P] [USX] Component test for [Component] in client/__tests__/[Component].test.tsx
- [ ] T0XX [P] [USX] Integration test for [user flow] in client/__tests__/integration/[flow].test.tsx
```

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Layer-Based Organization

**WRONG:**
```
Phase 1: All Models
Phase 2: All Services
Phase 3: All Endpoints
```

**Why it's wrong:**
- Can't test user stories independently
- Can't deliver incrementally
- Can't parallelize effectively
- No clear MVP

**RIGHT:**
```
Phase 1: Setup
Phase 2: Foundational
Phase 3: User Story 1 (models + services + endpoints)
Phase 4: User Story 2 (models + services + endpoints)
```

### ❌ Anti-Pattern 2: Vague Tasks

**WRONG:**
```
- [ ] T001 Create models
- [ ] T002 Implement services
- [ ] T003 Add endpoints
```

**Why it's wrong:**
- Not specific enough for immediate execution
- No file paths
- No story labels
- Unclear scope

**RIGHT:**
```
- [ ] T012 [P] [US1] Create User model in src/models/user.py
- [ ] T013 [P] [US1] Create Profile model in src/models/profile.py
- [ ] T014 [US1] Implement UserService in src/services/user_service.py
```

### ❌ Anti-Pattern 3: Missing Dependencies

**WRONG:**
```
- [ ] T014 [P] [US1] Implement UserService
- [ ] T012 [P] [US1] Create User model
```

**Why it's wrong:**
- Task order doesn't respect dependencies
- UserService depends on User model
- Both marked [P] but T014 can't start until T012 is done

**RIGHT:**
```
- [ ] T012 [P] [US1] Create User model in src/models/user.py
- [ ] T014 [US1] Implement UserService in src/services/user_service.py (depends on T012)
```

### ❌ Anti-Pattern 4: Everything in Foundational

**WRONG:**
```
Phase 2: Foundational
- [ ] T006 Setup database
- [ ] T007 Implement auth
- [ ] T008 Create User model
- [ ] T009 Create Post model
- [ ] T010 Create Comment model
- [ ] T011 Implement UserService
- [ ] T012 Implement PostService
```

**Why it's wrong:**
- Models and services belong to specific user stories
- Delays user story work unnecessarily
- Reduces parallelization opportunities

**RIGHT:**
```
Phase 2: Foundational
- [ ] T006 Setup database schema framework
- [ ] T007 Implement authentication framework
(Only truly shared infrastructure)

Phase 3: User Story 1 - User Management
- [ ] T008 [US1] Create User model
- [ ] T009 [US1] Implement UserService

Phase 4: User Story 2 - Posts
- [ ] T010 [US2] Create Post model
- [ ] T011 [US2] Implement PostService
```

### ❌ Anti-Pattern 5: Cross-Story Coupling

**WRONG:**
```
Phase 3: User Story 1
- [ ] T012 [US1] Create shared Comment model for US1 and US2

Phase 4: User Story 2
- [ ] T020 [US2] Use Comment model from US1 (depends on US1)
```

**Why it's wrong:**
- US2 can't start until US1 is complete
- Violates independence principle
- Can't parallelize stories

**RIGHT:**
```
Phase 2: Foundational
- [ ] T009 Create shared Comment model in src/models/comment.py

Phase 3: User Story 1
- [ ] T012 [US1] Use Comment model (independent)

Phase 4: User Story 2
- [ ] T020 [US2] Use Comment model (independent)
```

### ❌ Anti-Pattern 6: Missing [Story] Labels

**WRONG:**
```
Phase 3: User Story 1
- [ ] T012 Create User model
- [ ] T013 Implement UserService
```

**Why it's wrong:**
- No traceability to user story
- Hard to track story completion
- Can't generate story-based metrics

**RIGHT:**
```
Phase 3: User Story 1
- [ ] T012 [P] [US1] Create User model in src/models/user.py
- [ ] T013 [US1] Implement UserService in src/services/user_service.py
```

---

## Validation Checklist

Before finalizing tasks.md, verify:

### Structure
- [ ] Phase 1: Setup exists
- [ ] Phase 2: Foundational exists
- [ ] One phase per user story from spec.md
- [ ] Final phase: Polish & Cross-Cutting Concerns
- [ ] Phases ordered by user story priority (P1, P2, P3...)

### Task Format
- [ ] Every task has checkbox `- [ ]`
- [ ] Every task has sequential Task ID (T001, T002...)
- [ ] [P] marker only on truly parallel tasks
- [ ] [Story] label on all user story phase tasks
- [ ] Every task has clear action verb
- [ ] Every task has exact file path

### Dependencies
- [ ] Task IDs in execution order
- [ ] Dependencies section shows phase relationships
- [ ] Dependencies section shows story relationships
- [ ] No circular dependencies

### TDD (if requested)
- [ ] Test tasks before implementation tasks
- [ ] Tests marked as "Write FIRST, verify FAIL"
- [ ] RED-GREEN-REFACTOR cycle clear

### Constitution
- [ ] File paths match constitution structure
- [ ] Naming conventions follow constitution
- [ ] Testing strategy matches constitution
- [ ] Architectural patterns follow constitution

### Completeness
- [ ] All user stories from spec.md have phases
- [ ] All entities from data-model.md have tasks
- [ ] All endpoints from contracts/ have tasks
- [ ] All research decisions from research.md reflected in tasks

### Independence
- [ ] Each user story can be tested independently
- [ ] Cross-story dependencies minimized
- [ ] Shared dependencies in Foundational phase
- [ ] Clear MVP path (User Story 1 only)

---

## Final Notes

The dev-tasks skill transforms planning artifacts (spec.md, plan.md) into executable work. Good tasks enable:

1. **Clear execution:** Anyone can pick up a task and complete it
2. **Parallel work:** Multiple developers can work without conflicts
3. **Incremental delivery:** Ship User Story 1, then 2, then 3
4. **Independent testing:** Validate each story separately
5. **Clear progress tracking:** Task checkboxes show completion

Keep tasks LEAN, SPECIFIC, and INDEPENDENT. When in doubt, err on the side of smaller, more focused tasks.

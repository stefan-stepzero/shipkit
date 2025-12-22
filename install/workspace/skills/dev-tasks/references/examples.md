# Dev-Tasks Examples

**Purpose:** Concrete examples of well-structured task breakdowns for different types of features.

**Last Updated:** 2025-12-22

---

## Example 1: User Authentication Feature (Full TDD)

**Context:**
- Feature: Add user authentication
- Tech stack: Node.js, Express, PostgreSQL, JWT
- TDD requested: Yes
- User stories: 3 (Registration, Login, Password Reset)

### Generated Tasks

```markdown
# Tasks: User Authentication

**Created:** 2025-12-22
**Feature:** 001-user-authentication
**Input Documents:** spec.md, plan.md, constitution.md

---

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Node.js project with Express dependencies
- [ ] T003 [P] Configure ESLint and Prettier
- [ ] T004 [P] Setup TypeScript configuration
- [ ] T005 [P] Configure git hooks for code quality

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose:** Core infrastructure that MUST be complete before ANY user story

- [ ] T006 Setup PostgreSQL database and Prisma ORM
- [ ] T007 Create database migration framework
- [ ] T008 [P] Implement JWT token generation/validation utility
- [ ] T009 [P] Setup Express middleware (CORS, body parser, helmet)
- [ ] T010 [P] Configure environment variables (.env setup)
- [ ] T011 [P] Implement error handling middleware
- [ ] T012 [P] Setup logging infrastructure (Winston)

**Checkpoint:** Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal:** Users can create accounts with email and password

**Acceptance Criteria:**
- User can submit registration form with email, password, name
- System validates email format and password strength
- System stores hashed password (never plaintext)
- System returns JWT token upon successful registration
- System prevents duplicate email registration

**Independent Test:** POST /api/auth/register with valid data returns 201 and JWT token

### Tests for User Story 1 (TDD - Write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Contract test for POST /api/auth/register in tests/contract/auth.register.test.ts
- [ ] T014 [P] [US1] Integration test for registration flow in tests/integration/registration.test.ts
- [ ] T015 [P] [US1] Unit test for password hashing in tests/unit/password.utils.test.ts
- [ ] T016 [P] [US1] Unit test for email validation in tests/unit/email.validator.test.ts

**Verify all tests FAIL (🔴 RED phase)**

### Implementation for User Story 1

- [ ] T017 [P] [US1] Create User model with Prisma schema in prisma/schema.prisma
- [ ] T018 [US1] Run migration to create users table
- [ ] T019 [P] [US1] Implement password hashing utility in src/utils/password.ts
- [ ] T020 [P] [US1] Implement email validation utility in src/utils/email-validator.ts
- [ ] T021 [US1] Implement UserRepository in src/repositories/user.repository.ts
- [ ] T022 [US1] Implement AuthService.register() in src/services/auth.service.ts
- [ ] T023 [US1] Implement POST /api/auth/register endpoint in src/routes/auth.routes.ts
- [ ] T024 [US1] Add validation middleware for registration in src/middleware/validators/auth.validator.ts
- [ ] T025 [US1] Add logging for registration events

**Verify all tests PASS (🟢 GREEN phase)**

- [ ] T026 [US1] Refactor AuthService for clarity and error handling
- [ ] T027 [US1] Optimize User model queries with indexes

**Verify tests STILL PASS (🔵 REFACTOR phase)**

**Checkpoint:** User registration is fully functional and testable independently

---

## Phase 4: User Story 2 - User Login (Priority: P2)

**Goal:** Users can log in with email and password

**Acceptance Criteria:**
- User can submit login form with email and password
- System validates credentials
- System returns JWT token upon successful login
- System returns 401 for invalid credentials
- System implements rate limiting (5 attempts per 15 minutes)

**Independent Test:** POST /api/auth/login with valid credentials returns 200 and JWT token

### Tests for User Story 2 (TDD - Write FIRST)

- [ ] T028 [P] [US2] Contract test for POST /api/auth/login in tests/contract/auth.login.test.ts
- [ ] T029 [P] [US2] Integration test for login flow in tests/integration/login.test.ts
- [ ] T030 [P] [US2] Unit test for password comparison in tests/unit/password.utils.test.ts

**Verify tests FAIL (🔴 RED phase)**

### Implementation for User Story 2

- [ ] T031 [P] [US2] Implement password comparison utility in src/utils/password.ts
- [ ] T032 [P] [US2] Implement rate limiting middleware in src/middleware/rate-limit.ts
- [ ] T033 [US2] Implement AuthService.login() in src/services/auth.service.ts
- [ ] T034 [US2] Implement POST /api/auth/login endpoint in src/routes/auth.routes.ts
- [ ] T035 [US2] Add validation middleware for login
- [ ] T036 [US2] Add logging for login events (success and failure)

**Verify tests PASS (🟢 GREEN phase)**

- [ ] T037 [US2] Refactor error messages for security (avoid revealing if email exists)

**Verify tests STILL PASS (🔵 REFACTOR phase)**

**Checkpoint:** User login is fully functional alongside registration

---

## Phase 5: User Story 3 - Password Reset (Priority: P3)

**Goal:** Users can reset forgotten passwords via email

**Acceptance Criteria:**
- User can request password reset with email
- System sends reset token via email
- User can submit new password with valid token
- Reset tokens expire after 1 hour
- Tokens are single-use only

**Independent Test:** POST /api/auth/forgot-password sends email with reset token

### Tests for User Story 3 (TDD - Write FIRST)

- [ ] T038 [P] [US3] Contract test for POST /api/auth/forgot-password in tests/contract/auth.forgot.test.ts
- [ ] T039 [P] [US3] Contract test for POST /api/auth/reset-password in tests/contract/auth.reset.test.ts
- [ ] T040 [P] [US3] Integration test for password reset flow in tests/integration/password-reset.test.ts

**Verify tests FAIL (🔴 RED phase)**

### Implementation for User Story 3

- [ ] T041 [US3] Add resetToken and resetTokenExpiry fields to User model in prisma/schema.prisma
- [ ] T042 [US3] Run migration to add reset token fields
- [ ] T043 [P] [US3] Implement token generation utility in src/utils/token.ts
- [ ] T044 [P] [US3] Implement email service (SendGrid integration) in src/services/email.service.ts
- [ ] T045 [US3] Implement AuthService.forgotPassword() in src/services/auth.service.ts
- [ ] T046 [US3] Implement AuthService.resetPassword() in src/services/auth.service.ts
- [ ] T047 [US3] Implement POST /api/auth/forgot-password endpoint
- [ ] T048 [US3] Implement POST /api/auth/reset-password endpoint
- [ ] T049 [US3] Add validation for password reset requests
- [ ] T050 [US3] Add logging for password reset events

**Verify tests PASS (🟢 GREEN phase)**

- [ ] T051 [US3] Refactor email templates for better UX

**Verify tests STILL PASS (🔵 REFACTOR phase)**

**Checkpoint:** All authentication user stories are complete and independent

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T052 [P] API documentation (OpenAPI/Swagger) in docs/api/auth.yaml
- [ ] T053 [P] README with setup instructions in README.md
- [ ] T054 Security audit of authentication flow
- [ ] T055 Performance testing for auth endpoints
- [ ] T056 [P] Additional unit tests for edge cases
- [ ] T057 Code cleanup and refactoring across all auth code

---

## Dependencies & Execution Order

### Phase Dependencies
- Setup (Phase 1): No dependencies
- Foundational (Phase 2): Depends on Setup complete
- US1, US2, US3 (Phase 3-5): All depend on Foundational complete
  - Stories can run in parallel OR sequentially in priority order
- Polish (Phase 6): Depends on desired stories complete

### User Story Dependencies
- User Story 1: Independent (only depends on Foundational)
- User Story 2: Independent (only depends on Foundational)
- User Story 3: Independent (only depends on Foundational)

### Parallel Opportunities
- All Setup tasks (T002-T005) can run in parallel
- Foundational tasks T008-T012 can run in parallel
- US1 tests T013-T016 can run in parallel
- US1 implementation T017, T019, T020 can run in parallel
- Once Foundational complete: US1, US2, US3 can all start in parallel if team capacity allows

---

## Implementation Strategy

### MVP First (US1 Only)
1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T012)
3. Complete Phase 3: User Story 1 (T013-T027)
4. **STOP and VALIDATE:** Test registration independently
5. Deploy MVP with just registration

### Incremental Delivery
1. Setup + Foundational → Infrastructure ready
2. Add US1 → Registration works → Deploy MVP
3. Add US2 → Login works → Deploy
4. Add US3 → Password reset works → Deploy
```

**Key Features of This Example:**
- ✅ User story organization
- ✅ TDD with RED-GREEN-REFACTOR
- ✅ Clear dependencies
- ✅ [P] parallel markers
- ✅ [Story] labels
- ✅ File paths in every task
- ✅ Independent test criteria per story
- ✅ Checkpoints after each story

---

## Example 2: REST API for Task Management (No TDD)

**Context:**
- Feature: Task management CRUD API
- Tech stack: Python, FastAPI, PostgreSQL
- TDD requested: No (tests optional)
- User stories: 2 (Task CRUD, Task Assignment)

### Generated Tasks

```markdown
# Tasks: Task Management API

**Created:** 2025-12-22
**Feature:** 002-task-management-api
**Input Documents:** spec.md, plan.md, constitution.md

---

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python project with FastAPI and dependencies (requirements.txt)
- [ ] T003 [P] Configure Black and Flake8
- [ ] T004 [P] Setup pytest configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T005 Setup PostgreSQL database and SQLAlchemy ORM
- [ ] T006 Create Alembic migration framework
- [ ] T007 [P] Implement database connection management in src/db/connection.py
- [ ] T008 [P] Setup FastAPI application structure in src/main.py
- [ ] T009 [P] Implement error handling middleware
- [ ] T010 [P] Configure CORS and security headers

**Checkpoint:** Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Task CRUD Operations (Priority: P1) 🎯 MVP

**Goal:** Users can create, read, update, and delete tasks

**Acceptance Criteria:**
- User can create task with title, description, status, due_date
- User can retrieve single task by ID
- User can list all tasks with pagination
- User can update task fields
- User can delete task
- All endpoints validate input

**Independent Test:** POST /api/tasks creates task, GET /api/tasks/:id retrieves it

### Implementation for User Story 1

- [ ] T011 [US1] Create Task model in src/models/task.py
- [ ] T012 [US1] Create Alembic migration for tasks table in migrations/001_create_tasks.py
- [ ] T013 [US1] Run migration to create tasks table
- [ ] T014 [P] [US1] Implement TaskRepository.create() in src/repositories/task_repository.py
- [ ] T015 [P] [US1] Implement TaskRepository.get_by_id() in src/repositories/task_repository.py
- [ ] T016 [P] [US1] Implement TaskRepository.list() in src/repositories/task_repository.py
- [ ] T017 [P] [US1] Implement TaskRepository.update() in src/repositories/task_repository.py
- [ ] T018 [P] [US1] Implement TaskRepository.delete() in src/repositories/task_repository.py
- [ ] T019 [US1] Implement TaskService with CRUD methods in src/services/task_service.py
- [ ] T020 [P] [US1] Implement POST /api/tasks endpoint in src/routes/tasks.py
- [ ] T021 [P] [US1] Implement GET /api/tasks/:id endpoint in src/routes/tasks.py
- [ ] T022 [P] [US1] Implement GET /api/tasks endpoint (list) in src/routes/tasks.py
- [ ] T023 [P] [US1] Implement PUT /api/tasks/:id endpoint in src/routes/tasks.py
- [ ] T024 [P] [US1] Implement DELETE /api/tasks/:id endpoint in src/routes/tasks.py
- [ ] T025 [US1] Add Pydantic schemas for validation in src/schemas/task.py
- [ ] T026 [US1] Add pagination helper in src/utils/pagination.py
- [ ] T027 [US1] Add logging for task operations

**Checkpoint:** Task CRUD is fully functional

---

## Phase 4: User Story 2 - Task Assignment (Priority: P2)

**Goal:** Tasks can be assigned to users

**Acceptance Criteria:**
- Tasks have assignee_id field
- User can assign task to user
- User can unassign task
- User can filter tasks by assignee
- System validates assignee exists

**Independent Test:** PUT /api/tasks/:id/assign with valid user_id assigns task

### Implementation for User Story 2

- [ ] T028 [US2] Add assignee_id field to Task model in src/models/task.py
- [ ] T029 [US2] Create Alembic migration to add assignee_id in migrations/002_add_assignee.py
- [ ] T030 [US2] Run migration to add assignee_id column
- [ ] T031 [P] [US2] Implement TaskRepository.assign() in src/repositories/task_repository.py
- [ ] T032 [P] [US2] Implement TaskRepository.filter_by_assignee() in src/repositories/task_repository.py
- [ ] T033 [US2] Implement TaskService.assign() and validate user exists
- [ ] T034 [US2] Implement PUT /api/tasks/:id/assign endpoint in src/routes/tasks.py
- [ ] T035 [US2] Implement PUT /api/tasks/:id/unassign endpoint in src/routes/tasks.py
- [ ] T036 [US2] Add assignee filter to GET /api/tasks endpoint
- [ ] T037 [US2] Add validation for assignee_id in schemas
- [ ] T038 [US2] Add logging for assignment operations

**Checkpoint:** Task assignment is fully functional alongside CRUD

---

## Phase 5: Polish & Cross-Cutting Concerns

- [ ] T039 [P] OpenAPI documentation in docs/openapi.yaml
- [ ] T040 [P] README with API examples
- [ ] T041 Add indexes for task queries (status, assignee_id, due_date)
- [ ] T042 [P] Optional unit tests for TaskService in tests/unit/test_task_service.py
- [ ] T043 Performance optimization for task listing
- [ ] T044 Security review of endpoints

---

## Dependencies & Execution Order

### Phase Dependencies
- Setup (Phase 1): No dependencies
- Foundational (Phase 2): Depends on Setup
- US1, US2 (Phase 3-4): Depend on Foundational
- Polish (Phase 5): Depends on US1, US2

### User Story Dependencies
- User Story 1: Independent
- User Story 2: Independent (can run in parallel with US1 if team capacity)

### Parallel Opportunities
- Setup tasks T002-T004 can run in parallel
- Foundational tasks T007-T010 can run in parallel
- US1 repository methods T014-T018 can run in parallel
- US1 endpoints T020-T024 can run in parallel
- US2 repository methods T031-T032 can run in parallel
```

**Key Features of This Example:**
- ✅ No TDD (tests optional in Polish phase)
- ✅ CRUD pattern clearly shown
- ✅ Database migrations integrated into tasks
- ✅ Repository pattern followed
- ✅ Good parallelization opportunities

---

## Example 3: Frontend Feature with Backend Integration

**Context:**
- Feature: User profile management
- Tech stack: React (frontend), Node.js/Express (backend)
- TDD requested: No
- User stories: 2 (View Profile, Edit Profile)

### Generated Tasks (Abbreviated)

```markdown
# Tasks: User Profile Management

---

## Phase 1: Setup

- [ ] T001 Create project structure (frontend/, backend/)
- [ ] T002 [P] Initialize React app in frontend/
- [ ] T003 [P] Initialize Express app in backend/
- [ ] T004 [P] Configure TypeScript for frontend
- [ ] T005 [P] Configure TypeScript for backend

---

## Phase 2: Foundational

- [ ] T006 Setup database and User model in backend/src/models/user.model.ts
- [ ] T007 [P] Setup React Router in frontend/src/App.tsx
- [ ] T008 [P] Setup Axios API client in frontend/src/api/client.ts
- [ ] T009 [P] Implement CORS for frontend-backend communication in backend/src/middleware/cors.ts

**Checkpoint:** Foundation ready

---

## Phase 3: User Story 1 - View Profile (Priority: P1) 🎯 MVP

**Goal:** User can view their profile information

**Independent Test:** Navigate to /profile, see name, email, bio

### Backend for User Story 1

- [ ] T010 [P] [US1] Implement UserRepository.getById() in backend/src/repositories/user.repository.ts
- [ ] T011 [US1] Implement UserService.getProfile() in backend/src/services/user.service.ts
- [ ] T012 [US1] Implement GET /api/users/me endpoint in backend/src/routes/user.routes.ts

### Frontend for User Story 1

- [ ] T013 [P] [US1] Create ProfilePage component in frontend/src/pages/ProfilePage.tsx
- [ ] T014 [P] [US1] Create ProfileView component in frontend/src/components/ProfileView.tsx
- [ ] T015 [US1] Implement fetchProfile() API call in frontend/src/api/userApi.ts
- [ ] T016 [US1] Add /profile route to React Router
- [ ] T017 [US1] Add loading and error states to ProfilePage

**Checkpoint:** User can view profile

---

## Phase 4: User Story 2 - Edit Profile (Priority: P2)

**Goal:** User can edit name, email, bio

**Independent Test:** Click Edit, change name, save, see updated name

### Backend for User Story 2

- [ ] T018 [P] [US2] Implement UserRepository.update() in backend/src/repositories/user.repository.ts
- [ ] T019 [US2] Implement UserService.updateProfile() in backend/src/services/user.service.ts
- [ ] T020 [US2] Implement PUT /api/users/me endpoint in backend/src/routes/user.routes.ts
- [ ] T021 [US2] Add validation for profile updates

### Frontend for User Story 2

- [ ] T022 [P] [US2] Create ProfileEditForm component in frontend/src/components/ProfileEditForm.tsx
- [ ] T023 [US2] Implement updateProfile() API call in frontend/src/api/userApi.ts
- [ ] T024 [US2] Add edit mode toggle to ProfilePage
- [ ] T025 [US2] Add form validation for name, email, bio
- [ ] T026 [US2] Add success/error notifications

**Checkpoint:** User can edit profile

---

## Phase 5: Polish

- [ ] T027 [P] Add profile picture upload (backend endpoint)
- [ ] T028 [P] Add profile picture upload (frontend UI)
- [ ] T029 [P] Unit tests for UserService
- [ ] T030 [P] Component tests for ProfilePage
```

**Key Features of This Example:**
- ✅ Frontend + Backend tasks clearly separated
- ✅ Still organized by user story (not "all backend, then all frontend")
- ✅ Integration points clear
- ✅ Independent testing possible

---

## Example 4: Minimal Feature (Single User Story)

**Context:**
- Feature: Export data to CSV
- Tech stack: Python, Flask
- TDD requested: No
- User stories: 1 (Export CSV)

### Generated Tasks

```markdown
# Tasks: Export Data to CSV

---

## Phase 1: Setup

- [ ] T001 Install csv library (already in Python stdlib)
- [ ] T002 Create export module structure in src/export/

---

## Phase 2: Foundational

(No foundational tasks - feature is self-contained)

**Checkpoint:** Ready for implementation

---

## Phase 3: User Story 1 - Export CSV (Priority: P1) 🎯 MVP

**Goal:** User can export their data as CSV file

**Independent Test:** Click Export, download CSV, open in Excel, see data

### Implementation

- [ ] T003 [P] [US1] Implement CSVExporter class in src/export/csv_exporter.py
- [ ] T004 [P] [US1] Implement DataFormatter utility in src/export/data_formatter.py
- [ ] T005 [US1] Implement ExportService.generateCSV() in src/services/export_service.py
- [ ] T006 [US1] Implement GET /api/export/csv endpoint in src/routes/export.py
- [ ] T007 [US1] Add proper CSV headers and encoding (UTF-8 BOM for Excel)
- [ ] T008 [US1] Add logging for export operations

**Checkpoint:** CSV export works

---

## Phase 4: Polish

- [ ] T009 [P] Add optional unit tests
- [ ] T010 Add export rate limiting (prevent abuse)

---

## Dependencies & Execution Order

- Setup → Foundational (empty) → US1 → Polish
- US1 tasks T003-T004 can run in parallel
```

**Key Features of This Example:**
- ✅ Simple feature, simple structure
- ✅ Empty Foundational phase (not all features need it)
- ✅ Still follows format for consistency
- ✅ Can be MVP with just US1

---

## Summary: What Makes a Good Task Breakdown

Across all examples, notice the patterns:

1. **User Story Organization:** Tasks grouped by story, not layer
2. **Clear Format:** `- [ ] [TaskID] [P?] [Story?] Description with file path`
3. **Explicit Dependencies:** Task order respects dependencies
4. **Parallel Markers:** [P] on truly independent tasks
5. **Story Labels:** [US1], [US2], [US3] for traceability
6. **Independent Testing:** Each story can be validated separately
7. **Incremental Delivery:** MVP = Setup + Foundational + US1
8. **Constitution Alignment:** File paths, patterns match constitution
9. **TDD Integration:** When requested, tests BEFORE implementation
10. **Clear Checkpoints:** Validation points after each story

Use these examples as templates when generating tasks for similar feature types.

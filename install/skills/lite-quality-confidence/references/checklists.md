# Quality Confidence Checklists

Complete checklists for scanning implementation files before shipping.

---

## UI Component Checklist

**Apply to**: `.tsx`, `.jsx` files with UI components

### Loading States
**Why**: Users need feedback during async operations

**Patterns to search**:
- `isLoading|isPending|loading|pending` (state variables)
- `<Spinner|<Skeleton|<Loading|loading=` (UI indicators)
- `disabled={.*loading|disabled={.*pending` (disabled buttons)

**Mark ✓ if**: At least 2 of 3 patterns found
**Mark ✗ if**: No loading state management

---

### Error Handling
**Why**: Users need to know when things go wrong

**Patterns to search**:
- `catch.*toast|catch.*alert|catch.*setError` (error display)
- `ErrorBoundary|error-boundary` (React error boundaries)
- `toast\.error|alert\(.*error` (user-facing error messages)

**Mark ✓ if**: Catch blocks with user-facing error display
**Mark ✗ if**: No error handling or silent failures

---

### Success Feedback
**Why**: Users need confirmation that actions succeeded

**Patterns to search**:
- `toast\.success|alert.*success|setSuccess` (success messages)
- `checkmark|check-circle|success-icon` (visual indicators)

**Mark ✓ if**: Success message or visual indicator found
**Mark ✗ if**: No success feedback

---

### Accessibility
**Why**: Users with disabilities need equal access

**Patterns to search**:
- `aria-label|aria-labelledby|aria-describedby` (screen reader labels)
- `onKeyDown|onKeyPress|onKeyUp` (keyboard support)
- `tabIndex|role=` (focus management)
- `focus\(|blur\(` (programmatic focus)

**Mark ✓ if**: Interactive elements have aria-labels AND keyboard support
**Mark ✗ if**: Icon buttons lack labels OR no keyboard handling

---

### Empty States
**Why**: Handle cases where data is missing

**Patterns to search**:
- `if.*length === 0|if.*!.*length` (empty checks)
- `No.*found|No.*available|empty.*state` (empty messages)

**Mark ✓ if**: Conditional rendering for empty data
**Mark ✗ if**: No empty state handling

---

## API/Server Action Checklist

**Apply to**: `/api/`, `/actions/`, server-side `.ts` files

### Input Validation
**Why**: Prevent invalid data from entering the system

**Patterns to search**:
- `\.parse\(|\.safeParse\(|zod|Zod|z\.` (Zod validation)
- `typeof.*===|instanceof|Array\.isArray` (type checking)
- `validate|schema|Schema` (validation schemas)

**Mark ✓ if**: Zod schema validation OR explicit type checks
**Mark ✗ if**: No validation

---

### Auth Checks
**Why**: Ensure user is authenticated and authorized

**Patterns to search**:
- `getUser|getSession|auth\(|authenticate` (auth checks)
- `if.*!user|if.*!session|throw.*401|throw.*403` (auth enforcement)
- `role.*===|permission|can\(|authorize` (permission checks)

**Mark ✓ if**: User authentication AND ownership/permission checks
**Mark ⚠ if**: Authentication exists but no permission checks
**Mark ✗ if**: No auth checks

---

### Error Handling
**Why**: Gracefully handle failures

**Patterns to search**:
- `try.*catch|catch\s*\(` (try/catch blocks)
- `throw new Error|throw\s+\{` (proper error throwing)
- `status.*:|statusCode|res\.status` (HTTP status codes)

**Mark ✓ if**: Try/catch with proper error messages
**Mark ✗ if**: No error handling

---

### Rate Limiting
**Why**: Prevent abuse and spam

**Patterns to search**:
- `rateLimit|rate-limit|RateLimit` (rate limit middleware)
- `throttle|Throttle|debounce` (throttling)
- `Ratelimit|upstash.*ratelimit` (rate limit libraries)

**Mark ✓ if**: Rate limit middleware or checks found
**Mark ✗ if**: No rate limiting on write/expensive operations

**Note**: Focus on write operations, expensive operations, public endpoints

---

### Logging
**Why**: Observability and debugging

**Patterns to search**:
- `console\.error|console\.warn|logger\.error` (error logging)
- `Sentry|sentry|captureException` (error tracking services)
- `audit|auditLog|createAuditLog` (audit trails)

**Mark ✓ if**: Error logging AND audit logs for sensitive actions
**Mark ⚠ if**: Console logging only
**Mark ✗ if**: No logging

---

### Database Operations
**Why**: Ensure data integrity

**Patterns to search**:
- `transaction|\.transaction\(|prisma\.\$transaction` (transactions)
- `\.create\(|\.update\(|\.delete\(` (DB operations)
- `catch.*database|catch.*db` (DB error handling)

**Mark ✓ if**: Transactions for multi-step operations AND DB error handling
**Mark ✗ if**: No transactions or unhandled DB errors

---

## Form Checklist

**Apply to**: Files with `<form>` or `useForm`

### Client-Side Validation
**Why**: Immediate user feedback

**Patterns to search**:
- `zodResolver|yupResolver|joiResolver` (validation libraries)
- `register.*required|validate:|rules:` (field validation)
- `errors\.|formState\.errors` (error display)

**Mark ✓ if**: Form validation with error display
**Mark ✗ if**: No client-side validation

---

### Server-Side Validation
**Why**: Security - never trust client

**Patterns to search**:
- Server action has `\.parse\(|validate` after form submission
- API route validates form data before processing

**Mark ✓ if**: Server validates same fields as client
**Mark ✗ if**: Client validation only

---

### Submit States
**Why**: Prevent double submissions

**Patterns to search**:
- `isSubmitting|isPending|formState\.isSubmitting` (submit state)
- `disabled={.*isSubmitting` (disabled button during submit)

**Mark ✓ if**: Submit state prevents double submission
**Mark ✗ if**: No submit state tracking

---

### Field-Level Errors
**Why**: Users need to know what's wrong

**Patterns to search**:
- `errors\.[fieldName]|errors\?\.[fieldName]` (error access)
- `error && <span|error && <p` (error display)
- `text-red|text-destructive|error-message` (error styling)

**Mark ✓ if**: Field errors displayed inline
**Mark ✗ if**: No field-specific error messages

---

### Reset/Clear
**Why**: Let users start over

**Patterns to search**:
- `reset\(|resetForm|clearForm` (reset functions)
- `type="reset"|onClick.*reset` (reset buttons)

**Mark ✓ if**: Reset functionality exists
**Mark ⚠ if**: Missing (nice to have, not critical)

---

## Gap Categories

### Blockers (MUST fix before shipping)
- Security issues (auth, permissions, injection)
- Data integrity issues (validation, race conditions)
- Critical user flows broken

### Recommended (SHOULD fix before shipping)
- Accessibility gaps
- Error handling gaps
- Logging/observability gaps
- Edge case handling

### Nice to Have (Can defer)
- Color contrast checks (needs manual verification)
- Performance optimization
- Advanced error recovery

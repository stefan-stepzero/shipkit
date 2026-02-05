# Best Practices Reference

**Purpose**: Detailed guidance for each best practice category mentioned in specs

---

## Frontend Best Practices

### State Management
- Lift state to the lowest common ancestor that needs it
- Use controlled components for all form inputs
- Avoid prop drilling beyond 2 levels (use context or composition)
- Colocate state with the components that use it
- Derive state when possible instead of syncing

### User Feedback
- Show loading indicators for operations > 300ms
- Disable buttons during async operations to prevent double-submission
- Confirm destructive actions with a modal or undo option
- Provide immediate visual feedback on interactions (hover, active states)
- Show success/error toasts for completed operations
- Use optimistic updates for better perceived performance

### Accessibility
- All interactive elements must be keyboard accessible
- Provide visible focus indicators (don't remove `outline`)
- Use semantic HTML (`<button>`, `<nav>`, `<main>`, not `<div onClick>`)
- Include alt text for images, aria-labels for icon buttons
- Ensure sufficient color contrast (4.5:1 for text, 3:1 for UI)
- Support screen readers with proper heading hierarchy

### Performance
- Lazy load routes and heavy components
- Optimize images (WebP, proper sizing, lazy loading)
- Memoize expensive computations with `useMemo`
- Debounce search inputs and resize handlers
- Virtualize long lists (> 100 items)
- Minimize bundle size (tree shaking, code splitting)

### Security
- Sanitize user input before rendering (prevent XSS)
- Never store sensitive data in localStorage (use httpOnly cookies)
- Validate all inputs client-side AND server-side
- Use CSRF tokens for state-changing requests
- Implement proper authentication state management
- Don't expose API keys in client-side code

### Forms
- Validate on blur AND on submit
- Show inline validation errors next to fields
- Preserve form state on validation failure
- Disable submit until required fields valid (optional, show errors instead)
- Support keyboard submission (Enter key)
- Auto-focus first field on form mount

### Navigation
- Show loading state during route transitions
- Preserve scroll position on back navigation
- Confirm before navigating away from unsaved changes
- Use proper `<Link>` components (not `onClick` navigation)
- Handle 404s gracefully with helpful messaging
- Support browser back/forward buttons

---

## Backend Best Practices

### Input Validation
- Validate at API boundary before processing
- Use schema validation (Zod, Joi, class-validator)
- Reject invalid input early with clear error messages
- Sanitize strings (trim, normalize unicode)
- Validate file uploads (type, size, content)
- Never trust client-provided IDs without verification

### Authentication
- Use secure session management (httpOnly, secure, sameSite cookies)
- Implement proper password hashing (bcrypt, argon2)
- Support MFA for sensitive operations
- Set appropriate session timeouts
- Invalidate sessions on password change
- Rate limit login attempts

### Error Handling
- Never expose stack traces to clients in production
- Log errors with context (user, request, timestamp)
- Use consistent error response format
- Distinguish client errors (4xx) from server errors (5xx)
- Provide actionable error messages
- Implement global error handlers

### Data Integrity
- Use database transactions for multi-step operations
- Implement optimistic locking for concurrent updates
- Validate foreign key relationships
- Handle soft deletes properly (don't orphan related data)
- Maintain audit trails for sensitive data changes
- Use database constraints as safety net

### Security
- Use parameterized queries (prevent SQL injection)
- Implement proper authorization checks on every endpoint
- Validate Content-Type headers
- Set security headers (CORS, CSP, X-Frame-Options)
- Encrypt sensitive data at rest
- Rotate secrets regularly

### Performance
- Index database columns used in WHERE/JOIN clauses
- Paginate list endpoints (never return unbounded results)
- Cache expensive queries with appropriate TTL
- Use connection pooling for databases
- Implement request timeouts
- Profile slow endpoints

### API Design
- Use consistent naming conventions (camelCase or snake_case, not mixed)
- Version your API (v1, v2 in path or header)
- Return appropriate HTTP status codes
- Support filtering, sorting, pagination on list endpoints
- Document all endpoints (OpenAPI/Swagger)
- Use meaningful error codes

---

## Quick Checklist for Spec Review

### Before Implementation
- [ ] All edge cases from 6 categories addressed?
- [ ] Frontend best practices applicable to this feature identified?
- [ ] Backend best practices applicable to this feature identified?
- [ ] Security considerations documented?
- [ ] Performance implications considered?

### During Implementation
- [ ] Input validation in place?
- [ ] Error handling complete?
- [ ] Loading states implemented?
- [ ] Accessibility requirements met?

### Before Ship
- [ ] All best practices from spec actually implemented?
- [ ] No security shortcuts taken?
- [ ] Performance acceptable?
- [ ] Error messages user-friendly?

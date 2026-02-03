# Database & Data Layer Checks

Applies when project has a database (Supabase, Postgres, etc.).

---

## Row Level Security (Supabase)

### DB-RLS-001: RLS Enabled on User Tables
**Check**: All tables with user data have RLS enabled
**Scan for**: Tables without RLS, `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`
**Pass criteria**: RLS enabled on all user-facing tables
**Fail impact**: Any user can read/write any data
**Severity**: 🔴 Blocker

### DB-RLS-002: RLS Policies Exist
**Check**: Tables have appropriate RLS policies
**Scan for**: Policy definitions for SELECT, INSERT, UPDATE, DELETE
**Pass criteria**: Policies scope access to authenticated user's data
**Fail impact**: RLS enabled but no policies = no access
**Severity**: 🔴 Blocker

### DB-RLS-003: Service Role Not Exposed
**Check**: Supabase service_role key not in client code
**Scan for**: `service_role` key in frontend, browser-accessible code
**Pass criteria**: Only anon key in client
**Fail impact**: Full database access from browser
**Severity**: 🔴 Blocker

---

## Query Safety

### DB-QUERY-001: No Raw SQL from User Input
**Check**: User input not concatenated into SQL
**Scan for**: String interpolation in SQL, `${userInput}` in queries
**Pass criteria**: Parameterized queries only
**Fail impact**: SQL injection
**Severity**: 🔴 Blocker

### DB-QUERY-002: Queries Scoped to User
**Check**: All queries include user_id filter
**Scan for**: SELECT/UPDATE/DELETE without user_id WHERE clause
**Pass criteria**: Every query filtered by authenticated user
**Fail impact**: Users access others' data
**Severity**: 🔴 Blocker

### DB-QUERY-003: N+1 Queries Avoided
**Check**: Related data fetched efficiently
**Scan for**: Queries in loops, multiple queries for list items
**Pass criteria**: JOINs or batch queries used
**Fail impact**: Slow performance, database load
**Severity**: 🟡 Warning

---

## Schema & Migrations

### DB-SCHEMA-001: Migrations Exist
**Check**: Schema changes tracked in migrations
**Scan for**: Migration files, schema version tracking
**Pass criteria**: Reproducible schema from migrations
**Fail impact**: Schema drift, deployment failures
**Severity**: 🟡 Warning

### DB-SCHEMA-002: Migrations Auto-Run or Documented
**Check**: Migration process documented or automated
**Scan for**: Migration in CI/CD, migration docs
**Pass criteria**: Clear process for schema updates
**Fail impact**: Manual steps forgotten
**Severity**: 🟡 Warning

### DB-SCHEMA-003: Indexes on Query Patterns
**Check**: Frequently queried columns indexed
**Scan for**: Index definitions, common WHERE clauses
**Pass criteria**: Indexes match query patterns
**Fail impact**: Slow queries as data grows
**Severity**: 🟡 Warning

---

## Data Integrity

### DB-INT-001: Foreign Keys Defined
**Check**: Relationships have foreign key constraints
**Scan for**: Foreign key definitions, REFERENCES clauses
**Pass criteria**: Referential integrity enforced
**Fail impact**: Orphan records, inconsistent data
**Severity**: 🟡 Warning

### DB-INT-002: Cascade Deletes Configured
**Check**: Related records handled on delete
**Scan for**: ON DELETE CASCADE/SET NULL definitions
**Pass criteria**: Deletes don't leave orphans
**Fail impact**: Broken references, orphan data
**Severity**: 🟡 Warning

### DB-INT-003: Required Fields Not Null
**Check**: Required fields have NOT NULL constraint
**Scan for**: Column definitions, required fields
**Pass criteria**: Required data can't be null
**Fail impact**: Incomplete records
**Severity**: 🟢 Info

---

## Backup & Recovery

### DB-BACKUP-001: Backup Strategy Exists
**Check**: Regular backups configured
**Scan for**: Backup configuration, managed service settings
**Pass criteria**: Daily backups minimum
**Fail impact**: Data loss is permanent
**Severity**: 🔴 Blocker

### DB-BACKUP-002: Backup Tested
**Check**: Backup restoration tested
**Scan for**: Restoration procedure documented
**Pass criteria**: Successful test restore
**Fail impact**: Backups might not work
**Severity**: 🟡 Warning

### DB-BACKUP-003: Point-in-Time Recovery (for production)
**Check**: PITR available for critical data
**Scan for**: PITR configuration
**Pass criteria**: Can restore to specific point in time
**Fail impact**: Can only restore to backup time
**Severity**: 🟡 Warning (production only)

---

## Soft Deletes & Data Retention

### DB-DEL-001: Soft Deletes for User Data
**Check**: User data soft deleted, not hard deleted
**Scan for**: deleted_at column, soft delete logic
**Pass criteria**: Data recoverable after "delete"
**Fail impact**: Accidental permanent deletion, GDPR issues
**Severity**: 🟡 Warning

### DB-DEL-002: Data Retention Policy
**Check**: Policy for how long deleted data kept
**Scan for**: Retention configuration, cleanup jobs
**Pass criteria**: Clear retention period documented
**Fail impact**: GDPR compliance issues
**Severity**: 🟡 Warning

---

## Connection Management

### DB-CONN-001: Connection Pooling
**Check**: Database connections pooled appropriately
**Scan for**: Pool configuration, connection limits
**Pass criteria**: Pool sized for expected load
**Fail impact**: Connection exhaustion under load
**Severity**: 🟡 Warning

### DB-CONN-002: Connection Secrets Not Logged
**Check**: Database URLs/passwords not in logs
**Scan for**: Connection string logging
**Pass criteria**: Secrets redacted in all output
**Fail impact**: Credentials exposed in logs
**Severity**: 🔴 Blocker

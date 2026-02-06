# Database & Data Layer Checks (MVP)

Applies when project has a database (Supabase, Postgres, etc.).

**MVP focus**: Security (RLS, injection), data integrity, backup exists.
**Moved to scale-ready**: Indexes, soft deletes, connection pooling, PITR.

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
**Status**: ➡️ MOVED TO SCALE-READY (performance, not correctness)
**Check**: Frequently queried columns indexed
**Severity**: 🟡 Warning — see `/shipkit-scale-ready`

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

### DB-BACKUP-003: Point-in-Time Recovery
**Status**: ➡️ MOVED TO SCALE-READY (enterprise tier)
**Check**: PITR available for critical data
**Severity**: 🟡 Warning — see `/shipkit-scale-ready`

---

## Soft Deletes & Data Retention

**Status**: ➡️ ENTIRE SECTION MOVED TO SCALE-READY

These are important for GDPR compliance but can be added after MVP launch.
See `/shipkit-scale-ready` for DB-DEL-001 (soft deletes) and DB-DEL-002 (retention policy).

---

## Connection Management

### DB-CONN-001: Connection Pooling
**Status**: ➡️ MOVED TO SCALE-READY (performance at scale)
**Check**: Database connections pooled appropriately
**Severity**: 🟡 Warning — see `/shipkit-scale-ready`

### DB-CONN-002: Connection Secrets Not Logged
**Check**: Database URLs/passwords not in logs
**Scan for**: Connection string logging
**Pass criteria**: Secrets redacted in all output
**Fail impact**: Credentials exposed in logs
**Severity**: 🔴 Blocker

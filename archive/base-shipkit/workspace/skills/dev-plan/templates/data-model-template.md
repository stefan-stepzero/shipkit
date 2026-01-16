# Data Model: [Feature Name]

**Spec:** [Link to spec.md]
**Plan:** [Link to plan.md]
**Created:** [Date]

---

## Overview

**Data Requirements from Spec:**
[Summary of what data this feature needs to store/process]

**Storage Technology:** [From constitution, e.g., "PostgreSQL", "MongoDB", "DynamoDB"]

---

## Entities

### [Entity 1, e.g., "User"]

**Purpose:** [What this entity represents]

**Fields:**
```
id: UUID, primary key, auto-generated
email: String, unique, required, indexed
passwordHash: String, required (bcrypt, never expose)
createdAt: Timestamp, default now()
updatedAt: Timestamp, auto-update
lastLoginAt: Timestamp, nullable
```

**Constraints:**
- Unique: email
- Index: email (for login lookup)
- Validation: email must be valid format

**Relationships:**
- Has many: [Related entity]
- Belongs to: [Related entity]

---

### [Entity 2, e.g., "Article"]

**Purpose:** [What this entity represents]

**Fields:**
```
id: UUID, primary key
authorId: UUID, foreign key → User.id
title: String, required, max 200 chars
content: Text, required
status: Enum ['draft', 'published', 'archived'], default 'draft'
publishedAt: Timestamp, nullable
createdAt: Timestamp, default now()
updatedAt: Timestamp, auto-update
```

**Constraints:**
- Foreign key: authorId → User.id (cascade delete)
- Index: authorId (for "user's articles" query)
- Index: (status, publishedAt) (for "published articles" query)

**Relationships:**
- Belongs to: User (author)
- Has many: Comments

---

## Relationships

### Entity-Relationship Diagram

```
User (1) ──< Articles (N)
   │
   └──< Comments (N)

Article (1) ──< Comments (N)
```

### Cardinality Rules

- **User → Articles:** One-to-many
  - One user can author many articles
  - Each article has exactly one author
  - Cascade: Delete user → delete their articles

- **Article → Comments:** One-to-many
  - One article can have many comments
  - Each comment belongs to one article
  - Cascade: Delete article → delete its comments

---

## Indexes

### Primary Indexes
- User.email (unique, btree) - Login lookup
- Article.authorId (btree) - User's articles query
- Comment.articleId (btree) - Article's comments query

### Composite Indexes
- Article.(status, publishedAt) (btree) - Published articles, sorted by date

### Performance Considerations
- Email index: <10ms lookup (tested with 1M rows)
- AuthorId index: <50ms for user with 1000 articles
- Composite index: <100ms for feed query (paginated)

---

## Data Validation

### Application-Level Validation

**User:**
- Email: RFC 5322 format, lowercase before save
- Password: Min 8 chars, 1 uppercase, 1 number (per constitution security rules)

**Article:**
- Title: 1-200 chars, trim whitespace
- Content: Min 1 char, max 100KB
- Status: Must be one of enum values

### Database-Level Constraints

**User:**
- NOT NULL: email, passwordHash
- UNIQUE: email
- CHECK: email LIKE '%@%'

**Article:**
- NOT NULL: authorId, title, content, status
- FOREIGN KEY: authorId REFERENCES User(id) ON DELETE CASCADE
- CHECK: status IN ('draft', 'published', 'archived')

---

## Data Migrations

### Initial Schema

**Migration:** `001_create_users_and_articles.sql`

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_login_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(200) NOT NULL,
  content TEXT NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'draft',
  published_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_articles_author ON articles(author_id);
CREATE INDEX idx_articles_status_published ON articles(status, published_at);
```

### Rollback Strategy

**Down Migration:** `001_drop_users_and_articles.sql`

```sql
DROP TABLE IF EXISTS articles CASCADE;
DROP TABLE IF EXISTS users CASCADE;
```

---

## Data Access Patterns

### Read Queries

**Get user by email (login):**
```sql
SELECT id, email, password_hash, last_login_at
FROM users
WHERE email = $1;
```
- Uses: idx_users_email
- Expected: <10ms

**Get user's published articles:**
```sql
SELECT id, title, published_at
FROM articles
WHERE author_id = $1
  AND status = 'published'
ORDER BY published_at DESC
LIMIT 20 OFFSET $2;
```
- Uses: idx_articles_author, idx_articles_status_published
- Expected: <50ms

### Write Queries

**Create article:**
```sql
INSERT INTO articles (author_id, title, content, status)
VALUES ($1, $2, $3, 'draft')
RETURNING id, created_at;
```
- Expected: <20ms

**Publish article:**
```sql
UPDATE articles
SET status = 'published',
    published_at = CURRENT_TIMESTAMP,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $1 AND author_id = $2
RETURNING published_at;
```
- Expected: <20ms

---

## Caching Strategy

### What to Cache

**User lookups by email:**
- Cache key: `user:email:{email}`
- TTL: 5 minutes
- Invalidate: On password change, logout

**Published articles list:**
- Cache key: `articles:published:{authorId}:{page}`
- TTL: 1 minute
- Invalidate: On article publish/unpublish

### Cache Technology
[From plan, e.g., "Redis"]

---

## Data Privacy & Security

### Sensitive Fields

**Never expose:**
- User.passwordHash
- User.resetToken (if added later)

**PII (Personal Identifiable Information):**
- User.email (encrypt at rest if required by constitution)

### Data Retention

**User data:**
- Keep indefinitely while account active
- On account deletion: Hard delete after 30-day grace period

**Article data:**
- Keep published articles indefinitely
- Archived articles: Soft delete (retain for 1 year)

---

## Scalability Considerations

### Horizontal Scaling

**Read replicas:**
- Route read queries to replicas
- Master for writes only
- Acceptable replication lag: <1s

### Partitioning Strategy

**When to partition:** >10M articles

**Partition key:** author_id
- Keeps user's articles on same shard
- Efficient for "user's articles" queries

### Archive Strategy

**When to archive:** Articles >2 years old with <10 views/month

**Archive table:** articles_archive (same schema, separate table)
- Removes from hot queries
- Reduces index size

---

## Testing Data

### Fixtures

**users.fixture.json:**
```json
[
  {
    "id": "test-user-1",
    "email": "test@example.com",
    "passwordHash": "$2b$10$..."
  }
]
```

**articles.fixture.json:**
```json
[
  {
    "id": "test-article-1",
    "authorId": "test-user-1",
    "title": "Test Article",
    "status": "published"
  }
]
```

### Factories

**User factory:**
- Generates unique emails (test-{uuid}@example.com)
- Default password: "Password123!"
- Random createdAt (last 30 days)

**Article factory:**
- Generates lorem ipsum title/content
- Random status (weighted: 60% draft, 30% published, 10% archived)
- Random author from existing users

---

## Backup & Recovery

**Backup frequency:** [From constitution/plan, e.g., "Daily at 2am UTC"]

**Backup retention:**
- Daily: Last 7 days
- Weekly: Last 4 weeks
- Monthly: Last 12 months

**Recovery time objective (RTO):** [From spec, e.g., "<1 hour"]
**Recovery point objective (RPO):** [From spec, e.g., "<24 hours"]

**Restore procedure:**
1. Identify backup to restore (timestamp)
2. Create new database instance
3. Restore backup
4. Verify data integrity
5. Update connection strings
6. Switch traffic

---

## Schema Versioning

**Current version:** 1.0.0

**Version history:**
- 1.0.0: Initial schema (users, articles)

**Upcoming changes:**
- 1.1.0: Add comments table
- 1.2.0: Add article tags (many-to-many)

**Migration process:**
1. Write forward migration
2. Write rollback migration
3. Test on staging
4. Apply during maintenance window
5. Monitor for issues
6. Keep rollback ready for 24h

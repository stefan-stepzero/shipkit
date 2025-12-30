# Supabase Integration Patterns

Common security pitfalls and best practices for Supabase integrations.

---


### Common Mistakes:

1. **Missing Row-Level Security (RLS) policies**
   - Tables without RLS are PUBLIC by default
   - Any authenticated user can read/write ALL rows
   - MUST enable RLS + create policies

2. **Bypassing RLS with service role**
   - Service role key BYPASSES all RLS
   - Never use in client code
   - Only use server-side when intentional

3. **Weak auth checks**
   - `auth.user()` can be null
   - MUST check user exists before database operations
   - Check user owns resource before updates

4. **Not using RLS policies for multi-tenancy**
   - Filter `user_id` in application code = WRONG
   - Let RLS enforce `user_id = auth.uid()` = RIGHT
   - Prevents data leaks from code bugs

### Security Checklist:

- [ ] RLS enabled on ALL tables (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`)
- [ ] RLS policies created for SELECT/INSERT/UPDATE/DELETE
- [ ] Service role key stored server-side only (not client)
- [ ] Anon key used client-side
- [ ] Auth checks before every protected operation
- [ ] User ownership verified in RLS policies (not app code)
- [ ] Foreign key constraints prevent orphaned records

### Code Pattern - RLS Policies:

```sql
-- ✅ CORRECT - Enable RLS + create policies
CREATE TABLE recipes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  title TEXT,
  content TEXT
);

-- CRITICAL: Enable RLS
ALTER TABLE recipes ENABLE ROW LEVEL SECURITY;

-- Policy: Users see only their recipes
CREATE POLICY "Users see own recipes"
  ON recipes
  FOR SELECT
  USING (auth.uid() = user_id);

-- Policy: Users create recipes for themselves
CREATE POLICY "Users create own recipes"
  ON recipes
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Policy: Users update only their recipes
CREATE POLICY "Users update own recipes"
  ON recipes
  FOR UPDATE
  USING (auth.uid() = user_id);

-- Policy: Users delete only their recipes
CREATE POLICY "Users delete own recipes"
  ON recipes
  FOR DELETE
  USING (auth.uid() = user_id);
```

```sql
-- ❌ WRONG - No RLS (table is public!)
CREATE TABLE recipes (
  id UUID PRIMARY KEY,
  user_id UUID,
  title TEXT
);
-- Missing: ALTER TABLE recipes ENABLE ROW LEVEL SECURITY;
```

### Code Pattern - Client Auth Check:

```javascript
// ✅ CORRECT - Check auth before operations
const { data: { user }, error: authError } = await supabase.auth.getUser();

if (!user) {
  throw new Error('Not authenticated');
}

// RLS enforces user_id = auth.uid(), but explicit check is good practice
const { data, error } = await supabase
  .from('recipes')
  .insert({
    user_id: user.id, // Explicit user_id
    title: 'My Recipe'
  });
```

```javascript
// ❌ WRONG - No auth check
const { data, error } = await supabase
  .from('recipes')
  .insert({ title: 'Recipe' }); // Missing user_id, auth not checked
```

### Code Pattern - Service Role (Server-Side Only):

```javascript
// ✅ CORRECT - Service role server-side only
// Server-side API route:
import { createClient } from '@supabase/supabase-js';

const supabaseAdmin = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY // BYPASSES RLS - server only!
);

// Use ONLY when you intentionally need to bypass RLS
const { data } = await supabaseAdmin
  .from('recipes')
  .select('*'); // Returns ALL rows regardless of user
```

```javascript
// ❌ WRONG - Service role in client code
const supabase = createClient(
  'https://xxx.supabase.co',
  'eyJhbGc...' // Service role key EXPOSED - security breach!
);
```

### References:
- https://supabase.com/docs/guides/auth/row-level-security
- https://supabase.com/docs/guides/auth
- https://supabase.com/docs/reference/javascript/auth-getuser
```

---

**OPENAI INTEGRATION PATTERNS**

```markdown
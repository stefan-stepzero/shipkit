# Git Safety for Vibe Coders

Essential git hooks and workflows that prevent disasters — especially for builders with product backgrounds who might not know what they don't know.

---

## Why This Matters

When you're vibe coding with AI, it's easy to:
- Push broken code that crashes production
- Commit API keys that get scraped within minutes
- Deploy without running tests (because you forgot they exist)
- Overwrite your teammate's work (or your own working version)

Traditional devs learned these lessons painfully over years. This doc gives you the safety net upfront.

---

## The Safety Stack (Priority Order)

| Layer | What It Catches | Setup Effort |
|-------|-----------------|--------------|
| **1. Pre-commit hooks** | Bad formatting, lint errors, secrets | 5 min |
| **2. Pre-push hooks** | Failing tests, type errors, broken builds | 10 min |
| **3. Branch protection** | Direct pushes to main, unreviewed code | 5 min |
| **4. CI/CD pipeline** | Everything above + more, on every PR | 30 min |

Start with 1-2, add the rest as you grow.

---

## 1. Pre-Commit Hooks

Run automatically before every commit. Catches small issues before they pile up.

### What to Run

| Check | Why | Command |
|-------|-----|---------|
| **Formatting** | Consistent code style | `prettier --write` |
| **Linting** | Catch obvious bugs | `eslint --fix` |
| **Secret detection** | Stop API keys from leaking | `git-secrets` or `gitleaks` |

### Setup with Husky + lint-staged

```bash
# Install
npm install -D husky lint-staged

# Initialize husky
npx husky init

# Create pre-commit hook
echo "npx lint-staged" > .husky/pre-commit
```

**package.json:**
```json
{
  "lint-staged": {
    "*.{js,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

Now every commit automatically formats and lints only the files you changed.

### Secret Detection (Critical)

**The nightmare scenario:** You commit an API key, push to GitHub, and within 5 minutes bots have scraped it and are racking up charges on your AWS account.

```bash
# Option 1: gitleaks (recommended)
brew install gitleaks  # or download from GitHub releases

# Add to pre-commit
echo "gitleaks protect --staged" >> .husky/pre-commit
```

**Or add to package.json scripts:**
```json
{
  "scripts": {
    "check-secrets": "gitleaks protect --staged"
  },
  "lint-staged": {
    "*": ["npm run check-secrets"]
  }
}
```

---

## 2. Pre-Push Hooks

Run before pushing to remote. These are your "don't embarrass yourself" checks.

### What to Run

| Check | Why | Command |
|-------|-----|---------|
| **Tests** | Catch broken functionality | `npm test` |
| **Type check** | Catch type errors (TypeScript) | `tsc --noEmit` |
| **Build** | Verify it actually compiles | `npm run build` |

### Setup

```bash
# Create pre-push hook
cat > .husky/pre-push << 'EOF'
#!/bin/sh

echo "Running pre-push checks..."

# Type check (if using TypeScript)
echo "→ Type checking..."
npm run typecheck || exit 1

# Run tests
echo "→ Running tests..."
npm test || exit 1

# Verify build works
echo "→ Verifying build..."
npm run build || exit 1

echo "✓ All checks passed!"
EOF

chmod +x .husky/pre-push
```

**package.json scripts:**
```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "build": "vite build"
  }
}
```

### When to Skip (Escape Hatch)

Sometimes you need to push broken code (WIP branch, asking for help):

```bash
git push --no-verify
```

**Use sparingly.** If you're using this often, your hooks might be too slow.

---

## 3. Branch Protection

Prevent accidental pushes directly to main/production.

### GitHub Settings

1. Go to repo → Settings → Branches
2. Add rule for `main` (or `master`)
3. Enable:
   - ✅ Require pull request before merging
   - ✅ Require status checks to pass (after setting up CI)
   - ✅ Require conversation resolution
   - ✅ Do not allow bypassing the above settings (even for admins)

### Local Protection (Belt + Suspenders)

Add to `.husky/pre-push`:

```bash
#!/bin/sh

# Prevent direct push to main
branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
  echo "❌ Direct push to $branch is not allowed!"
  echo "Create a feature branch and open a PR instead."
  exit 1
fi

# ... rest of pre-push checks
```

---

## 4. CI/CD Pipeline

Runs on GitHub's servers after you push. The final safety net.

### Basic GitHub Actions Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run typecheck

      - name: Test
        run: npm test

      - name: Build
        run: npm run build
```

### What This Gives You

- Every PR shows ✅ or ❌ before you merge
- Can't accidentally merge broken code
- Runs on clean environment (catches "works on my machine" issues)
- History of all checks for every commit

---

## Common Vibe Coder Gotchas

Things that bite people without traditional dev backgrounds:

### 1. "It Works Locally" Syndrome

**Problem:** You tested in dev, pushed to prod, everything broke.

**Why:** Environment differences, missing env vars, different database state.

**Fix:**
- CI/CD runs in clean environment (catches this)
- Use `.env.example` to document required variables
- Add build step to pre-push hooks

### 2. The Force Push Disaster

**Problem:** `git push --force` and you just overwrote your teammate's (or your own) work.

**What it looks like:**
```bash
git push --force  # Seems to work...
# Later: "Where did all my commits go??"
```

**Fix:**
```bash
# Never use --force, use --force-with-lease instead
git push --force-with-lease

# This fails if remote has commits you don't have locally
```

Add alias to make it the default:
```bash
git config --global alias.pushf "push --force-with-lease"
```

### 3. Committing Secrets

**Problem:** API keys, passwords, tokens in your code.

**Examples that get you hacked:**
```javascript
// DON'T DO THIS
const API_KEY = "sk-1234567890abcdef";
const DB_PASSWORD = "supersecret123";
```

**Fix:**
1. Use `.env` files (add to `.gitignore`)
2. Use secret detection in pre-commit hooks
3. If you already committed a secret:
   ```bash
   # Rotate the secret IMMEDIATELY (it's already compromised)
   # Then remove from history:
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/secret-file" \
     --prune-empty --tag-name-filter cat -- --all
   ```

### 4. No Tests = No Safety Net

**Problem:** You're making changes with no way to know if you broke something.

**Why vibe coders skip tests:**
- "AI wrote it, it must work"
- "I'll add tests later" (you won't)
- "It's just a small project"

**Minimum viable testing:**
```javascript
// At least test your critical paths
// tests/auth.test.js
test('login with valid credentials works', async () => {
  const result = await login('user@test.com', 'password');
  expect(result.success).toBe(true);
});

test('login with invalid credentials fails', async () => {
  const result = await login('user@test.com', 'wrong');
  expect(result.success).toBe(false);
});
```

**Ask Claude:** "What are the critical paths in this code that should have tests?"

### 5. The "Main is Broken" Problem

**Problem:** Main branch is broken, can't deploy, can't demonstrate to users.

**Why it happens:**
- Direct pushes to main
- Merging without testing
- No branch protection

**Fix:**
- Never work directly on main
- Always use feature branches
- Always open PRs, even for small changes
- Enable branch protection (see section 3)

### 6. "I'll Remember" (You Won't)

**Problem:** Manual checks you tell yourself you'll do every time.

**Examples:**
- "I'll run tests before pushing"
- "I'll check for console.logs"
- "I'll update the changelog"

**Fix:** Automate everything. If it's important enough to remember, it's important enough to automate.

---

## Quick Setup Checklist

### Minimum Viable Safety (15 minutes)

```bash
# 1. Install husky
npm install -D husky lint-staged
npx husky init

# 2. Add pre-commit (formatting + secrets)
echo 'npx lint-staged' > .husky/pre-commit

# 3. Add lint-staged config to package.json
# (see examples above)

# 4. Add pre-push (tests + build)
# (see examples above)

# 5. Enable branch protection on GitHub
# Settings → Branches → Add rule → main
```

### Full Safety Stack (1 hour)

1. ✅ Pre-commit: formatting, linting, secret detection
2. ✅ Pre-push: tests, type check, build verification
3. ✅ Branch protection: require PRs, require checks
4. ✅ CI/CD: GitHub Actions running all checks
5. ✅ Force push protection: `--force-with-lease` alias

---

## Tool Alternatives

| Task | Recommended | Alternatives |
|------|-------------|--------------|
| Git hooks | Husky | Lefthook, simple-git-hooks |
| Staged file running | lint-staged | - |
| Secret detection | gitleaks | git-secrets, trufflehog |
| Formatting | Prettier | Biome, dprint |
| Linting | ESLint | Biome, oxlint |
| Testing | Vitest | Jest, Playwright |
| CI/CD | GitHub Actions | GitLab CI, CircleCI |

---

## When Things Go Wrong

### "Pre-push hook is too slow"

```bash
# Option 1: Run tests in parallel
npm test -- --parallel

# Option 2: Only run affected tests
npm test -- --changed

# Option 3: Skip occasionally (use sparingly)
git push --no-verify
```

### "I committed a secret"

1. **Rotate immediately** — The secret is compromised the moment it's pushed
2. Remove from history (see section above)
3. Add secret detection to prevent recurrence

### "CI is passing but prod is broken"

- Environment variables different? Check `.env.example`
- Database state different? Check migrations
- API dependencies down? Add health checks
- Add smoke tests that run against staging

### "I can't push, hooks keep failing"

```bash
# See what's failing
npm run lint
npm run typecheck
npm test

# Fix issues, or if truly stuck:
git push --no-verify  # Last resort
```

---

## Summary

| Hook | When | What | Time |
|------|------|------|------|
| **pre-commit** | Every commit | Format, lint, secrets | ~2s |
| **pre-push** | Every push | Tests, types, build | ~30s |
| **CI/CD** | Every PR | Everything, clean env | ~2-5m |

**The 80/20:** If you only do one thing, set up **pre-push hooks with tests**. This single change prevents most disasters.

---

## Related

- [Husky documentation](https://typicode.github.io/husky/)
- [lint-staged](https://github.com/lint-staged/lint-staged)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [GitHub Actions](https://docs.github.com/en/actions)

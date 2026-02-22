---
name: shipkit-dev-release
description: Manages Shipkit release process — version bump, validation, changelog, counts update, and pre-push checklist. Ensures nothing ships broken. Use when preparing a new Shipkit version for GitHub.
argument-hint: "[patch|minor|major] [--dry-run]"
---

# shipkit-dev-release - Framework Release Manager

**Purpose**: Ensure consistent, validated releases of the Shipkit framework

**What it does**:
- Bumps version in `VERSION`
- Runs all validation (integrity + skill validation)
- Updates counts in README and overview HTML
- Generates changelog entry
- Runs pre-push checklist
- Optionally tags and pushes

---

## When to Invoke

**User says:**
- "Release a new version"
- "Prepare for release"
- "Bump the version"
- "Ship it"
- "Push to GitHub"

**Automated trigger:**
- After `/shipkit-dev-review` passes
- As the final step of a development cycle

---

## Prerequisites

**Required**:
- Clean git working tree (or only expected changes staged)
- All changes committed
- Review passed (no blockers from `/shipkit-dev-review`)

**Helpful context**:
- Current version in `VERSION`
- Recent git log for changelog generation

---

## Process

### Step 1: Determine Version Bump

Read current version from `VERSION`.

If argument provided (`patch`, `minor`, `major`), use it. Otherwise, infer:

| Change Type | Bump |
|-------------|------|
| Bug fixes, typo fixes, minor skill tweaks | `patch` (1.9.1 → 1.9.2) |
| New skills, new agents, new features | `minor` (1.9.2 → 1.10.0) |
| Breaking changes, major refactors | `major` (1.10.0 → 2.0.0) |

Ask user to confirm: "Bumping from {current} to {new}. Correct?"

### Step 2: Pre-Release Validation

Run these checks (all must pass):

**2.1 Framework Integrity**
```
/shipkit-framework-integrity --quick
```
- Manifest ↔ disk sync
- Broken references
- Hook syntax
- Settings validity

**2.2 Skill Count Audit**
Count skills on disk vs counts in:
- `README.md` — skill count number
- `docs/generated/shipkit-overview.html` — stat-number span
- `install/profiles/shipkit.manifest.json` — definitions count

All three must match actual disk count.

**2.3 Git Status Check**
```bash
git status
git diff --cached
```
- No unexpected untracked files
- No uncommitted changes (unless intentionally staging)
- No files that should be gitignored but aren't

**2.4 Secrets Scan**
Search for patterns that shouldn't be committed:
- API keys (`sk-`, `pk_`, `AKIA`)
- Tokens (`token`, `secret`, `password` in config files)
- `.env` files not in `.gitignore`

**2.5 Installer Check**
Verify `install/install.sh`:
- References correct file paths
- No hardcoded versions (should read from VERSION)
- All skill directories it copies exist

### Step 3: Update Version

Write new version to BOTH version sources (must stay in sync):
1. `VERSION` — Source of truth for framework version
2. `package.json` — npm registry version (must match VERSION)

```bash
# Update VERSION file
echo "X.Y.Z" > VERSION
# Update package.json version field
node -e "const p=require('./package.json');p.version='X.Y.Z';require('fs').writeFileSync('package.json',JSON.stringify(p,null,2)+'\n')"
```

### Step 4: Update Counts

Run the sync-docs command to regenerate all counts from the manifest:

```bash
node cli/bin/shipkit.js sync-docs
```

This updates `<!-- sync:* -->` markers in README.md, installers/README.md, and shipkit-overview.html.
Verify the output shows correct counts and no unexpected changes.

### Step 5: Generate Changelog Entry

Read git log since last tag:
```bash
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~20")..HEAD --oneline
```

Group commits by category:
- **Added** — New skills, agents, hooks, features
- **Changed** — Modifications to existing components
- **Fixed** — Bug fixes
- **Removed** — Deprecated/removed components

Format:
```markdown
## v{version}

### Added
- shipkit-team skill with Agent Teams integration
- TaskCompleted and TeammateIdle quality gate hooks

### Changed
- Updated master routing table

### Fixed
- Settings.json trailing comma
```

Present to user for review/edit before writing.

### Step 6: Pre-Push Checklist

Present the checklist for user confirmation:

```
## Release Checklist: v{version}

### Automated Checks
- [x] Framework integrity: PASS
- [x] Skill counts match: {N} skills
- [x] No secrets detected
- [x] Installer paths valid
- [x] Git tree clean

### Manual Checks (user confirms)
- [ ] Changelog entry reviewed
- [ ] Breaking changes documented (if any)
- [ ] README updated (if needed)
- [ ] Tested installation in a fresh project (recommended for minor/major)

### Ready to Release?
```

### Step 7: Commit and Tag

If user confirms:

```bash
git add VERSION package.json README.md docs/generated/shipkit-overview.html
git commit -m "v{version}: {summary}"
git tag v{version}
```

### Step 8: Push (with confirmation)

Ask before pushing:
```
Push v{version} to origin? This will:
- Push commits to {branch}
- Push tag v{version}
```

If confirmed:
```bash
git push origin {branch}
git push origin v{version}
```

If `--dry-run`: Skip steps 7-8, just report what would happen.

---

## Output Quality Checklist

- [ ] Version bump is semantically correct
- [ ] All validation passed before version bump
- [ ] Counts are accurate across all files
- [ ] Changelog covers all commits since last tag
- [ ] No secrets in the release
- [ ] User confirmed the release

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-dev-review` — Design review should pass first
  - **Trigger**: Review verdict is PASS
  - **Why**: Don't release unreviewed changes
- `/shipkit-framework-integrity` — Structural and skill validation
  - **Trigger**: Called automatically in Step 2

### After This Skill
- GitHub release — user creates release notes on GitHub
- `/shipkit-update` — users in other projects pull the new version

---

## Context Files This Skill Reads

- `VERSION` — Current version (source of truth)
- `package.json` — npm package version (must match VERSION)
- `README.md` — Skill counts and feature lists
- `docs/generated/shipkit-overview.html` — Skill counts
- `install/profiles/shipkit.manifest.json` — Manifest
- `install/install.sh` — Installer paths
- `.gitignore` — What's excluded

## Context Files This Skill Writes

- `VERSION` — Updated version number
- `package.json` — Updated version field (must match VERSION)
- Potentially: `README.md`, `docs/generated/shipkit-overview.html` (count updates)

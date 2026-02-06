# Scripts (Dev Only)

These scripts are tracked on the `dev` branch only (private). They don't ship with the public release.

## Available Scripts

### merge-to-main.sh
Merges dev → main while excluding `dev/` folder.

```bash
./Scripts/merge-to-main.sh "Release: feature X"
```

**What it does:**
1. Merges dev into main (no-commit)
2. Restores main's version of `dev/` (excludes dev artifacts)
3. Commits with your message
4. Reminds you to push

### update-version.py
Updates version number across all files.

```bash
python Scripts/update-version.py 1.8.0
```

### package-for-sharing.py
Packages Shipkit for distribution.

---

## Workflow: Dev Branch with Private Artifacts

### Problem
We want `dev/` and `Scripts/` on the dev branch but not on public main.

### Solution: Dual Remote + Selective Merge

**Remotes:**
- `origin` → public GitHub (stefan-stepzero/shipkit)
- `private` → private GitHub (stefan-stepzero/sg-shipkit-private)

**Branches:**
- `main` tracks `origin/main` (public, clean)
- `dev` tracks `private/dev` (private, includes dev/ and Scripts/)

### Daily Development
```bash
git checkout dev
# ... work ...
git add -A && git commit -m "message"
git push private dev
```

### Release to Public
```bash
# Merge excluding dev/
git checkout main
git merge dev --no-commit --no-ff
git restore --staged --worktree dev/ 2>/dev/null
git restore --staged --worktree Scripts/ 2>/dev/null
git commit -m "Merge dev"
git push origin main

# Sync dev back and restore private folders
git checkout dev
git merge main
git checkout HEAD~1 -- dev/ Scripts/
git add -f dev/ Scripts/
git commit -m "Restore dev/ and Scripts/"
git push private dev
```

### Key Learnings

1. **gitignore doesn't prevent tracking** — Once a file is tracked, gitignore is ignored. Use `git rm --cached` to untrack.

2. **Merging deletes untracked-on-target files** — When main doesn't have `dev/`, merging main→dev deletes it. Must restore after.

3. **Force-add for ignored files** — Use `git add -f` to add files that are in .gitignore.

4. **Dual remotes work well** — Keep public and private work cleanly separated.

5. **Restore from previous commit** — Use `git checkout <commit> -- path/` to restore files from before a merge.

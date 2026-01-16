# Manual Testing Guide - Shipkit Lite Edition

This guide walks through manually testing the lite edition installation and skills in a real repository.

---

## Prerequisites

- Claude Code CLI installed
- Empty test repository or willing to use existing repo
- 30-45 minutes for full workflow test

---

## Phase 1: Installation Test (5 minutes)

### 1.1 Create/Navigate to Test Repository

```bash
# Option A: Create new test repo
mkdir ~/shipkit-lite-test
cd ~/shipkit-lite-test
git init

# Option B: Use existing repo (make sure it's backed up!)
cd ~/my-existing-project
```

### 1.2 Run Installation

```bash
# From shipkit repo root
cd /path/to/sg-shipkit
bash Install.bat  # or install.sh on Mac/Linux
```

**Select:**
- Profile: `lite`
- Language: `python` or `bash` (your preference)
- Target: Your test repo directory

### 1.3 Verify Installation

**Check files created:**
```bash
cd ~/shipkit-lite-test  # or your test repo

# Should exist:
ls -la .claude/settings.json
ls -la CLAUDE.md
ls -la .claude/skills/
ls -la .shipkit/skills/

# Count skills
ls .claude/skills/ | wc -l          # Should be 9
ls .shipkit/skills/ | wc -l         # Should be 8
```

**Check settings.json:**
```bash
cat .claude/settings.json | grep '"edition"'
# Should show: "edition": "lite"
```

**Check CLAUDE.md:**
```bash
head -20 CLAUDE.md
# Should mention "Shipkit Lite"
```

**✅ Pass Criteria:**
- All directories created
- 9 skill definitions installed
- 8 workspace implementations installed
- settings.json contains `"edition": "lite"`
- CLAUDE.md mentions Shipkit Lite

---

## Phase 2: Skill Availability Test (2 minutes)

### 2.1 Start Claude Code

```bash
cd ~/shipkit-lite-test
claude-code
```

### 2.2 Check Skills Available

Type `/` and verify these skills appear:
- `/prod-strategic-thinking-lite`
- `/prod-personas-lite`
- `/prod-user-stories-lite`
- `/dev-specify-lite`
- `/dev-plan-lite`
- `/dev-tasks-lite`
- `/dev-implement-lite`
- `/shipkit-master`
- `/shipkit-status`

**✅ Pass Criteria:**
- All 9 skills appear in autocomplete
- Skills have `-lite` suffix (except master/status)

---

## Phase 3: Product Discovery Workflow Test (15-20 minutes)

### 3.1 Strategic Thinking Skill

```bash
/prod-strategic-thinking-lite
```

**Answer 3-5 questions** (use a real or hypothetical project)

**Verify:**
- [ ] Skill asks questions (3-5, not 10+)
- [ ] Process takes ~15 minutes
- [ ] Output created: `.shipkit/skills/prod-strategic-thinking-lite/outputs/business-canvas-[timestamp].md`
- [ ] Output is ~1 page (not 5-10 pages)
- [ ] Skill suggests next: `/prod-personas-lite`

**Check output file:**
```bash
ls .shipkit/skills/prod-strategic-thinking-lite/outputs/
cat .shipkit/skills/prod-strategic-thinking-lite/outputs/business-canvas-*.md
```

---

### 3.2 Personas Skill

```bash
/prod-personas-lite
```

**Verify:**
- [ ] References business canvas if available
- [ ] Asks 3-5 questions
- [ ] Creates 1 persona only (not 3-5)
- [ ] Output: `.shipkit/skills/prod-personas-lite/outputs/persona-[timestamp].md`
- [ ] Suggests next: `/prod-user-stories-lite`

---

### 3.3 User Stories Skill

```bash
/prod-user-stories-lite
```

**Verify:**
- [ ] References persona if available
- [ ] Creates 5-10 user stories (not 20+)
- [ ] Stories focus on happy path
- [ ] Acceptance criteria are simple (not exhaustive)
- [ ] Output: `.shipkit/skills/prod-user-stories-lite/outputs/user-stories-[timestamp].md`
- [ ] Suggests next: `/dev-specify-lite`

---

## Phase 4: Development Workflow Test (15-20 minutes)

### 4.1 Specify Skill

```bash
/dev-specify-lite
```

**Pick one user story to specify**

**Verify:**
- [ ] Asks about feature (3-5 questions)
- [ ] Focuses on happy path
- [ ] Creates 1-page spec (not multi-page)
- [ ] Output: `.shipkit/skills/dev-specify-lite/outputs/spec-[feature]-[timestamp].md`
- [ ] Suggests next: `/dev-plan-lite`

---

### 4.2 Plan Skill

```bash
/dev-plan-lite
```

**Verify:**
- [ ] References spec if available
- [ ] Creates simple task list (5-10 tasks)
- [ ] Linear implementation order
- [ ] Output: `.shipkit/skills/dev-plan-lite/outputs/plan-[feature]-[timestamp].md`
- [ ] Suggests next: `/dev-tasks-lite`

---

### 4.3 Tasks Skill

```bash
/dev-tasks-lite
```

**Verify:**
- [ ] References plan if available
- [ ] Creates detailed checklist
- [ ] Tasks are actionable
- [ ] Output: `.shipkit/skills/dev-tasks-lite/outputs/tasks-[feature]-[timestamp].md`
- [ ] Suggests next: `/dev-implement-lite`

---

### 4.4 Implement Skill

```bash
/dev-implement-lite
```

**Verify:**
- [ ] References tasks if available
- [ ] Provides TDD-lite guidance
- [ ] Doesn't create code automatically (it's guidance)
- [ ] Suggests manual testing
- [ ] examples.md shows implementation workflow

---

## Phase 5: Meta Skills Test (5 minutes)

### 5.1 Shipkit Status

```bash
/shipkit-status
```

**Verify:**
- [ ] Shows which skills have been run
- [ ] Lists output files created
- [ ] Suggests next logical skill

---

### 5.2 Shipkit Master (Auto-loaded)

**Check session start:**
- [ ] SessionStart hook fired (check for any enforcement messages)
- [ ] Can view available skills
- [ ] Routing guidance works

---

## Phase 6: File Structure Validation (3 minutes)

### 6.1 Check Outputs Created

```bash
# Count output files
find .shipkit/skills/*/outputs -name "*.md" | wc -l
# Should be 6 (canvas, persona, stories, spec, plan, tasks)
```

### 6.2 Check File Permissions

```bash
# Try to edit a template (should be protected or warned)
# Try to edit an output (should work)
echo "# Test" >> .shipkit/skills/prod-strategic-thinking-lite/outputs/business-canvas-*.md
# Should succeed
```

### 6.3 Check Examples Accessible

```bash
# Verify examples.md at root (lite convention)
ls .shipkit/skills/prod-strategic-thinking-lite/examples.md
ls .shipkit/skills/prod-personas-lite/examples.md
# Should NOT be in references/
```

---

## Phase 7: Workflow Continuity Test (2 minutes)

### 7.1 Verify Chain Works

**Check that each skill:**
1. References previous outputs when appropriate
2. Suggests next skill in workflow
3. Builds on prior work

**Example:**
- `/prod-personas-lite` should reference business canvas from `/prod-strategic-thinking-lite`
- `/dev-specify-lite` should reference user stories from `/prod-user-stories-lite`

---

## Common Issues to Watch For

### Issue: Skill doesn't load
**Symptom:** "Skill not found" error
**Check:**
- Skill listed in `.claude/skills/`?
- YAML frontmatter correct?
- Run: `ls .claude/skills/[skill-name]/SKILL.md`

### Issue: Can't write to outputs/
**Symptom:** Permission denied
**Check:**
- `.shipkit/skills/[skill]/outputs/` exists?
- Permissions set correctly?
- Run: `ls -la .shipkit/skills/[skill]/`

### Issue: Scripts not found
**Symptom:** "Script not found" when skill tries to run
**Check:**
- Scripts exist: `ls .shipkit/skills/[skill]/scripts/`
- Scripts executable: `ls -l .shipkit/skills/[skill]/scripts/*.sh`
- If not: `chmod +x .shipkit/skills/*/scripts/*.sh`

### Issue: Skill asks too many questions
**Symptom:** More than 5 questions, takes >20 minutes
**Possible Cause:** Wrong skill (full version vs lite)
**Check:** Skill name ends with `-lite`?

---

## Success Criteria Summary

**Installation:**
- ✅ 9 skills installed
- ✅ Settings marked as lite edition
- ✅ CLAUDE.md mentions Shipkit Lite

**Product Workflow:**
- ✅ Each skill completes in ~15-20 minutes
- ✅ Outputs are 1-2 pages (not 5-10)
- ✅ Skills chain together logically
- ✅ Canvas → Persona → Stories flow works

**Development Workflow:**
- ✅ Spec → Plan → Tasks → Implement flow works
- ✅ Each skill references previous outputs
- ✅ Guidance is minimal, focused on POC/MVP

**File Structure:**
- ✅ Outputs created in correct locations
- ✅ examples.md at root (not in references/)
- ✅ Scripts executable
- ✅ Templates accessible

---

## Reporting Issues

When testing finds issues, report:

1. **What:** Which skill/test failed
2. **Where:** File path or specific step
3. **Expected:** What should have happened
4. **Actual:** What actually happened
5. **Logs:** Relevant error messages

**Example:**
```
Issue: prod-personas-lite creates 3 personas instead of 1
Where: Step 3.2 of product workflow
Expected: Single persona for lite edition
Actual: Created 3 personas (full version behavior)
Logs: [paste relevant output]
```

---

## Time Estimates

- **Quick smoke test** (Phases 1-2): 10 minutes
- **Product workflow test** (Phase 3): 20 minutes
- **Development workflow test** (Phase 4): 20 minutes
- **Full test** (All phases): 45 minutes

---

## After Testing

**If all tests pass:**
1. Document any observations
2. Consider testing in a real project
3. Lite edition ready to use!

**If tests fail:**
1. Document failures using format above
2. Run automated tests to isolate issue:
   ```bash
   python3 tests/test-installation.py
   python3 tests/test-skill-compliance.py
   ```
3. Check skill definitions in `install/skills/`
4. Fix issues and re-test

---

## Quick Test Script

For rapid verification (no actual skill execution):

```bash
# Run from shipkit repo root
cd /path/to/sg-shipkit

# 1. Automated tests
bash tests/run-all-tests.sh

# 2. Install to temp
mkdir /tmp/shipkit-test
cd /tmp/shipkit-test
bash /path/to/sg-shipkit/installers/install.sh lite python /tmp/shipkit-test -y

# 3. Verify
ls .claude/skills/ | wc -l      # Should be 9
ls .shipkit/skills/ | wc -l     # Should be 8
grep '"edition"' .claude/settings.json

# 4. Cleanup
cd ~
rm -rf /tmp/shipkit-test
```

This gives confidence without full manual workflow testing.

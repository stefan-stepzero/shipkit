# Error Handling for Task Tracking

How to handle common error scenarios when tracking user tasks.

---

## If `.shipkit-lite/` Directory Doesn't Exist

**Scenario:** First time using task tracking, directory structure missing.

**Solution:**
1. Create `.shipkit-lite/` directory automatically
2. Create `user-tasks/` subdirectory
3. Create `active.md` with header template
4. Proceed with task entry

**No user intervention needed** - Just inform them directory was created.

**Example:**
```
"Created task tracking structure at .shipkit-lite/user-tasks/
✓ Added task: Install Stripe CLI"
```

---

## If Task Entry is Malformed in active.md

**Scenario:** Existing task entry doesn't match template format.

**Symptoms:**
- Missing required fields (priority, steps, verification)
- Inconsistent formatting
- Corrupted markdown structure

**Solution:**
1. Don't fail silently
2. Tell user: "Task entry format is inconsistent. I'll recreate it."
3. Parse what information exists
4. Rewrite entry using proper template
5. Preserve original intent and details

**Example:**
```
"Found malformed task entry for 'Install Stripe'.
Reformatting with proper structure...
✓ Task entry corrected"
```

---

## If User Marks Task Complete But Verification Fails

**Scenario:** User claims task is done, but verification criteria not met.

**Example:**
```
User: "I finished installing Stripe CLI"

Verification check: stripe --version
Result: Command not found
```

**Solution:**
1. **Don't move to completed.md**
2. Update status to: "⚠️ Verification failed"
3. Show specific failure reason
4. Ask user to re-do verification steps
5. Keep task in active.md until verified

**Response:**
```
"⚠️ Verification failed: `stripe --version` command not found.

The Stripe CLI may not be installed correctly or not in PATH.

Verification steps:
1. Run `stripe --version`
2. Should output: stripe version X.X.X

Please retry installation or check PATH configuration."
```

---

## If active.md File is Locked or Unreadable

**Scenario:** File permissions issue or file in use.

**Solution:**
1. Show clear error message
2. Suggest user fix permissions
3. Provide fallback: "I can tell you what to add manually"
4. Don't crash or lose task information

**Example:**
```
"Cannot write to .shipkit-lite/user-tasks/active.md
Possible file permission issue.

Your task to track:
[Show task details]

Please add this manually to active.md or fix file permissions."
```

---

## If Multiple Tasks Reference Same Work

**Scenario:** Two tasks created for essentially the same thing.

**Solution:**
1. Detect duplicate intent during creation
2. Ask user: "This seems similar to existing task X. Same thing?"
3. If yes: Update existing task instead of creating new one
4. If no: Create both but cross-reference

**Example:**
```
"I found an existing task: 'Install Stripe CLI'
Your new task: 'Set up Stripe command line tools'

Are these the same? (y/n)
→ If yes: I'll update the existing task
→ If no: I'll create both and note they're related"
```

---

## If Task is Too Vague to Verify

**Scenario:** User wants to track something without clear success criteria.

**Example:**
```
User: "Remind me to improve performance"
```

**Solution:**
1. Ask clarifying questions before creating task
2. Make verification concrete
3. Break into specific sub-tasks if needed

**Example conversation:**
```
Claude: "What specific performance improvement?
- Reduce page load time?
- Optimize database queries?
- Improve API response time?"

User: "Page load time"

Claude: "What's the target? Current load time?"

User: "Currently 3 seconds, want under 1 second"

Task created:
Title: "Reduce page load time to <1 second"
Verification: Run Lighthouse, Performance score > 90
```

---

**Remember:** Errors should be informative and suggest fixes. Never lose task information.

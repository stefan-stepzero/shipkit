# File 2: Update help/shipkit-shipkit-overview.html

**Purpose**: Add new skill to the overview HTML page and increment the skills count

**File**: `help/shipkit-shipkit-overview.html`

---

## Step 1: Increment Skill Count

**Find the stats section** (around line 58-70):

```html
<div class="stat">
    <span class="stat-number">17</span>
    <span class="stat-label">Skills</span>
</div>
```

**Action**: Increment the number by 1

```html
<div class="stat">
    <span class="stat-number">18</span>  <!-- Changed from 17 -->
    <span class="stat-label">Skills</span>
</div>
```

---

## Step 2: Find Correct Category Section

**Categories in the HTML** (search for `<h3>` tags):

1. **Meta/Infrastructure** - Around line 200
2. **Decision & Design** - Around line 230
3. **Implementation** - Around line 260
4. **Documentation** - Around line 290
5. **Quality & Process** - Around line 320

**Match to user's category choice** (from Step 1.3 of wizard):
- User chose category 1 → Meta/Infrastructure section
- User chose category 2 → Decision & Design section
- User chose category 3 → Implementation section
- User chose category 4 → Documentation section
- User chose category 5 → Quality & Process section

---

## Step 3: Add Skill to Category List

**Find the `<ul>` list in the correct category section:**

```html
<h3>Decision & Design</h3>
<ul>
    <li><strong>shipkit-spec</strong> - Feature specifications</li>
    <li><strong>shipkit-architecture-memory</strong> - Decision log</li>
    <li><strong>shipkit-ux-coherence</strong> - UX consistency</li>
    <li><strong>shipkit-data-consistency</strong> - Type management</li>
</ul>
```

**Add new entry** (in alphabetical order):

```html
<h3>Decision & Design</h3>
<ul>
    <li><strong>shipkit-architecture-memory</strong> - Decision log</li>
    <li><strong>shipkit-data-consistency</strong> - Type management</li>
    <li><strong>shipkit-NEW-SKILL</strong> - {2-4 word description}</li>  <!-- NEW -->
    <li><strong>shipkit-spec</strong> - Feature specifications</li>
    <li><strong>shipkit-ux-coherence</strong> - UX consistency</li>
</ul>
```

**Description guidelines**:
- Keep to 2-4 words
- Summarize skill purpose
- Use consistent tone with existing entries

---

## Step 4: Validate HTML

**Check**:
- [ ] Skill count incremented by 1
- [ ] New skill added to correct category section
- [ ] Entry is in alphabetical order
- [ ] HTML structure is valid (no broken tags)
- [ ] Description is concise (2-4 words)

**Validation command**:
```bash
# Check if file is valid HTML (optional)
# Most editors will show syntax errors
```

---

## Example: Adding "shipkit-user-stories"

**Before**:
```html
<!-- Stats -->
<span class="stat-number">17</span>

<!-- Documentation Section -->
<h3>Documentation</h3>
<ul>
    <li><strong>shipkit-component-knowledge</strong> - Component docs</li>
    <li><strong>shipkit-document-artifact</strong> - Standalone docs</li>
    <li><strong>shipkit-route-knowledge</strong> - Route docs</li>
</ul>
```

**After**:
```html
<!-- Stats -->
<span class="stat-number">18</span>  <!-- Incremented -->

<!-- Documentation Section -->
<h3>Documentation</h3>
<ul>
    <li><strong>shipkit-component-knowledge</strong> - Component docs</li>
    <li><strong>shipkit-document-artifact</strong> - Standalone docs</li>
    <li><strong>shipkit-route-knowledge</strong> - Route docs</li>
    <li><strong>shipkit-user-stories</strong> - User requirements</li>  <!-- NEW -->
</ul>
```

---

## Common Mistakes

**❌ Forgetting to increment skill count**
- File shows new skill but count is wrong

**❌ Adding to wrong category**
- Check user's category choice from wizard (Step 1.3)

**❌ Not alphabetizing**
- Keeps list organized and maintainable

**❌ Description too long**
- Keep to 2-4 words max, match existing style

---

## Report Format

After updating, report:

```
✓ File 2: Updated overview.html
  - Incremented skill count: 17 → 18
  - Added to {Category Name} section
  - Entry: shipkit-{skill-name} - {description}
```

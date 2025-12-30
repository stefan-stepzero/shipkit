# Bash Commands for Status Checking

Detailed bash commands for scanning context files and detecting gaps.

---

## Freshness Calculation

```bash
# Get file modification time in seconds since epoch
file_modified=$(stat -c %Y "$file" 2>/dev/null)

# Get current time
now=$(date +%s)

# Calculate age in days
age_days=$(( (now - file_modified) / 86400 ))

if [ $age_days -le 1 ]; then
  echo "✓ Fresh (modified today)"
elif [ $age_days -le 7 ]; then
  echo "⚠ Aging (modified $age_days days ago)"
else
  echo "✗ Stale (modified $age_days days ago)"
fi
```

---

## Gap Detection Patterns

### Large Undocumented Files

```bash
# Find files >200 LOC
large_files=$(find src -type f \( -name "*.ts" -o -name "*.tsx" \) -exec wc -l {} + | awk '$1 > 200 {print $2}')

# Check if mentioned in implementations.md
for file in $large_files; do
  if ! grep -q "$file" .shipkit-lite/implementations.md; then
    echo "⚠ Undocumented: $file"
  fi
done
```

### Stale Stack

```bash
# Compare package.json and stack.md timestamps
if [ package.json -nt .shipkit-lite/stack.md ]; then
  echo "⚠ Stack outdated: package.json modified after stack.md"
fi
```

### Workflow Gaps

```bash
# Specs without plans
spec_count=$(ls -1 .shipkit-lite/specs/active/*.md 2>/dev/null | wc -l)
plan_count=$(ls -1 .shipkit-lite/plans/*.md 2>/dev/null | wc -l)

if [ $spec_count -gt $plan_count ]; then
  echo "⚠ $((spec_count - plan_count)) specs have no plans"
fi
```

---

## File Scanning Commands

### Count Active Specs

```bash
ls -1 .shipkit-lite/specs/active/*.md 2>/dev/null | wc -l
```

### Count Plans

```bash
ls -1 .shipkit-lite/plans/*.md 2>/dev/null | wc -l
```

### Count User Tasks

```bash
if [ -f ".shipkit-lite/user-tasks/active.md" ]; then
  grep -c "^- \[ \]" .shipkit-lite/user-tasks/active.md
fi
```

---

## Status Report Generation

### Add Timestamp

```bash
# Add timestamp to status report
echo "Last Updated: $(date '+%Y-%m-%d %H:%M:%S')" > .shipkit-lite/status.md
echo "" >> .shipkit-lite/status.md
```

# Shipkit Testing Framework

Automated tests to validate installation, skill structure, and compliance with Shipkit patterns.

## Test Suites

### 1. Installation Validation (`test-installation.py`)

**Purpose:** Validates manifest files and skill structure without running installation

**Tests:**
- ✅ Manifest files exist and are valid JSON
- ✅ Manifest structure is correct (edition, skills, agents)
- ✅ All skills referenced in manifest actually exist
- ✅ Settings and CLAUDE.md files exist
- ✅ SKILL.md files have valid YAML frontmatter
- ✅ Workspace implementations have expected structure
- ✅ Skill counts match expectations

**Run:**
```bash
python3 tests/test-installation.py
```

**Speed:** Fast (< 5 seconds)

---

### 2. Skill Compliance (`test-skill-compliance.py`)

**Purpose:** Validates that lite skills follow patterns from LITE-SKILLS-GUIDE.md

**Tests:**
- ✅ File structure (examples.md at root, no references/ folder)
- ✅ SKILL.md length (< 300 lines target, < 500 max)
- ✅ Required sections present
- ✅ Both bash and python scripts exist
- ✅ Templates are simple (1-page target)
- ✅ examples.md has 2-3 examples
- ✅ examples.md length (< 150 lines target)
- ✅ Suggests next skill in workflow

**Run:**
```bash
python3 tests/test-skill-compliance.py
```

**Speed:** Fast (< 5 seconds)

---

### 3. Integration Test (`test-integration.sh`)

**Purpose:** Actually runs installation and validates the result

**Tests:**
- ✅ Installation completes without errors
- ✅ Directory structure created correctly
- ✅ All skills copied to target
- ✅ settings.json is valid and marked as lite edition
- ✅ CLAUDE.md mentions Shipkit Lite
- ✅ Scripts are executable
- ✅ Templates installed
- ✅ Correct skill count (9 definitions, 8 workspace)

**Run:**
```bash
bash tests/test-integration.sh
```

**Speed:** Moderate (~30 seconds, creates temp directory)

---

## Running All Tests

```bash
bash tests/run-all-tests.sh
```

Runs all three test suites in sequence and reports overall results.

---

## Test Output

### Pass Example:
```
✓ Manifest is valid JSON
✓ All required fields present
✓ All 9 skill definitions exist
```

### Fail Example:
```
✗ Manifest not found: lite.manifest.json
✗ Skill definition missing: prod-personas-lite/SKILL.md
```

### Warning Example:
```
⚠ Lite has 10 skill definitions (expected 9)
⚠ examples.md longer than lite target but acceptable (≤300 lines)
```

---

## Exit Codes

- `0` - All tests passed
- `1` - One or more tests failed

Warnings don't cause failure, but indicate potential issues.

---

## When to Run Tests

**Before committing:**
```bash
bash tests/run-all-tests.sh
```

**After creating new skills:**
```bash
python3 tests/test-skill-compliance.py
```

**After modifying manifests:**
```bash
python3 tests/test-installation.py
```

**Before releasing:**
```bash
bash tests/run-all-tests.sh
```

---

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v2
    - name: Run tests
      run: bash tests/run-all-tests.sh
```

---

## Adding New Tests

### For Installation Tests

Edit `test-installation.py` and add new test functions:

```python
def test_new_feature(profile: str, manifest: Dict) -> bool:
    """Test description"""
    global passed_tests, failed_tests

    # Your test logic
    if condition:
        print_pass("Test passed")
        passed_tests += 1
        return True
    else:
        print_fail("Test failed")
        failed_tests += 1
        return False
```

### For Compliance Tests

Edit `test-skill-compliance.py` and add to `test_skill()`:

```python
def test_new_compliance(skill_name: str) -> bool:
    """Test description"""
    global passed, failed, warnings

    # Your test logic
    if compliant:
        print_pass("Compliant")
        passed += 1
        return True
    else:
        print_warn("Not compliant")
        warnings += 1
        return False
```

### For Integration Tests

Edit `test-integration.sh` and add new sections:

```bash
print_section "Test: New Feature"

print_test "Checking new feature..."
if [ condition ]; then
    print_pass "Feature working"
    ((PASSED++))
else
    print_fail "Feature broken"
    ((FAILED++))
fi
```

---

## Troubleshooting

### Python tests fail with import errors

Ensure Python 3.6+ is installed:
```bash
python3 --version
```

### Integration test fails with permission errors

Make scripts executable:
```bash
chmod +x tests/*.sh
chmod +x installers/*.sh
```

### Tests pass locally but fail in CI

Check file paths are correct and all dependencies are available in CI environment.

---

## Test Coverage

Current coverage for Lite edition:

| Area | Coverage |
|------|----------|
| Manifest validation | ✅ 100% |
| Skill structure | ✅ 100% |
| File existence | ✅ 100% |
| Installation process | ✅ 100% |
| Lite compliance | ✅ 100% |
| Script execution | ⚠️ Partial (executability only, not runtime) |

---

## Future Improvements

Potential additions:

1. **Skill Script Tests** - Actually run skill scripts and verify output
2. **YAML Validation** - Deep validation of SKILL.md frontmatter
3. **Link Checking** - Verify internal references in docs
4. **Performance Tests** - Measure installation time
5. **Cross-Platform** - Test on Linux, macOS, Windows
6. **Full Edition Tests** - Expand to cover full Shipkit (not just lite)

---

## Maintenance

Update tests when:
- Adding new skills to manifests
- Changing skill file structure
- Updating LITE-SKILLS-GUIDE.md patterns
- Modifying installation logic
- Changing required sections in SKILL.md

Keep tests synchronized with implementation!

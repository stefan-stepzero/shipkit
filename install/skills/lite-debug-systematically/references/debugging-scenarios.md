# Common Debugging Scenarios

Real-world examples of systematic debugging in action.

---

## Scenario 1: API Call Failing

```
User: "The share button isn't working"

Phase 1 - OBSERVE:
- Network tab shows: 500 error on POST /api/share
- Response body: "Cannot read property 'id' of null"
- Browser console: No client errors
- Server logs: Stack trace points to shareRecipe function

Phase 2 - HYPOTHESIZE:
1. Missing auth check (most likely - null user)
2. Database constraint violation (possible)
3. Missing form data (less likely - error says null user)

Phase 3 - TEST:
- Read app/actions/share-recipe.ts
- Find: No auth validation, directly accesses user.id
- Confirmed: Hypothesis #1 is correct

Phase 4 - FIX:
- Add requireAuth() at start of function
- Verify: Share button now works
- Document: Append to architecture.md
```

---

## Scenario 2: UI Not Rendering

```
User: "Recipe list is blank"

Phase 1 - OBSERVE:
- Browser console: "Cannot read property 'map' of undefined"
- Component: RecipeList.tsx
- Network tab: GET /api/recipes returns []
- Expected: Should show sample recipes

Phase 2 - HYPOTHESIZE:
1. Component expects array but gets undefined (most likely)
2. API returns empty array incorrectly (possible)
3. Conditional rendering bug (less likely)

Phase 3 - TEST:
- Read components/RecipeList.tsx
- Find: recipes.map() called without null check
- API actually returns null on first load
- Confirmed: Hypothesis #1

Phase 4 - FIX:
- Change: recipes?.map() or default to []
- Verify: List renders empty state gracefully
- Document: "UI components should handle null/undefined data"
```

---

## Scenario 3: Build Error

```
User: "Build is failing"

Phase 1 - OBSERVE:
- Terminal: "Module not found: 'lucide-react'"
- Error in: components/Icon.tsx
- Recent change: Added new icon imports

Phase 2 - HYPOTHESIZE:
1. Package not installed (most likely)
2. Import path wrong (possible)
3. Version mismatch (less likely)

Phase 3 - TEST:
- Check package.json: lucide-react is listed
- Check node_modules: lucide-react folder missing
- Confirmed: Hypothesis #1

Phase 4 - FIX:
- Run: npm install
- Verify: Build succeeds
- Document: "After adding dependencies, run install"
```

---

## Pattern Recognition

**After solving multiple bugs, patterns emerge:**

| Bug Pattern | Root Cause | Prevention |
|-------------|------------|------------|
| 500 errors with "Cannot read property of null" | Missing auth checks | Add auth validation template |
| Blank screens after data fetch | Missing null checks in components | Use optional chaining or defaults |
| Build failures after adding imports | Missing npm install | Document dependency installation in README |
| Infinite loops in React | Missing useEffect dependencies | Use ESLint react-hooks plugin |
| Styling not applied | Tailwind not recompiling | Check dev server running, clear cache |

**Use architecture.md to build this pattern library over time.**

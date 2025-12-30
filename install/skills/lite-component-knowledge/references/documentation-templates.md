# Component Documentation Templates

Templates used by `/lite-component-knowledge` for documenting components.

## Metadata Header Template

Place at top of `implementations.md`:

```markdown
<!-- Component Documentation Metadata
Last Full Scan: [ISO 8601 timestamp]
Documented Files:
- [file-path] ([ISO 8601 timestamp])
- [file-path] ([ISO 8601 timestamp])
-->
```

**Example**:
```markdown
<!-- Component Documentation Metadata
Last Full Scan: 2025-01-15T14:30:00Z
Documented Files:
- src/components/RecipeCard.tsx (2025-01-15T14:25:00Z)
- src/components/UserProfile.tsx (2025-01-14T10:00:00Z)
-->
```

## Component Entry Template

Append to end of `implementations.md`:

```markdown
---

## Component: [Name] - Documented [Date]

**File**: `[path]`
**Size**: [LOC] lines
**Last Modified**: [timestamp]
**Documented**: [timestamp]

### Purpose
[Description]

### Pattern & Architecture
- **Type**: [type]
- **Rendering**: [CSR/SSR/etc]
- **State**: [state management]
- **Data fetching**: [approach]

### Props/API
```typescript
[interface or function signature]
```

### Key Decisions
- **[Decision]**: [Rationale]

### Usage Locations
- [location 1]

### Dependencies
- [library 1]

### Notes
[Additional details]

---
```

**Example**:
```markdown
---

## Component: RecipeCard - Documented 2025-01-15

**File**: `src/components/RecipeCard.tsx`
**Size**: 450 lines
**Last Modified**: 2025-01-15T14:25:00Z
**Documented**: 2025-01-15T14:30:00Z

### Purpose
Displays recipe information with image, title, ingredients count, and cooking time. Handles favorite toggling and navigation to recipe details.

### Pattern & Architecture
- **Type**: Presentational
- **Rendering**: CSR (Client-Side Rendering)
- **State**: Local useState for favorite toggle
- **Data fetching**: None (receives data as props)

### Props/API
```typescript
interface RecipeCardProps {
  recipe: Recipe;
  onFavorite: (id: string) => void;
  isFavorite: boolean;
}
```

### Key Decisions
- **Optimistic UI**: Favorite toggle updates immediately before API confirmation for better UX
- **Image lazy loading**: Uses Next.js Image component with priority={false} to defer loading

### Usage Locations
- pages/recipes/index.tsx
- components/RecipeGrid.tsx
- pages/favorites.tsx

### Dependencies
- next/image
- react-icons/fa

### Notes
Currently uses client-side rendering for favorite toggle. Could be migrated to Server Actions in future for improved performance.

---
```

## Metadata Format Specification

**Header format** (must be valid HTML comment):
```html
<!-- Component Documentation Metadata
Last Full Scan: 2025-01-15T14:30:00Z
Documented Files:
- src/components/RecipeCard.tsx (2025-01-15T14:25:00Z)
- src/components/UserProfile.tsx (2025-01-14T10:00:00Z)
-->
```

**Timestamp format**: ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)

**File path format**: Relative to project root

**Parsing logic**:
1. Read implementations.md
2. Extract metadata comment block
3. Parse "Last Full Scan" timestamp
4. Parse file list with timestamps
5. Use these for freshness comparison

**Why metadata header**:
- Enables timestamp-based freshness checking
- Tracks which files were documented when
- Allows incremental updates
- Provides audit trail

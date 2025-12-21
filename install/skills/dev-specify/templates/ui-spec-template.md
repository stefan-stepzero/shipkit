# UI Feature Specification

## Overview

**Feature Name:** [Descriptive name]
**Component Type:** [Page/Modal/Widget/Component]
**User Story:** [Reference from .prodkit/requirements/user-stories.md]
**Problem Statement:** [What user problem does this solve?]

## Brand Alignment

**Voice & Tone:** [Reference .prodkit/brand/personality.md]
- Copy should be: [professional/friendly/technical/casual]
- Button text: [action-oriented/descriptive]
- Error messages: [helpful/empathetic]

**Visual Direction:** [Reference .prodkit/brand/visual-direction.md]
- Color palette: [Primary/secondary colors to use]
- Typography: [Font families, sizes, weights]
- Spacing: [Grid system, padding/margin guidelines]
- Iconography: [Icon style, size]

## User Journey Context

**Where in Journey:** [Reference .prodkit/design/future-state-journeys.md]
- **Previous Step:** [What screen/action comes before?]
- **Current Step:** [This feature]
- **Next Step:** [Where does user go after?]

**Entry Points:**
- User navigates from [Screen A]
- User clicks [Button/Link] in [Location]
- System redirects after [Event]

**Exit Points:**
- Success: User continues to [Next Screen]
- Cancel: User returns to [Previous Screen]
- Error: User sees [Error State]

## Screen Layout

### Desktop View (1920x1080)

```
┌─────────────────────────────────────────────────────────┐
│ Header Navigation                            [User Menu]│
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─ Breadcrumb ──────────────────────────────────┐     │
│  │  Home > Section > Current Page              │     │
│  └──────────────────────────────────────────────────┘     │
│                                                         │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓     │
│  ┃ Main Content Area                           ┃     │
│  ┃                                              ┃     │
│  ┃  [Component elements here]                  ┃     │
│  ┃                                              ┃     │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Tablet View (768x1024)

```
┌─────────────────────────────┐
│ [☰] Header      [User Menu]│
├─────────────────────────────┤
│                             │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Content (stacked)     ┃ │
│ ┃                       ┃ │
│ ┗━━━━━━━━━━━━━━━━━━━━━━━┛ │
│                             │
└─────────────────────────────┘
```

### Mobile View (375x812)

```
┌───────────────┐
│[☰]  Title [≡]│
├───────────────┤
│               │
│ ┏━━━━━━━━━┓ │
│ ┃ Content ┃ │
│ ┃ (full   ┃ │
│ ┃  width) ┃ │
│ ┗━━━━━━━━━┛ │
│               │
└───────────────┘
```

## Component Specifications

### Component 1: [Name]

**Purpose:** [What this component does]

**Location:** [Where it appears on screen]

**Visual Spec:**
- **Dimensions:** Width x Height (or responsive rules)
- **Background:** Color/gradient/image
- **Border:** Style, width, radius
- **Shadow:** Box-shadow values
- **Spacing:** Padding, margin

**Interactive States:**
- **Default:** [Appearance]
- **Hover:** [Visual change]
- **Active/Pressed:** [Visual change]
- **Focus:** [Keyboard focus ring]
- **Disabled:** [Greyed out appearance]
- **Loading:** [Spinner or skeleton]
- **Error:** [Error state styling]

**Content:**
```
[Icon] Heading Text
Description text in body font.
[Button Label]
```

**Behavior:**
- On click: [Action]
- On hover: [Tooltip/preview]
- On error: [Error message location]

**Accessibility:**
- **ARIA Role:** `role="button"` / `role="dialog"` / etc.
- **ARIA Labels:** `aria-label="Descriptive text"`
- **Keyboard Navigation:** Tab order, Enter/Space actions
- **Screen Reader:** Announces as "[Type]: [Label]"

### Component 2: Form Field

**Field Type:** Text input / Dropdown / Checkbox / Radio / etc.

**Label:**
- Text: "[Field Label]"
- Position: Above/beside field
- Required indicator: Red asterisk *

**Input Spec:**
- **Placeholder:** "Enter [field name]"
- **Max Length:** 255 characters
- **Validation:** Real-time / On blur / On submit
- **Format:** Email / Phone / Date / etc.

**Validation States:**
- **Valid:** Green checkmark icon
- **Invalid:** Red error border + error message below
- **Warning:** Yellow border + warning message

**Error Messages:**
```
"Please enter a valid email address"
"Password must be at least 8 characters"
"This field is required"
```

**Help Text:**
```
"Example: user@example.com"
"Must include uppercase, lowercase, and number"
```

## User Interactions

### Interaction 1: [Action]

**Trigger:** User clicks [Button/Link]

**Flow:**
1. User initiates action
2. System shows loading state (spinner, disabled button)
3. API call to [Endpoint]
4. On success:
   - Show success message: "[Message]"
   - Update UI: [Changes]
   - Navigate to: [Next screen]
5. On error:
   - Show error message: "[Message]"
   - Keep user on current screen
   - Focus on error location

**Validation:**
- **Client-side:** Check required fields, format validation
- **Server-side:** Business logic validation
- **Display:** Show errors inline and in summary at top

### Interaction 2: [Animation/Transition]

**Animation Type:** Fade in / Slide up / Expand / etc.

**Duration:** 300ms

**Easing:** ease-in-out

**Trigger:** [When animation plays]

## Responsive Behavior

### Breakpoints
- **Mobile:** < 768px
- **Tablet:** 768px - 1024px
- **Desktop:** > 1024px

### Layout Changes
- **Desktop:** 3-column layout
- **Tablet:** 2-column layout
- **Mobile:** Single column, stacked

### Touch Targets
- **Minimum Size:** 44x44px for touch
- **Spacing:** 8px between tappable elements

## Loading States

### Initial Load
- **Skeleton Screen:** Show placeholder boxes
- **Duration:** Until data loads
- **Fallback:** "Loading..." text after 3 seconds

### Lazy Loading
- **Images:** Load as user scrolls
- **Sections:** Progressive enhancement

### Pull to Refresh (mobile)
- **Gesture:** Pull down from top
- **Feedback:** Spinner animation
- **Update:** Refresh data

## Empty States

### No Data
```
┌──────────────────┐
│    [Icon]        │
│                  │
│  No items yet    │
│                  │
│  [Create Item]   │
└──────────────────┘
```

### No Search Results
```
┌───────────────────┐
│   [Search Icon]   │
│                   │
│ No results for    │
│ "search term"     │
│                   │
│ [Clear Search]    │
└───────────────────┘
```

### No Permission
```
┌────────────────────┐
│   [Lock Icon]      │
│                    │
│ Access Denied      │
│                    │
│ Contact admin to   │
│ request access.    │
└────────────────────┘
```

## Error States

### Validation Errors
- **Inline:** Red border + message below field
- **Summary:** Error list at top of form

### System Errors
```
┌──────────────────────┐
│  [Error Icon]        │
│                      │
│  Something went      │
│  wrong               │
│                      │
│  [Try Again]         │
│  [Report Issue]      │
└──────────────────────┘
```

### Network Errors
```
┌──────────────────────┐
│  [Offline Icon]      │
│                      │
│  No connection       │
│                      │
│  Check your network  │
│  and try again.      │
│                      │
│  [Retry]             │
└──────────────────────┘
```

## Copy & Microcopy

### Headings
- **H1 (Page Title):** "[Title]"
- **H2 (Section):** "[Section Name]"

### Button Labels
- **Primary Action:** "[Action Verb + Noun]" (e.g., "Save Changes")
- **Secondary Action:** "Cancel" / "Go Back"
- **Destructive Action:** "Delete [Item]"

### Confirmation Dialogs
```
Title: "Delete [Item Name]?"
Body: "This action cannot be undone. Are you sure?"
Buttons: [Cancel] [Delete]
```

### Success Messages
```
"✓ Changes saved successfully"
"✓ Item created"
"✓ Email sent"
```

### Error Messages
```
"✗ Unable to save changes. Please try again."
"✗ Invalid email format"
"✗ Server error. Contact support if this persists."
```

## Accessibility Requirements

### WCAG 2.1 Level AA Compliance

**Keyboard Navigation:**
- All interactive elements reachable by Tab
- Logical tab order
- Focus visible with 2px outline
- Escape closes modals/dropdowns

**Screen Reader:**
- All images have alt text
- Forms have proper labels
- Status messages announced
- Error messages associated with fields

**Color Contrast:**
- Text: Minimum 4.5:1 ratio
- Large text: Minimum 3:1 ratio
- UI components: Minimum 3:1 ratio

**Visual:**
- Text resizable to 200%
- No information conveyed by color alone
- Sufficient target size (44x44px minimum)

## Performance Budget

- **First Contentful Paint:** < 1.5s
- **Largest Contentful Paint:** < 2.5s
- **Time to Interactive:** < 3.5s
- **Cumulative Layout Shift:** < 0.1
- **Bundle Size:** < 200KB (gzipped)

## Browser Support

- **Desktop:** Chrome, Firefox, Safari, Edge (latest 2 versions)
- **Mobile:** iOS Safari, Chrome Android (latest 2 versions)
- **Degradation:** Functional without JavaScript (where possible)

## Localization

- **Text:** All user-facing text in i18n files
- **Dates/Times:** Locale-aware formatting
- **RTL Support:** Layout mirrors for Arabic/Hebrew
- **Number Formats:** Locale-specific (commas, decimals)

## Analytics & Tracking

**Events to Track:**
- Page view
- Button clicks: `[Button Label]_clicked`
- Form submissions: `form_submitted`
- Errors: `error_[type]`

**Properties:**
- User ID
- Session ID
- Feature variant (for A/B tests)
- Timestamp

## Testing Checklist

- [ ] **Visual QA:** Matches design in all breakpoints
- [ ] **Interaction:** All buttons/links work as expected
- [ ] **Forms:** Validation works, errors display correctly
- [ ] **Accessibility:** Keyboard navigation, screen reader tested
- [ ] **Performance:** Meets performance budget
- [ ] **Cross-browser:** Tested in all supported browsers
- [ ] **Responsive:** Mobile, tablet, desktop views correct
- [ ] **Loading:** Loading states display properly
- [ ] **Errors:** Error states handle gracefully
- [ ] **Empty:** Empty states show correctly

---

**Spec Version:** 1.0
**Last Updated:** [Date]
**Author:** [Name]
**Designer:** [Name]

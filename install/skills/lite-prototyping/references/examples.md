# lite-prototyping - Examples and Tips

## Tips for Effective Prototyping

**Start with paper/whiteboard first:**
- Sketch rough layout before touching code
- Saves time by eliminating obviously bad ideas
- Code only after rough direction is clear

**Focus on ONE risky interaction:**
- Don't prototype the entire feature
- Identify the uncertain part (e.g., "share flow")
- Build minimal prototype to test that one thing

**Use real content, not Lorem Ipsum:**
- Realistic data reveals layout issues
- "Recipe: Grandma's Chocolate Chip Cookies" beats "Item 1"
- Helps user imagine actual usage

**Mobile first, then scale up:**
- Start with 375px width (iPhone)
- Ensure core interaction works on small screen
- Add desktop styles after mobile validated

**Embrace ugly first drafts:**
- First iteration will look bad - that's fine
- User feedback fixes it quickly
- Perfection is the enemy of iteration speed

---

## Common Scenarios

### Scenario 1: Validating a Flow

```
User: "Prototype the recipe sharing flow"

Claude:
1. Asks: "What's the risky part?" → User: "Share button placement"
2. Generates: Simple HTML with share button in 3 different positions
3. Iterates: User tries each position, picks top-right
4. Adds: Confirmation toast, copy-to-clipboard
5. Extracts: Learnings to spec via /lite-prototype-to-spec
```

---

### Scenario 2: Comparing Two Approaches

```
User: "Should we use tabs or accordion for recipe sections?"

Claude:
1. Creates: recipe-tabs-v1/ with tabbed interface
2. User tests: "Tabs feel cramped on mobile"
3. Creates: recipe-tabs-v2/ with accordion
4. User tests: "Accordion is better, but collapse all by default"
5. Iterates: Changes accordion to collapsed state
6. User: "Perfect, use this"
```

---

### Scenario 3: Importing Existing Mockup

```
User: "I have a Figma export, can we iterate on it?"

Claude:
1. User provides: mockup.zip with HTML/CSS from Figma
2. Extracts to: .shipkit-mockups/figma-import-v1/
3. Opens in browser: Reviews with user
4. Iterates: Makes changes to spacing, colors, interactions
5. Logs: Each change in iterations.md
```

---

## Example Prototype Structure

### Simple Share Button Prototype (React + Tailwind)

**Complete single-file HTML prototype:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recipe Share Prototype</title>

    <!-- Tailwind CSS via CDN -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- React and ReactDOM via CDN -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>

    <!-- Babel for JSX support -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState } = React;

        function RecipeSharePrototype() {
            const [showToast, setShowToast] = useState(false);

            // Mock recipe data
            const recipe = {
                title: "Chocolate Chip Cookies",
                description: "Grandma's secret recipe...",
                link: "https://example.com/recipe/123"
            };

            const handleShare = () => {
                // Mock share functionality
                console.log('Copied:', recipe.link);

                // Show toast notification
                setShowToast(true);
                setTimeout(() => {
                    setShowToast(false);
                }, 2000);
            };

            return (
                <div className="min-h-screen bg-gray-50 p-6 flex items-center justify-center">
                    {/* Recipe Card */}
                    <div className="relative max-w-md w-full bg-white border border-gray-200 rounded-lg shadow-sm p-6">
                        {/* Share Button */}
                        <button
                            onClick={handleShare}
                            className="absolute top-4 right-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                        >
                            Share
                        </button>

                        {/* Recipe Content */}
                        <h1 className="text-2xl font-bold text-gray-900 mb-2">
                            {recipe.title}
                        </h1>
                        <p className="text-gray-600">
                            {recipe.description}
                        </p>
                    </div>

                    {/* Toast Notification */}
                    {showToast && (
                        <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2 bg-green-600 text-white px-6 py-3 rounded-md shadow-lg animate-fade-in">
                            Link copied!
                        </div>
                    )}
                </div>
            );
        }

        // Render to DOM
        ReactDOM.render(<RecipeSharePrototype />, document.getElementById('root'));
    </script>
</body>
</html>
```

### Key Features of This Example

- **React hooks** (`useState`) for toast visibility state
- **Tailwind utility classes** for all styling (no custom CSS)
- **Responsive design** built-in (`min-h-screen`, `max-w-md`)
- **Interactive state management** (click → show toast → hide after 2s)
- **Mock data** hardcoded (no API calls)
- **Single file** - works by double-clicking (CDN imports)

### Template Variations

**Multi-page flow (using conditional rendering):**
```javascript
const [currentStep, setCurrentStep] = useState(1);

// In render:
{currentStep === 1 && <Step1 onNext={() => setCurrentStep(2)} />}
{currentStep === 2 && <Step2 onNext={() => setCurrentStep(3)} />}
{currentStep === 3 && <Step3 />}
```

**Form with validation:**
```javascript
const [email, setEmail] = useState('');
const [error, setError] = useState('');

const handleSubmit = () => {
    if (!email.includes('@')) {
        setError('Invalid email');
        return;
    }
    // Process form
};
```

**List with filtering:**
```javascript
const [filter, setFilter] = useState('');
const filteredItems = mockData.filter(item =>
    item.name.toLowerCase().includes(filter.toLowerCase())
);
```

---

## When to Use Which Pattern

**Simple interaction** → Single component, minimal state
**Multi-step flow** → Conditional rendering with step state
**Form** → Controlled inputs with validation state
**List/Grid** → Map over mock data array
**Navigation** → Conditional rendering (not React Router)

---

**Remember:** Prototypes are disposable. Focus on learning, not code quality.

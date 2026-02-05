# Prototyping Examples

**Purpose**: Copy-pasteable React + Tailwind templates for common UI patterns

---

## Example 1: Share Button with Toast Notification

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Share Button Prototype</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body class="bg-gray-100 min-h-screen p-8">
  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect } = React;

    function Toast({ message, onClose }) {
      useEffect(() => {
        const timer = setTimeout(onClose, 3000);
        return () => clearTimeout(timer);
      }, [onClose]);

      return (
        <div className="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-2 animate-pulse">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          {message}
        </div>
      );
    }

    function ShareButton({ url }) {
      const [toast, setToast] = useState(null);

      const handleShare = async () => {
        try {
          await navigator.clipboard.writeText(url);
          setToast('Link copied to clipboard!');
        } catch (err) {
          // Fallback for older browsers
          const textArea = document.createElement('textarea');
          textArea.value = url;
          document.body.appendChild(textArea);
          textArea.select();
          document.execCommand('copy');
          document.body.removeChild(textArea);
          setToast('Link copied!');
        }
      };

      return (
        <>
          <button
            onClick={handleShare}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
            </svg>
            Share
          </button>
          {toast && <Toast message={toast} onClose={() => setToast(null)} />}
        </>
      );
    }

    function App() {
      return (
        <div className="max-w-md mx-auto bg-white rounded-xl shadow-md p-6">
          <h1 className="text-xl font-bold mb-4">Share This Page</h1>
          <p className="text-gray-600 mb-4">Click the button to copy the link to your clipboard.</p>
          <ShareButton url={window.location.href} />
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
```

---

## Example 2: Multi-Step Wizard

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Multi-Step Wizard Prototype</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body class="bg-gray-100 min-h-screen p-8">
  <div id="root"></div>

  <script type="text/babel">
    const { useState } = React;

    const STEPS = [
      { id: 1, title: 'Account', description: 'Create your account' },
      { id: 2, title: 'Profile', description: 'Tell us about yourself' },
      { id: 3, title: 'Preferences', description: 'Customize your experience' },
      { id: 4, title: 'Complete', description: 'All done!' },
    ];

    function StepIndicator({ steps, currentStep }) {
      return (
        <div className="flex items-center justify-between mb-8">
          {steps.map((step, index) => (
            <div key={step.id} className="flex items-center">
              <div className={`
                w-10 h-10 rounded-full flex items-center justify-center font-bold
                ${currentStep >= step.id ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-500'}
              `}>
                {currentStep > step.id ? '✓' : step.id}
              </div>
              {index < steps.length - 1 && (
                <div className={`w-16 h-1 mx-2 ${currentStep > step.id ? 'bg-blue-500' : 'bg-gray-200'}`} />
              )}
            </div>
          ))}
        </div>
      );
    }

    function Step1({ data, onChange, onNext }) {
      return (
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Create Account</h2>
          <input
            type="email"
            placeholder="Email"
            value={data.email || ''}
            onChange={(e) => onChange({ ...data, email: e.target.value })}
            className="w-full p-3 border rounded-lg"
          />
          <input
            type="password"
            placeholder="Password"
            value={data.password || ''}
            onChange={(e) => onChange({ ...data, password: e.target.value })}
            className="w-full p-3 border rounded-lg"
          />
          <button onClick={onNext} className="w-full bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600">
            Continue
          </button>
        </div>
      );
    }

    function Step2({ data, onChange, onNext, onBack }) {
      return (
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Your Profile</h2>
          <input
            type="text"
            placeholder="Full Name"
            value={data.name || ''}
            onChange={(e) => onChange({ ...data, name: e.target.value })}
            className="w-full p-3 border rounded-lg"
          />
          <textarea
            placeholder="Bio"
            value={data.bio || ''}
            onChange={(e) => onChange({ ...data, bio: e.target.value })}
            className="w-full p-3 border rounded-lg"
            rows={3}
          />
          <div className="flex gap-3">
            <button onClick={onBack} className="flex-1 border py-3 rounded-lg hover:bg-gray-50">Back</button>
            <button onClick={onNext} className="flex-1 bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600">Continue</button>
          </div>
        </div>
      );
    }

    function Step3({ data, onChange, onNext, onBack }) {
      return (
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Preferences</h2>
          <label className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
            <input
              type="checkbox"
              checked={data.newsletter || false}
              onChange={(e) => onChange({ ...data, newsletter: e.target.checked })}
              className="w-5 h-5"
            />
            <span>Subscribe to newsletter</span>
          </label>
          <label className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
            <input
              type="checkbox"
              checked={data.darkMode || false}
              onChange={(e) => onChange({ ...data, darkMode: e.target.checked })}
              className="w-5 h-5"
            />
            <span>Enable dark mode</span>
          </label>
          <div className="flex gap-3">
            <button onClick={onBack} className="flex-1 border py-3 rounded-lg hover:bg-gray-50">Back</button>
            <button onClick={onNext} className="flex-1 bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600">Complete</button>
          </div>
        </div>
      );
    }

    function Step4({ data }) {
      return (
        <div className="text-center space-y-4">
          <div className="text-6xl">🎉</div>
          <h2 className="text-xl font-bold">All Done!</h2>
          <p className="text-gray-600">Welcome, {data.name || data.email}!</p>
          <pre className="text-left bg-gray-100 p-4 rounded-lg text-sm overflow-auto">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      );
    }

    function Wizard() {
      const [step, setStep] = useState(1);
      const [data, setData] = useState({});

      const renderStep = () => {
        switch (step) {
          case 1: return <Step1 data={data} onChange={setData} onNext={() => setStep(2)} />;
          case 2: return <Step2 data={data} onChange={setData} onNext={() => setStep(3)} onBack={() => setStep(1)} />;
          case 3: return <Step3 data={data} onChange={setData} onNext={() => setStep(4)} onBack={() => setStep(2)} />;
          case 4: return <Step4 data={data} />;
        }
      };

      return (
        <div className="max-w-lg mx-auto bg-white rounded-xl shadow-md p-6">
          <StepIndicator steps={STEPS} currentStep={step} />
          {renderStep()}
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<Wizard />);
  </script>
</body>
</html>
```

---

## Example 3: Form with Validation

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Form Validation Prototype</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body class="bg-gray-100 min-h-screen p-8">
  <div id="root"></div>

  <script type="text/babel">
    const { useState } = React;

    function validateEmail(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function validatePassword(password) {
      const errors = [];
      if (password.length < 8) errors.push('At least 8 characters');
      if (!/[A-Z]/.test(password)) errors.push('One uppercase letter');
      if (!/[a-z]/.test(password)) errors.push('One lowercase letter');
      if (!/[0-9]/.test(password)) errors.push('One number');
      return errors;
    }

    function Input({ label, type, value, onChange, error, hint }) {
      return (
        <div className="space-y-1">
          <label className="block text-sm font-medium text-gray-700">{label}</label>
          <input
            type={type}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className={`w-full p-3 border rounded-lg ${error ? 'border-red-500 bg-red-50' : 'border-gray-300'}`}
          />
          {error && <p className="text-red-500 text-sm">{error}</p>}
          {hint && !error && <p className="text-gray-500 text-sm">{hint}</p>}
        </div>
      );
    }

    function PasswordStrength({ password }) {
      const errors = validatePassword(password);
      const strength = 4 - errors.length;
      const colors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-green-500'];

      return (
        <div className="space-y-2">
          <div className="flex gap-1">
            {[0, 1, 2, 3].map((i) => (
              <div key={i} className={`h-2 flex-1 rounded ${i < strength ? colors[strength - 1] : 'bg-gray-200'}`} />
            ))}
          </div>
          {errors.length > 0 && (
            <ul className="text-sm text-gray-500">
              {errors.map((err, i) => (
                <li key={i} className="flex items-center gap-1">
                  <span className="text-red-500">✗</span> {err}
                </li>
              ))}
            </ul>
          )}
        </div>
      );
    }

    function Form() {
      const [form, setForm] = useState({ email: '', password: '', confirm: '' });
      const [errors, setErrors] = useState({});
      const [submitted, setSubmitted] = useState(false);

      const validate = () => {
        const newErrors = {};
        if (!form.email) newErrors.email = 'Email is required';
        else if (!validateEmail(form.email)) newErrors.email = 'Invalid email format';

        if (!form.password) newErrors.password = 'Password is required';
        else if (validatePassword(form.password).length > 0) newErrors.password = 'Password too weak';

        if (form.password !== form.confirm) newErrors.confirm = 'Passwords do not match';

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
      };

      const handleSubmit = (e) => {
        e.preventDefault();
        if (validate()) {
          setSubmitted(true);
        }
      };

      if (submitted) {
        return (
          <div className="max-w-md mx-auto bg-white rounded-xl shadow-md p-6 text-center">
            <div className="text-6xl mb-4">✅</div>
            <h2 className="text-xl font-bold">Account Created!</h2>
            <p className="text-gray-600">Welcome aboard, {form.email}</p>
          </div>
        );
      }

      return (
        <form onSubmit={handleSubmit} className="max-w-md mx-auto bg-white rounded-xl shadow-md p-6 space-y-4">
          <h2 className="text-xl font-bold">Create Account</h2>

          <Input
            label="Email"
            type="email"
            value={form.email}
            onChange={(v) => setForm({ ...form, email: v })}
            error={errors.email}
          />

          <div className="space-y-1">
            <Input
              label="Password"
              type="password"
              value={form.password}
              onChange={(v) => setForm({ ...form, password: v })}
              error={errors.password}
            />
            {form.password && <PasswordStrength password={form.password} />}
          </div>

          <Input
            label="Confirm Password"
            type="password"
            value={form.confirm}
            onChange={(v) => setForm({ ...form, confirm: v })}
            error={errors.confirm}
          />

          <button type="submit" className="w-full bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600">
            Create Account
          </button>
        </form>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<Form />);
  </script>
</body>
</html>
```

---

## Example 4: Dynamic List with Add/Remove

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dynamic List Prototype</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body class="bg-gray-100 min-h-screen p-8">
  <div id="root"></div>

  <script type="text/babel">
    const { useState } = React;

    function TodoList() {
      const [items, setItems] = useState([
        { id: 1, text: 'Learn React', done: true },
        { id: 2, text: 'Build prototype', done: false },
        { id: 3, text: 'Ship feature', done: false },
      ]);
      const [newItem, setNewItem] = useState('');

      const addItem = () => {
        if (!newItem.trim()) return;
        setItems([...items, { id: Date.now(), text: newItem, done: false }]);
        setNewItem('');
      };

      const toggleItem = (id) => {
        setItems(items.map(item =>
          item.id === id ? { ...item, done: !item.done } : item
        ));
      };

      const removeItem = (id) => {
        setItems(items.filter(item => item.id !== id));
      };

      const doneCount = items.filter(i => i.done).length;

      return (
        <div className="max-w-md mx-auto bg-white rounded-xl shadow-md p-6">
          <h2 className="text-xl font-bold mb-4">Todo List</h2>

          {/* Add new item */}
          <div className="flex gap-2 mb-4">
            <input
              type="text"
              value={newItem}
              onChange={(e) => setNewItem(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && addItem()}
              placeholder="Add new item..."
              className="flex-1 p-3 border rounded-lg"
            />
            <button
              onClick={addItem}
              className="bg-blue-500 text-white px-4 rounded-lg hover:bg-blue-600"
            >
              Add
            </button>
          </div>

          {/* Progress */}
          <div className="mb-4">
            <div className="flex justify-between text-sm text-gray-500 mb-1">
              <span>{doneCount} of {items.length} completed</span>
              <span>{Math.round((doneCount / items.length) * 100) || 0}%</span>
            </div>
            <div className="h-2 bg-gray-200 rounded-full">
              <div
                className="h-2 bg-green-500 rounded-full transition-all"
                style={{ width: `${(doneCount / items.length) * 100 || 0}%` }}
              />
            </div>
          </div>

          {/* List */}
          <ul className="space-y-2">
            {items.map(item => (
              <li
                key={item.id}
                className={`flex items-center gap-3 p-3 border rounded-lg ${item.done ? 'bg-gray-50' : ''}`}
              >
                <input
                  type="checkbox"
                  checked={item.done}
                  onChange={() => toggleItem(item.id)}
                  className="w-5 h-5"
                />
                <span className={`flex-1 ${item.done ? 'line-through text-gray-400' : ''}`}>
                  {item.text}
                </span>
                <button
                  onClick={() => removeItem(item.id)}
                  className="text-red-500 hover:text-red-700 p-1"
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>

          {items.length === 0 && (
            <p className="text-center text-gray-400 py-8">No items yet. Add one above!</p>
          )}
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<TodoList />);
  </script>
</body>
</html>
```

---

## Tips for Effective Prototyping

1. **Mobile-first**: Start with `max-w-md mx-auto` to constrain width
2. **Real content**: Use realistic data, not "Lorem ipsum"
3. **One interaction**: Focus on validating ONE user flow per prototype
4. **Visible state**: Show state changes clearly (colors, animations, counters)
5. **Error states**: Include what happens when things go wrong
6. **Loading states**: Show spinners/skeletons during async operations

---

## Common Patterns Cheatsheet

| Pattern | Key React Hooks | Tailwind Classes |
|---------|-----------------|------------------|
| Form | `useState` for each field | `space-y-4`, `p-3 border rounded-lg` |
| List | `useState` with array, `map()` | `space-y-2`, `flex items-center gap-3` |
| Modal | `useState` for open/close | `fixed inset-0`, `bg-black/50` |
| Toast | `useState` + `useEffect` timer | `fixed bottom-4 right-4`, `animate-pulse` |
| Tabs | `useState` for active tab | Conditional `border-b-2 border-blue-500` |
| Wizard | `useState` for step number | Step indicator with `rounded-full` |

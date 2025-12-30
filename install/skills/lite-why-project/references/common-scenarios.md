# Common Scenarios

## Scenario 1: Brand New Project

```
User: "Define the project vision"

Claude:
1. Check: why.md doesn't exist
2. Ask Question 1: "Who is this for?"
3. User: "Solo developers learning React"
4. Ask Question 2: "Why does this exist?"
5. User: "I need a real project to learn React hooks and state management"
6. Ask Question 3: "Where are we now?"
7. User: "Just started, have basic setup"
8. Ask Question 4: "Where do we need to be?"
9. User: "Working app I can show in portfolio, well-documented code I can reference later"
10. Ask Question 5: "How are we getting there?"
11. User: "Build feature by feature, document each pattern as I learn it"
12. Ask: Constraints/priorities?
13. User: "Priority: learning over shipping fast"
14. Write: why.md with all answers
15. Confirm: "Vision defined. Will auto-load at session start."
```

---

## Scenario 2: Updating Existing Vision

```
User: "Update the project vision"

Claude:
1. Check: why.md exists
2. Ask: "Vision exists. View, Update, or Cancel?"
3. User: "Update"
4. Read: old why.md
5. Ask Question 1: "Who is this for?"
   Show: "Current: Solo developers learning React"
   Ask: "Has this changed?"
6. User: "Now for small dev teams at startups"
7. Ask Questions 2-5 (showing old answers, asking for changes)
8. User updates answers 1 and 4, keeps others
9. Ask: Constraints/priorities?
10. User keeps old constraints
11. Write: why.md (preserve Created date, update Last Updated)
12. Confirm: Updated vision shown
```

---

## Scenario 3: Mid-Session Suggestion

```
[Session starts]
lite-session-start.py: "📝 No project vision found. Run /lite-why-project to define who/why/where"

User: "Scan my project"
Claude: Runs /lite-project-context

User: "Should I use TypeScript or JavaScript?"
Claude: "Before I recommend, would you like to run /lite-why-project?
         Knowing your goals (learning vs shipping, team size, priorities)
         will help me give you a better answer."

User: "/lite-why-project"
Claude: [Runs through 5 questions]
Claude: "Now that I know this is a learning project with priority on
         understanding fundamentals, I'd recommend starting with JavaScript.
         Once you're comfortable, add TypeScript to learn type systems."
```

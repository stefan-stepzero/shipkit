# Skill Routing Tables (Keyword Fallback)

These tables serve as **fallback** for explicit keyword-matched requests. The loop dispatch system handles ambiguous/open-ended requests; routing tables handle explicit ones.

## Vision & Discovery

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Define vision", "Why this project?", "Project goals" | `/shipkit-why-project` | .shipkit/why.json |
| "Who are our users?", "Create personas", "User research", "User journey" | `/shipkit-product-discovery` | .shipkit/why.json, stack.json |
| "Define solution", "Product definition", "What to build", "Features", "Differentiators" | `/shipkit-product-definition` | .shipkit/product-discovery.json, why.json |
| "Technical approach", "Engineering design", "How to build", "Mechanisms", "Components" | `/shipkit-engineering-definition` | .shipkit/product-definition.json, stack.json |
| "Design system", "Design tokens", "Brand guidelines", "Visual direction", "Design principles" | `/shipkit-design-system` | .shipkit/why.json, product-discovery.json, engineering-definition.json |
| "Set stage", "Project stage", "Constraints", "Graduation" | `/shipkit-stage` | .shipkit/goals/strategic.json |
| "Success criteria", "Measure success", "Product goals" | `/shipkit-product-goals` | .shipkit/product-definition.json |
| "Engineering goals", "Technical criteria", "SLAs", "Performance targets" | `/shipkit-engineering-goals` | .shipkit/engineering-definition.json |

## Context & Status

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Scan project", "Generate stack", "What's my tech stack?" | `/shipkit-project-context` | package.json, .env.example |
| "Index codebase", "Map project", "Create index", "Update index" | `/shipkit-codebase-index` | None (generates from git) |
| "Log progress", "Session summary", "What did we do?", "Checkpoint", "Save state", "End session" | `/shipkit-work-memory` | .shipkit/progress.json |
| "Help", "What skills exist?", "What can you do?" | List all shipkit skills | None |
| "Find skills", "Get skills", "Is there a skill for?", "Install skill" | `/shipkit-get-skills` | None |
| "Find MCPs", "Get MCPs", "Is there an MCP for?", "Install MCP" | `/shipkit-get-mcps` | .mcp.json |
| "Install Shipkit", "Update Shipkit", "Upgrade Shipkit", "Reinstall Shipkit" | `/shipkit-update` | None |

## Specification & Planning

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "What to spec first", "Spec roadmap", "Prioritize features", "Spec backlog" | `/shipkit-spec-roadmap` | product-definition.json, engineering-definition.json, goals/ |
| "Spec this feature", "Create specification", "Write requirements" | `/shipkit-spec` | .shipkit/specs/todo/ |
| "Triage feedback", "Process bug reports", "User testing feedback" | `/shipkit-feedback-bug` | .shipkit/specs/{todo,active}/, codebase-index |
| "Plan this", "How to implement?", "Create plan" | `/shipkit-plan` | specs/{todo,active}/, stack.json, architecture.json |
| "Help me think through", "Think with me", "Let's discuss", "What am I missing?" | `/shipkit-thinking-partner` | .shipkit/why.json, architecture.json |
| "Devil's advocate", "Pre-mortem", "Trade-offs", "I'm torn between" | `/shipkit-thinking-partner` | .shipkit/why.json, architecture.json |

## Knowledge Persistence

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Remember this", "Save this", "Update CLAUDE.md", "Add to CLAUDE.md" | `/shipkit-claude-md` | CLAUDE.md |

## Quality & Communication

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Verify", "Check my work", "Ready to commit?", "Review changes" | `/shipkit-review-shipping` | Git diff, specs, architecture |
| "Preflight", "Production ready", "Ready to ship?", "Go live", "Launch check" | `/shipkit-preflight` | stack.json, why.json, architecture.json |
| "Scale ready", "Enterprise ready", "Scale audit", "Observability", "Reliability" | `/shipkit-scale-ready` | stack.json, architecture.json |
| "Audit UX", "Check UX patterns", "UX gaps" | `/shipkit-ux-audit` | implementations/ |
| "Create task", "Track TODO", "User tasks" | `/shipkit-user-instructions` | user-tasks/active.md |
| "Visualize", "HTML report", "Visual communication" | `/shipkit-communications` | Relevant files based on request |
| "Audit prompts", "Prompt architecture", "LLM pipeline review", "Check my prompts" | `/shipkit-prompt-audit` | stack.json, architecture.json |
| "Semantic QA", "Quality check", "Judge outputs", "QA suite", "Run QA" | `/shipkit-semantic-qa` | .shipkit/semantic-qa/config.json |
| "Visual QA", "UI testing", "Screenshot test", "Check the UI", "Playwright", "Test UI goals" | `/shipkit-qa-visual` | .shipkit/ui-goals.json |

## Execution

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Test cases", "Generate tests", "What to test", "Test coverage", "Test specification" | `/shipkit-test-cases` | Source files, specs, existing test cases |

## What Doesn't Need a Skill

| User Says | Just Do It |
|-----------|------------|
| "Build this", "Implement", "Start coding" | Implement using spec/plan |
| "Bug", "Error", "Not working", "Broken" | Debug systematically |
| "Write tests" | Write tests alongside code |
| "Document this code" | Add comments/docstrings |
| "Refactor this" | Refactor as requested |

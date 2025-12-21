# Dev Specify References

This folder contains extended guidance for creating feature specifications.

## Built-in References

### reference.md
Comprehensive guide covering:
- What makes a good spec (clear, measurable, testable)
- Extracting from product artifacts (user stories, interaction design, brand, JTBD, metrics, constitution)
- Template sections explained (all 12 sections)
- Spec quality checklist
- Common mistakes to avoid
- Using [NEEDS_CLARIFICATION] markers
- Working with --clarify and --update flags

### examples.md
Two complete specification examples:
- **Simple:** Dark Mode Toggle (~600 words)
- **Complex:** Real-Time Collaborative Editing (~1200 words)

Plus an anti-example showing what NOT to do.

## How Claude Uses These

When you run `/dev-specify`, Claude will:
1. Read all files in this folder
2. Read product artifacts (user stories, interaction design, brand, constitution)
3. Use the template from `../templates/spec-template.md`
4. Guide you through creating a complete, grounded specification

## Add Your Own References

Drop files here to customize guidance:

```
references/
├── reference.md              # Built-in
├── examples.md               # Built-in
├── README.md                 # This file
├── our-spec-checklist.md     # Your team's review checklist
├── regulatory-reqs.pdf       # Compliance requirements for specs
└── api-standards.md          # Your API design standards
```

Claude reads ALL files in this folder, so you can add:
- Team's spec review checklist
- Regulatory/compliance templates
- Domain-specific requirements (healthcare, fintech, etc.)
- Examples from your past projects

## Key Principles

1. **Extract, don't invent** - Requirements come from product artifacts
2. **High-level, not implementation** - Defer technical decisions to dev-plan
3. **Testable** - Every requirement has clear acceptance criteria (Given-When-Then)
4. **Complete** - Address edge cases, errors, non-functionals
5. **Use clarification markers** - [NEEDS_CLARIFICATION: ...] for ambiguities

## Workflow

```
/dev-specify "Feature description"
  → Creates specs/N-feature-name/spec.md from template
  → Claude reads product artifacts
  → Fills spec conversationally
  → May include [NEEDS_CLARIFICATION] markers

/dev-specify --clarify --spec N-feature-name
  → Finds [NEEDS_CLARIFICATION] markers
  → Asks questions interactively
  → Updates spec with answers

/dev-specify --update --spec N-feature-name
  → Archives old version
  → Updates spec with new information
```

---

**Remember:** Specs are grounded in product artifacts, not invented from scratch!

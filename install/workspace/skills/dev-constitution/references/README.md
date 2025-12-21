# Dev Constitution References

This folder contains extended guidance for creating technical constitutions.

## Built-in References

### reference.md
Comprehensive guide covering:
- What goes in a constitution (5 sections)
- Token efficiency strategies (<500 words target)
- How to extract from product artifacts
- Usage in dev workflow
- Quick checklist

### examples.md
Three complete constitution examples:
- **POC** - AI Meeting Summarizer (speed-focused)
- **MVP** - SaaS Task Manager (balanced)
- **Established** - Fintech Platform (compliance-heavy)

Plus anti-examples showing what NOT to do.

## How Claude Uses These

When you run `/dev-constitution`, Claude will:
1. Read all files in this folder
2. Read product artifacts (user stories, strategy, metrics)
3. Use the template from `../templates/constitution-template.md`
4. Guide you through creating a lean, product-aware constitution

## Add Your Own References

Drop files here to customize guidance:

```
references/
├── reference.md         # Built-in
├── examples.md          # Built-in
├── README.md            # This file
├── our-tech-stack.md    # Your team's standard stack
├── security-reqs.pdf    # Your company's security policy
└── architecture-adrs/   # Your architectural decision records
```

Claude reads ALL files in this folder, so you can add:
- Company coding standards
- Compliance requirements
- Team conventions
- Architectural patterns you prefer
- Anti-patterns to avoid

## Key Principles

1. **LEAN** - Target <500 words total in final constitution
2. **HIGH-LEVEL** - Principles, not implementation details
3. **PRODUCT-AWARE** - Grounded in your product artifacts
4. **STAGE-APPROPRIATE** - POC vs MVP vs Established have different needs

---

**Remember:** Constitution is consumed by ALL dev skills (specify, plan, tasks, implement), so keep it token-efficient!

# dev-plan - Extended References

This folder contains extended documentation for the dev-plan skill.

---

## Files in This Folder

### reference.md (2000+ words)
**Comprehensive planning guide covering:**
- Constitution-driven design principles
- Research-first methodology (Phase 0)
- Design and contract generation (Phase 1)
- Architecture decision framework
- Performance, security, and testing strategies
- Common pitfalls and quality checklist

**Use this for:**
- Understanding the planning philosophy
- Learning how to resolve unknowns through research
- Creating comprehensive technical designs
- Validating against constitution standards

### examples.md
**Concrete planning examples including:**
- Example 1: User Authentication (backend feature)
- Example 2: Product Catalog (full-stack with search)
- Example 3: Payment Integration (external service)
- Example 4: Real-Time Notifications (WebSocket + Redis)
- Example 5: Data Export (background jobs)

**Each example shows:**
- Plan summary with constitution check
- Research documentation with decision rationale
- Data model design with indexes
- API contracts (OpenAPI/GraphQL)
- Security and performance considerations
- Error handling strategies

**Use this for:**
- Seeing complete planning artifacts
- Understanding decision documentation patterns
- Learning from different feature types
- Reference when planning similar features

---

## Adding Your Own References

Feel free to add to this folder:

### Research Papers
- PDFs from technical research
- Benchmark results
- Architecture decision records (ADRs)

### Links and Articles
- `links.md` - Curated list of useful resources
- API documentation references
- Best practice guides

### Team Knowledge
- `patterns.md` - Company-specific patterns
- `lessons-learned.md` - Post-mortems and insights
- `faq.md` - Common planning questions

### Templates and Variations
- Custom plan templates for your domain
- API contract examples specific to your stack
- Data model patterns for your architecture

---

## When Claude Runs dev-plan

**Claude will automatically read:**
1. All `.md` files in this references/ folder
2. The plan templates from templates/
3. The spec from dev-specify outputs
4. The constitution from dev-constitution outputs

**Claude uses these references to:**
- Understand planning best practices
- Learn from examples
- Follow established patterns
- Validate decisions against constitution

---

## Tips for Extending References

### Keep It Actionable
- Include concrete examples, not just theory
- Show actual code snippets where helpful
- Link to real documentation

### Organize by Topic
- Create subfolders for complex topics
- Name files descriptively
- Cross-reference between documents

### Update After Each Project
- Add new patterns discovered
- Document what worked well
- Note what to avoid next time

### Version Control
- Commit updates to references
- Tag significant improvements
- Document breaking changes to patterns

---

## Questions?

If these references don't cover your planning scenario:

1. **Check examples.md** - See if similar feature type exists
2. **Review reference.md** - Follow the framework for your domain
3. **Add your own example** - Document your plan as a reference for next time

---

**Remember**: Great plans set up great implementations. Invest time upfront in thorough planning to save time during development.

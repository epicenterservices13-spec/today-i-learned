# TIL vs. Learning Journal Cognitive Taxonomy

Enforce architectural separation between atomic tactical TIL entries and reflective, longitudinal Learning Journal synthesis.

## Context

Blurring quick tactical snippets with long-form reflections creates index bloat and cognitive friction. Systemic workspace health requires distinct repositories and directory scopes for immediate discovery versus retrospective synthesis.

## Implementation / Code

```bash
# Tactical micro-writeups (commands, syntax, bug fixes)
# Target: ~/10_DEV/11_PROJECTS/today-i-learned/
cat << 'EOF' > ~/10_DEV/11_PROJECTS/today-i-learned/arch/sample.md
# Title
Brief summary.
## Context
...
## Implementation / Code
...
## Takeaways
...
EOF

# Strategic metacognitive logs (daily reviews, architecture roadmaps)
# Target: ~/30_DOCS/32_LEARNING_JOURNAL/YYYYMMDD/
cat << 'EOF' > ~/30_DOCS/32_LEARNING_JOURNAL/$(date +%Y%m%d)/session.md
# Session Codex
...
EOF
```

## Takeaways

- TILs are atomic, isolated, and rapidly searchable reference cards.
- Learning Journals capture narrative problem solving, philosophical arcs, and multi-tool workflows.
- Never mix raw command notes into long-term learning journals; route each payload to its canonical sector.

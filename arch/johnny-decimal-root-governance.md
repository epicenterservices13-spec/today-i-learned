# Zero Root Clutter via Johnny Decimal Governance

Impose order on home directory file chaos by partitioning workloads into canonical numbered decimal sectors.

## Context

Unmanaged root directories (`$HOME`) quickly become dumping grounds for temporary logs, stray git clones, test scripts, and downloaded packages. A strict sector taxonomy stops entropy before it spreads.

## Implementation / Code

```text
00-09 | INTAKE       -> 00_INBOX (01_RAW, 02_PROCESSING, 03_SCRATCH, 04_TRIAGE)
10-19 | CODE & TOOLS -> 10_DEV (11_PROJECTS, 14_TOOLS, colab-books)
20-29 | ASSETS       -> 20_MEDIA (21_SOUNDTRACK, 23_CLIPS, 25_PRODUCTION, 26_ASSETS)
30-39 | KNOWLEDGE    -> 30_DOCS (31_FILES, 32_LEARNING_JOURNAL, 39_PRODUCTS)
40-49 | ENTERPRISE   -> 40_BUSINESS (41_FINANCE, 42_CONTRACTS, 43_CLIENTS)
50-59 | OPERATIONS   -> 50_OPS (51_SCRIPTS, 54_QUARANTINE, logs)
55-59 | PLATFORM     -> 55_INFRA (dotfiles, configs, builtin-skills)
60-69 | SCAFFOLDING  -> 60_TEMPLATES (61_PROJECT_INSTRUCTIONS, 62_TEMPLATES)
70-79 | RESTORATION  -> 70_BACKUPS (71_GOOGLE, 72_ANDROID, 75_PROOT)
80-89 | RETENTION    -> 80_ARCHIVE (82_COLD, 85_LEGACY)
90-99 | SECURITY     -> 90_VAULT (91_KEYS, 92_CREDENTIALS) [chmod 700]
99    | EGRESS       -> 99_OUTBOX (finalized exports, PRoot bridges)
```

## Takeaways

- Only numbered sectors, `storage/`, `bin/`, `AGENTS.md`, and `README.md` may exist at root.
- Dotfiles must be symlinks pointing into canonical `55_INFRA/dotfiles/`.
- No orphan files survive at `$HOME`.

# Single-File Atomic Commits in Git

Stage and commit exactly one file per commit to maintain deterministic git histories and simplify git bisect and cherry-picking.

## Context

Batch commits bundling multiple unrelated changes obscure regression origins, make rollbacks messy, and prevent atomic cherry-picks across staging and production branches.

## Implementation / Code

```bash
# Bad: Batch staging masking individual module intents
git add . && git commit -m "misc updates"

# Good: Atomic stage and commit per file
git add src/core/auth.py && git commit -m "src/core/auth.py: enforce token expiry validation"
git add tests/test_auth.py && git commit -m "tests/test_auth.py: add unit test for token expiry"
```

## Takeaways

- Commit messages must begin with `<filepath>: <clear intent>`.
- Isolate functional logic from test additions or configuration adjustments.
- Rollbacks become trivial: `git revert <commit-hash>` targets only the affected file.

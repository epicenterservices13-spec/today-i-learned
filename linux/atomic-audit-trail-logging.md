# Atomic Audit Trail Logging for Filesystem Mutations

Enforce accountability on cross-sector filesystem operations (`mv`, `cp`, `rm`, `rmdir`) by logging a structured CSV entry in the exact same step.

## Context

Automated agents and scripts frequently modify directory structures. Without an immutable append-only ledger, misplaced files or unintended deletions become impossible to reconstruct.

## Implementation / Code

```bash
#!/usr/bin/env bash
set -euo pipefail

LOG="$HOME/50_OPS/logs/file_moves.csv"
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SRC="/data/data/com.termux/files/home/downloads"
DEST="/data/data/com.termux/files/home/00_INBOX/01_RAW/downloads"
REASON="taxonomy: purge root clutter incoming drops to 01_RAW"

# Execute move and append to audit log in the same step
mv "$SRC" "$DEST"
echo "\"$TS\",\"mv\",\"$SRC\",\"$DEST\",\"$REASON\"" >> "$LOG"
```

## Takeaways

- Format: `"timestamp","action","src","dest","reason"`.
- Use UTC timestamps (`date -u +"%Y-%m-%dT%H:%M:%SZ"`) to prevent timezone drift across remotes.
- Both the filesystem action and log write must succeed atomically or fail together.

# Fail-Fast Shell Scripts with set -euo pipefail

Eliminate silent script failures and masked pipeline errors using strict execution flags.

## Context

By default, Bash proceeds after errors, treats unset variables as empty strings, and only returns the exit code of the final command in a pipeline. In automation and backup workflows, this often results in catastrophic silent failures.

## Implementation / Code

```bash
#!/usr/bin/env bash
set -euo pipefail

# -e: Exit immediately if any command exits with a non-zero status
# -u: Treat unset variables as an error and exit immediately
# -o pipefail: Pipeline return status is that of the last command to fail

# Example of trapped failure in pipeline:
cat non_existent_file.txt | grep "pattern" | wc -l
# Without pipefail, the above returns 0 (from wc -l), masking the missing file error.
# With pipefail, the script exits immediately with the error code from cat.
```

## Takeaways

- Start every non-trivial bash utility with `set -euo pipefail`.
- Use `${VAR:-default}` syntax when a variable is intentionally optional.

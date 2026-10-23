# Standard Stream Redirection and /dev/null Descriptor Mechanics

Understand POSIX stream redirection order and descriptor mapping to silence stdout, stderr, or both without leaking console errors.

## Context

Pipelines and automated jobs often need to suppress noisy tool diagnostics or trap standard errors without discarding standard output. Confusion regarding file descriptor evaluation order leads to leaking error streams (such as `2>&1 > /dev/null`) because redirections execute sequentially from left to right.

## Implementation / Code

```bash
# File Descriptors:
# 0 = stdin
# 1 = stdout (standard output, default for '>')
# 2 = stderr (standard error)

# Silence standard output only (errors still display on screen):
command > /dev/null

# Silence standard error only (normal output still displays):
command 2> /dev/null

# POSIX-compliant full suppression (silences stdout AND stderr):
command > /dev/null 2>&1
# Order matters: stdout (1) is redirected to /dev/null first;
# then stderr (2) is pointed to wherever stdout (1) currently points.

# Modern Bash shorthand (not supported in strict POSIX sh):
command &> /dev/null

# The fatal ordering error:
command 2>&1 > /dev/null
# Here, stderr (2) copies stdout (terminal), THEN stdout (1) moves to /dev/null.
# Result: stderr continues printing directly to the terminal!
```

## Takeaways

- Redirections evaluate strictly from left to right.
- In `command > /dev/null 2>&1`, the destination `/dev/null` must be bound to FD 1 before copying FD 1 to FD 2.
- Prefer `> /dev/null 2>&1` in scripts for maximum portability across Alpine, Dash, BusyBox, and Bash.

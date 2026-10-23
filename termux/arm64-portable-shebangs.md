# Portable Shebangs in Android Termux ARM64 Environments

Avoid hardcoding `/bin/bash` or `/usr/bin/python3` in script shebangs when operating across standard Linux distributions and Termux.

## Context

Android does not place system binaries in standard `/bin` or `/usr/bin` locations. In Termux, binaries reside under `/data/data/com.termux/files/usr/bin`. Hardcoded paths break portability between Termux, PRoot Debian/Ubuntu containers, and cloud environments.

## Implementation / Code

```bash
# Inflexible: fails on Termux unless termux-exec is active
#!/bin/bash
#!/usr/bin/python3

# Portable: resolved dynamically via $PATH
#!/usr/bin/env bash
#!/usr/bin/env python3
```

Ensure the file permissions are marked executable:
```bash
chmod +x scripts/my_script.py
```

## Takeaways

- Always prefer `#!/usr/bin/env <interpreter>`.
- Keep arguments out of the shebang line on Linux/Termux where multi-argument env is non-standard.

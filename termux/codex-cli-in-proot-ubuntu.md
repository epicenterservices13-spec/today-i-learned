# Deploying OpenAI Codex CLI in PRoot Ubuntu Containers on Android

Isolating and executing `@openai/codex` agent CLI workflows inside PRoot Ubuntu glibc environments on Termux.

## Context

Running heavy AI developer CLI tools directly in Termux can encounter architecture mismatches (Android Bionic libc vs Linux glibc, missing prebuilt native bindings, or binary path contamination). 

By hosting `@openai/codex` inside a PRoot Ubuntu container (`proot-distro`), the agent operates within a standard Ubuntu ARM64 environment with access to standard Node.js, npm, and system packages, while retaining access to host storage via PRoot mounts.

## Implementation / Code

### 1. Install Codex in PRoot Ubuntu
Execute installation inside the container without polluting the native Termux global npm prefix:

```bash
# Enter Ubuntu proot and install global @openai/codex package
proot-distro login ubuntu -- npm install -g @openai/codex

# Verify installation & binary path
proot-distro login ubuntu -- which codex
# Output: /usr/local/bin/codex

proot-distro login ubuntu -- codex --version
# Output: codex-cli 0.164.0
```

### 2. Invoke Headless Agent Workflows from Termux Host
Command the PRoot agent directly from Termux scripts or aliases:

```bash
# Non-interactive headless execution
proot-distro login ubuntu -- codex exec "Audit repository structure and generate tests"

# Pass credentials and environment variables
proot-distro login ubuntu -- env OPENAI_API_KEY="$OPENAI_API_KEY" codex
```

### 3. Create Shorthand Host Wrapper
Expose the PRoot Codex binary directly to your host `$PATH` (`~/.local/bin/codex`):

```bash
cat << 'EOF' > ~/.local/bin/codex
#!/usr/bin/env bash
exec proot-distro login ubuntu -- codex "$@"
EOF
chmod +x ~/.local/bin/codex
```

## Takeaways

- **Runtime Isolation**: Keeping npm CLI agents inside PRoot prevents Bionic libc linker conflicts and keeps native Termux binaries lean.
- **Shared Storage Mounts**: PRoot containers automatically mount `/data/data/com.termux/files/home` and `/sdcard`, allowing the containerized agent to edit host files seamlessly.
- **Execution Overhead**: PRoot introduces negligible ptrace overhead for filesystem and CPU operations, while providing 100% Linux ARM64 ABI compatibility.

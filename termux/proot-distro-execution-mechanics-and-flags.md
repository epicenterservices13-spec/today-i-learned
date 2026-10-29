# PRoot-Distro Architecture, Syscall Interception, and Execution Flags

Understanding `proot` user-space virtualization mechanics via `ptrace(2)` and mastering `proot-distro` container lifecycle, filesystem isolation, and performance flags on Android Termux.

## Context

Android security architecture forbids unprivileged user namespaces (`CLONE_NEWUSER`, `CLONE_NEWNS`) and prevents non-root access to standard Linux root directories (`/`, `/bin`, `/lib`, `/usr`). Standard Docker and LXC containers cannot run without a customized kernel and root access.

`proot` circumvents these kernel restrictions entirely in user-space by leveraging `ptrace(2)` syscall tracing. Instead of true kernel-level containerization, `proot` intercepts every syscall issued by guest binaries before it reaches the Linux kernel, dynamically rewriting file paths to guest rootfs trees, faking UID/GID 0 (root), and emulating missing POSIX features. 

Without understanding `proot-distro` operational flags, guest containers can inadvertently expose or collide with Android host files, suffer unnecessary `ptrace` latency, or fail on unhandled syscalls.

## Implementation / Code

### 1. Underlying Execution Inspection
To see the raw `proot` command synthesized beneath `proot-distro`:

```bash
# Print the exact proot command line without launching the session
proot-distro login --get-proot-cmd ubuntu
```

This reveals the underlying `ptrace` intercepts: `--kill-on-exit`, `--link2symlink`, `--sysvipc`, synthetic `/proc` and `/sys` bindings, and guest root mapping (`--rootfs=...`).

### 2. Isolation and Minimal Performance Modes

By default, `proot-distro` bind-mounts Android host storage and system directories (`/storage`, `/apex`, `/system`, `/data/data/com.termux`). Control isolation with:

```bash
# Isolated Mode: Strip host binds; confine processes purely to guest rootfs
proot-distro login --isolated ubuntu

# Minimal Mode: Extreme stripped profile; binds only /dev, /proc, and /sys
# Disables synthetic proc/sysctl workarounds to minimize ptrace tracing overhead
proot-distro login --minimal ubuntu
```

### 3. Granular Bind Mounts and Host Bridges

```bash
# Mount host Termux home to a clean mountpoint inside the container
proot-distro login ubuntu --bind /data/data/com.termux/files/home:/host

# Share host HOME, host temporary directory, and local X11 socket
proot-distro login ubuntu --shared-home --shared-tmp --shared-x11

# Drop faked root to an unprivileged guest user
proot-distro login ubuntu --user devuser --work-dir /home/devuser
```

### 4. Backgrounding & Port Redirection

Android forbids non-root users from binding to ports `< 1024`. PRoot redirects privileged ports into unprivileged ranges:

```bash
# Shift privileged ports: 80 -> 2080, 22 -> 2022
# Detach session to run persistent services in the background
proot-distro run --redirect-ports --detach ubuntu -- /usr/sbin/nginx -g 'daemon off;'

# Inspect and terminate running sessions
proot-distro ps
proot-distro kill <PID>
```

### 5. Archiving and Restoring Rootfs Constructs

```bash
# Create an atomic compressed archive of a container
proot-distro backup ubuntu --output ~/30_DOCS/backups/ubuntu-2026.tar.gz

# Restore a container from an archive
proot-distro restore ~/30_DOCS/backups/ubuntu-2026.tar.gz
```

## Takeaways

- **Syscall Overhead (`ptrace`)**: PRoot is not native speed; I/O-heavy operations (e.g. `npm install`, git operations with thousands of loose objects) incur a double context-switch cost per syscall. Use `--minimal` when raw throughput is needed.
- **Port Shifts**: PRoot's `--redirect-ports` flag uses a hardcoded port offset in the compiled binary; services configured for port 80 listen on port 2080 on the host interface.
- **Hardlink Emulation**: Standard Android internal storage does not support standard hardlinks across unprivileged boundaries; `proot-distro` automatically enables `--link2symlink` using `.l2s` symlink trees. Do not disable this unless running on a permissive ext4 partition.
- **Lifecycle Cleanliness**: Use `proot-distro list` and `proot-distro ps` to keep container state and background sessions strictly inventoried.

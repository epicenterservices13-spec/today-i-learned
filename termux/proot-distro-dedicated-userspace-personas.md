# Dedicated PRoot Userspace Personas with Host Binding

Isolate specialized development environments and operational roles inside unprivileged PRoot Ubuntu userspaces while maintaining shared host storage bridges.

## Context

Running all operations inside a `proot-distro` container as `root` causes configuration pollution, permissions mismatches, and monolithic dependency bloat. Tools like Node.js global packages, Python virtual environments, and AI agents end up sharing the same `$HOME` directory, leading to package collisions and messy shell histories.

However, standard unprivileged Linux users created inside PRoot often lack seamless access to Android host directories (`$HOME` in Termux, `/sdcard`), trapping data inside the guest filesystem.

By provisioning dedicated Linux users inside the PRoot container and binding the Termux host filesystem to a dedicated `/host` mountpoint, you achieve clean domain isolation (e.g. `turbo` for content production, `brainrot` for media pipelines, `dev` for engineering) without forfeiting access to host storage.

## Implementation / Code

### 1. Provisioning Dedicated Container Personas

Inside the PRoot container (as `root`), create the persona user accounts with dedicated home directories and default bash shells:

```bash
# Log in as root inside Ubuntu container
proot-distro login ubuntu

# Create isolated persona user
useradd -m -s /bin/bash turbo
usermod -aG sudo turbo

# Set up default directory structure
mkdir -p /home/turbo/{10_DEV,20_MEDIA,50_OPS}
chown -R turbo:turbo /home/turbo
```

### 2. Establishing Host Bridges and Workspace Ingress

Launch the container directly into the persona workspace while binding the Android Termux home directory to `/host`:

```bash
# Launch as user 'turbo' directly into /home/turbo with Termux $HOME bound to /host
proot-distro login ubuntu \
    --user turbo \
    --work-dir /home/turbo \
    --shared-tmp \
    --bind "$HOME:/host"
```

### 3. Binding Fast Shell Aliases (`proot_aliases.sh`)

Standardize workspace entrypoints in your Termux `.bashrc`:

```bash
# 🐢 Turbo Persona (Content Creation, Video Ops, Shorts Automation)
alias turbo='proot-distro login ubuntu --user turbo --work-dir /home/turbo --shared-tmp --bind "$HOME:/host"'
alias u-turbo='proot-distro login ubuntu --user turbo --work-dir /home/turbo --shared-tmp --bind "$HOME:/host"'

# 🧠 Brainrot Persona (Media Swarm Pipeline)
alias brain='proot-distro login ubuntu --user brainrot --work-dir /home/brainrot --shared-tmp --bind "$HOME:/host"'

# Isolated Sandbox (No host access, pure container quarantine)
alias turbo-iso='proot-distro login ubuntu --user turbo --work-dir /home/turbo --isolated --shared-tmp'
```

### 4. Symlinking Shared Host Mounts

Inside `/home/turbo`, link directly to host resources without duplicating disk space:

```bash
# Inside Ubuntu (/home/turbo)
ln -s /sdcard sdcard
ln -s /host/55_INFRA/dotfiles/agents .agents
ln -s /host/20_MEDIA/21_SOUNDTRACK assets/soundtracks
```

## Takeaways

- **Permission Hygeine**: Guest users run as unprivileged UIDs, preventing accidental global system mutations or root package overwrites.
- **Bi-directional Bridge**: Access Android Termux files at `/host/<path>` and guest files at `/data/data/com.termux/files/usr/var/lib/proot-distro/containers/ubuntu/rootfs/home/<user>/`.
- **Domain Cleanliness**: Git configurations, SSH keys, pip/npm caches, and command histories stay strictly segregated per persona.
- **Quarantine Toggle**: Use `--isolated` flag instead of `--bind` when running untested code that should not have access to host Termux storage.

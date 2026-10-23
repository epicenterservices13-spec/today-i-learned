# Universal Johnny Decimal Taxonomy Across PRoot Containers

Enforce structural sector parity between host Termux environments and isolated PRoot distributions using automated scripts and bridge symlinks.

## Context

Chrooted and virtualized PRoot distributions (such as Ubuntu or Void Linux) run on top of Termux. Without explicit governance, tools, dotfiles, and projects drift into divergent hierarchies inside container root filesystems (`/root`, `/home/ubuntu`), causing fragmentation and accidental data loss.

## Implementation / Code

```bash
UBUNTU_ROOTFS="/data/data/com.termux/files/usr/var/lib/proot-distro/containers/ubuntu/rootfs"
SECTORS=("00_INBOX" "10_DEV" "20_MEDIA" "30_DOCS" "40_BUSINESS" "50_OPS" "55_INFRA" "90_VAULT" "99_OUTBOX")

# Provision identical taxonomy into container root and user directories
for sector in "${SECTORS[@]}"; do
    mkdir -p "$UBUNTU_ROOTFS/root/$sector"
    mkdir -p "$UBUNTU_ROOTFS/home/ubuntu/$sector"
done

# Bridge container paths back to the host in 99_OUTBOX/03_BRIDGES
mkdir -p "$HOME/99_OUTBOX/03_BRIDGES"
ln -sfn "$UBUNTU_ROOTFS/root" "$HOME/99_OUTBOX/03_BRIDGES/ubuntu-root"
ln -sfn "$UBUNTU_ROOTFS/home/ubuntu" "$HOME/99_OUTBOX/03_BRIDGES/ubuntu"
```

## Takeaways

- Every container environment must mirror the host Johnny Decimal taxonomy.
- Symlinks in `99_OUTBOX/03_BRIDGES/` provide seamless, bidirectional host-to-container access without path hunting.
- Centralize provisioning scripts in `50_OPS/51_SCRIPTS/` to allow deterministic reconstruction.

# Today I Learned

> A collection of concise, battle-tested write-ups on commands, systems architecture, and engineering discipline.

**Total TILs documented:** `10`

---

## Categories

- [Architecture & Taxonomy](#arch) (`2`)
- [Bash & Shell Scripting](#bash) (`2`)
- [Git Discipline & Version Control](#git) (`1`)
- [Linux Administration & Storage](#linux) (`3`)
- [Termux & Android POSIX](#termux) (`2`)

---

<a id="arch"></a>
### Architecture & Taxonomy

- [Zero Root Clutter via Johnny Decimal Governance](arch/johnny-decimal-root-governance.md)
- [Universal Johnny Decimal Taxonomy Across PRoot Containers](arch/proot-distro-taxonomy-synchronization.md)

<a id="bash"></a>
### Bash & Shell Scripting

- [Fail-Fast Shell Scripts with set -euo pipefail](bash/safe-shell-pipelines.md)
- [Standard Stream Redirection and /dev/null Descriptor Mechanics](bash/stream-redirection-dev-null.md)

<a id="git"></a>
### Git Discipline & Version Control

- [Single-File Atomic Commits in Git](git/atomic-commits-per-file.md)

<a id="linux"></a>
### Linux Administration & Storage

- [Atomic Audit Trail Logging for Filesystem Mutations](linux/atomic-audit-trail-logging.md)
- [Zero-Download Remote Auditing and Safe Deduplication with Rclone](linux/rclone-cloud-remote-auditing.md)
- [Rsync vs MV for Mass Transfers and Safe Migration](linux/rsync-vs-mv-large-transfers.md)

<a id="termux"></a>
### Termux & Android POSIX

- [Portable Shebangs in Android Termux ARM64 Environments](termux/arm64-portable-shebangs.md)
- [Termux Extra Keys Layout Restoration and Instant Reload](termux/termux-extra-keys-configuration.md)

---

## Adding a TIL

1. Copy [`template.md`](template.md) into the appropriate category folder:
   ```bash
   cp template.md bash/my-topic.md
   ```
2. Populate your notes following the structured sections.
3. Rebuild the index:
   ```bash
   python3 scripts/build_index.py
   ```
4. Enforce atomic commits:
   ```bash
   git add bash/my-topic.md && git commit -m "bash/my-topic.md: add notes on my topic"
   git add README.md && git commit -m "README.md: update index"
   ```

## License

MIT License. See [LICENSE](LICENSE).
